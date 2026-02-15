#!/usr/bin/env bash
# Run from repo root (Auto-FTP-Sync-Plus). Builds repo, commits, pushes. Optional: tag + release.
# Usage:
#   ./gitpush.sh                          # commit message: "Update repo output and docs"
#   ./gitpush.sh "Fix sync bug"            # custom commit message
#   ./gitpush.sh "Release 1.0.0" v1.0.0   # commit, push, tag v1.0.0, push tag, create GitHub release if gh installed
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

# Only stage what belongs on GitHub (no git add -A)
git add addons/ repo/ README.md CHANGELOG.md .gitignore ENTWICKLUNG.md gitpush.sh 2>/dev/null || true
git add repo/output/ 2>/dev/null || true
echo "--- git status ---"
git status

if git commit -m "$COMMIT_MSG"; then
  BRANCH=$(git rev-parse --abbrev-ref HEAD)
  git push origin "$BRANCH"
else
  echo "Nothing to commit or commit failed."
  if [ -z "$TAG" ]; then
    exit 0
  fi
  echo "Creating tag and release only (on current HEAD)."
fi

if [ -n "$TAG" ]; then
  TAG=$(echo "$TAG" | sed 's/^v//')
  if [[ ! "$TAG" =~ ^v ]]; then
    TAG="v$TAG"
  fi
  echo ""
  echo "Creating tag $TAG..."
  git tag -a "$TAG" -m "Release $TAG"
  git push origin "$TAG"

  # Release notes: extract English block from CHANGELOG for this version
  VER="${TAG#v}"
  REINSTALL_HINT="If you are updating from an older version, reinstalling the addon may be required."
  NOTES_FILE=$(mktemp)
  trap 'rm -f "$NOTES_FILE"' EXIT

  awk -v ver="$VER" '
    $0 ~ /^## \[/ && index($0, "[" ver "]") > 0 { in_version=1; next }
    in_version && /^### English/ { in_english=1; next }
    in_english && (/^---/ || /^## \[/) { exit }
    in_english { print }
  ' CHANGELOG.md | tr -d '\r' > "$NOTES_FILE"
  echo "" >> "$NOTES_FILE"
  echo "$REINSTALL_HINT" >> "$NOTES_FILE"

  if command -v gh >/dev/null 2>&1; then
    echo ""
    echo "Creating GitHub release $TAG..."
    gh release create "$TAG" --notes-file "$NOTES_FILE"
    echo "Done. Release: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/$TAG"
  else
    echo ""
    echo "--- Create GitHub release manually ---"
    echo "1. Open: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/new"
    echo "2. Choose tag: $TAG"
    echo "3. Title: e.g. Release $TAG"
    echo "4. Description: Copy the English section for this version from CHANGELOG.md (### English under ## [${VER}]) and add:"
    echo "   $REINSTALL_HINT"
    echo "   CHANGELOG.md is in the repo root."
  fi
else
  echo ""
  echo "Done. For a release: ./gitpush.sh \"Release 1.0.0\" v1.0.0"
fi
