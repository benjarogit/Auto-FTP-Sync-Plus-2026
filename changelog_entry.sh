#!/usr/bin/env bash
# Erstellt einen neuen CHANGELOG-Eintrag für die angegebene Version.
# Nutzt die Git-Commits seit dem letzten Tag als Bullet-Liste (DE + EN).
# Usage: ./changelog_entry.sh 1.0.2
# Danach CHANGELOG.md ggf. anpassen und ./gitpush.sh release 1.0.2 ausführen.
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

# Letzten Tag finden (höchster Tag vor dieser Version)
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
if [ -n "$PREV_TAG" ]; then
  COMMITS=$(git log "$PREV_TAG"..HEAD --pretty=format:"- %s" 2>/dev/null | grep -v "^- Release " || true)
fi
if [ -z "$COMMITS" ]; then
  COMMITS="- Release $VERSION"
fi

# English: dieselbe Liste (Commit-Messages oft schon EN)
EN_LINE="$COMMITS"

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

echo "CHANGELOG.md: Eintrag für $VERSION ergänzt (Commits seit ${PREV_TAG:-Anfang})."
echo "Bitte prüfen, ggf. anpassen, dann: ./gitpush.sh release $VERSION"
