#!/usr/bin/env bash
# Erstellt einen neuen CHANGELOG-Eintrag für die angegebene Version.
# Quelle 1: RELEASE_NOTES.txt (Stichpunkte für diese Version) → wird danach geleert.
# Quelle 2 (Fallback): Git-Commits seit letztem Tag.
# Usage: ./changelog_entry.sh 1.0.2
set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  echo "Usage: ./changelog_entry.sh <version>"
  echo "Example: ./changelog_entry.sh 1.0.2"
  exit 1
fi
VERSION="${VERSION#v}"

# Letzten Tag finden (für Fallback und Default-Text)
PREV_TAG=""
for t in $(git tag -l 'v*' | sort -V); do
  [ "$t" = "v$VERSION" ] && continue
  case "$(printf '%s\n%s\n' "v$VERSION" "$t" | sort -V | head -1)" in
    "v$VERSION") break ;;
    *) PREV_TAG="$t" ;;
  esac
done

DATE=$(date +%Y-%m-%d)
COMMITS=""
EN_LINE=""
USED_RELEASE_NOTES=0
RELEASE_NOTES_FILE="RELEASE_NOTES.txt"

# --- Quelle 1: RELEASE_NOTES.txt (während Entwicklung gefüllt) ---
if [ -f "$RELEASE_NOTES_FILE" ]; then
  CONTENT=$(python3 -c "
import sys
path = sys.argv[1]
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
header_end = 0
for i, line in enumerate(lines):
    s = line.strip()
    if s.startswith('#') or not s:
        continue
    if s == '### English' or s.startswith('- '):
        header_end = i
        break
de_bullets = []
en_bullets = []
in_english = False
for i in range(header_end, len(lines)):
    line = lines[i]
    s = line.strip()
    if s == '### English':
        in_english = True
        continue
    if s.startswith('- '):
        if in_english:
            en_bullets.append(s)
        else:
            de_bullets.append(s)
if de_bullets or en_bullets:
    de = chr(10).join(de_bullets) if de_bullets else ''
    en = chr(10).join(en_bullets) if en_bullets else de
    print('DE---')
    print(de)
    print('EN---')
    print(en)
else:
    sys.exit(1)
" "$RELEASE_NOTES_FILE" 2>/dev/null) || true
  if [ -n "$CONTENT" ]; then
    COMMITS=$(echo "$CONTENT" | sed -n '/^DE---$/,/^EN---$/p' | sed '1d;/^EN---$/d' | tr -d '\r')
    EN_LINE=$(echo "$CONTENT" | sed -n '/^EN---$/,$p' | sed '1d' | tr -d '\r')
    if [ -n "$(echo "$COMMITS" | tr -d '\n' | tr -d ' ')" ]; then
      USED_RELEASE_NOTES=1
      if [ -z "$(echo "$EN_LINE" | tr -d '\n' | tr -d ' ')" ]; then
        EN_LINE="$COMMITS"
      fi
    fi
  fi
fi

# --- Quelle 2 (Fallback): Git-Commits ---
if [ "$USED_RELEASE_NOTES" -eq 0 ]; then
  COMMITS_RAW=""
  if [ -n "$PREV_TAG" ]; then
    COMMITS_RAW=$(git log "$PREV_TAG"..HEAD --pretty=format:"- %s" 2>/dev/null || true)
  fi
  if [ -n "$COMMITS_RAW" ]; then
    COMMITS=$(echo "$COMMITS_RAW" | while read -r line; do
      if [[ "$line" =~ ^-\ Release\ [0-9]+\.[0-9]+\.[0-9]+ ]]; then continue; fi
      if [[ "$line" =~ ^-\ Update\ repo\ output ]]; then
        echo "- Plugin- und Repo-Build aktualisiert."
        continue
      fi
      echo "$line"
    done | sort -u)
  fi
  if [ -z "$(echo "$COMMITS" | tr -d '\n' | tr -d ' ')" ]; then
    COMMITS="- Plugin- und Repo-Updates seit ${PREV_TAG:-letztem Release}."
  fi
  EN_LINE="$COMMITS"
  if [[ "$COMMITS" = *"Plugin- und Repo-Updates seit"* ]] || [[ "$COMMITS" = *"Plugin- und Repo-Build aktualisiert"* ]] || [ "$COMMITS" = "- Release $VERSION" ]; then
    EN_LINE="Release $VERSION

- Plugin and repo updates since ${PREV_TAG:-last release}."
  fi
  EN_LINE=$(echo "$EN_LINE" | sed 's/^- Plugin- und Repo-Build aktualisiert\.$/- Build and repo output updated./')
  EN_LINE=$(echo "$EN_LINE" | sed "s/^- Plugin- und Repo-Updates seit ${PREV_TAG:-letztem Release}\.$/- Plugin and repo updates since ${PREV_TAG:-last release}./")
fi

# Neuer Block in Temp-Datei (wegen Zeilenumbrüchen)
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
cat > "$TMP" << BLOCK
## [$VERSION] – $DATE

$COMMITS

### English

$EN_LINE

---

BLOCK

# CHANGELOG.md: Block vor der ersten ## [ einfügen, Link ergänzen
python3 -c "
import re, sys
ver = sys.argv[1]
block_path = sys.argv[2]
path = 'CHANGELOG.md'
block = open(block_path).read()
content = open(path).read()
# Link am Ende einfügen, falls noch nicht vorhanden
link = f\"[{ver}]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v{ver}\n\"
if f'[{ver}]:' not in content:
    content = re.sub(r'(\n\[[\d.]+\]:)', link + r'\1', content, count=1)
# Block vor der ersten ## [ einfügen
match = re.search(r'^(\s*)(## \[)', content, re.MULTILINE)
if match:
    insert_pos = match.start(2)
    content = content[:insert_pos] + block + content[insert_pos:]
else:
    content = content.rstrip() + '\n\n' + block
open(path, 'w').write(content)
" "$VERSION" "$TMP"

# Nach Verwendung: RELEASE_NOTES.txt zurücksetzen (nur Kommentar-Header behalten)
if [ "$USED_RELEASE_NOTES" -eq 1 ] && [ -f "$RELEASE_NOTES_FILE" ]; then
  python3 -c "
path = 'RELEASE_NOTES.txt'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
header = []
for line in lines:
    s = line.strip()
    if s.startswith('- ') or s == '### English':
        break
    header.append(line)
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(header)
    if header and not header[-1].endswith(chr(10)):
        f.write(chr(10))
"
  echo "RELEASE_NOTES.txt geleert (nur Header behalten) – für nächste Version wieder befüllen."
fi

if [ "$USED_RELEASE_NOTES" -eq 1 ]; then
  echo "CHANGELOG.md: Eintrag für $VERSION ergänzt (aus RELEASE_NOTES.txt)."
else
  echo "CHANGELOG.md: Eintrag für $VERSION ergänzt (aus Git-Commits seit ${PREV_TAG:-Anfang})."
fi
