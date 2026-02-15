#!/usr/bin/env bash
# Run from repo root (Auto-FTP-Sync-Plus). Builds repo, commits, pushes. Optional: tag + release.
# Usage:
#   ./gitpush.sh                          # commit message: "Update repo output and docs"
#   ./gitpush.sh "Fix sync bug"            # custom commit message
#   ./gitpush.sh "Release 1.0.0" v1.0.0   # commit, push, then create tag v1.0.0 and push tag
set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: Not inside a Git repository. Run this script from the repo root (Auto-FTP-Sync-Plus)."
  exit 1
fi

COMMIT_MSG="${1:-Update repo output and docs}"
TAG="${2:-}"

echo "Building repository..."
python3 repo/build_repo.py

git add addons/ repo/ README.md CHANGELOG.md .gitignore 2>/dev/null || true
git add repo/output/ 2>/dev/null || true
git add -A
echo "--- git status ---"
git status

git commit -m "$COMMIT_MSG" || { echo "Nothing to commit or commit failed."; exit 0; }

BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push origin "$BRANCH"

if [ -n "$TAG" ]; then
  TAG=$(echo "$TAG" | sed 's/^v//')  # allow 1.0.0 or v1.0.0
  if [[ ! "$TAG" =~ ^v ]]; then
    TAG="v$TAG"
  fi
  echo ""
  echo "Creating tag $TAG..."
  git tag -a "$TAG" -m "Release $TAG"
  git push origin "$TAG"
  echo ""
  echo "--- Release auf GitHub erstellen ---"
  echo "1. Öffne: https://github.com/benjarogit/Auto-FTP-Sync-Plus/releases/new"
  echo "2. Wähle Tag: $TAG"
  echo "3. Titel: z.B. Release $TAG"
  echo "4. Beschreibung: Abschnitt aus CHANGELOG.md für diese Version kopieren (## [${TAG#v}] – ...)"
  echo "   CHANGELOG.md liegt im Repo-Root."
else
  echo ""
  echo "Done. Für ein Release: ./gitpush.sh \"Release 1.0.0\" v1.0.0"
fi
