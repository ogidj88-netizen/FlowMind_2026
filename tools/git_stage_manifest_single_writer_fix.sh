#!/usr/bin/env bash
set -euo pipefail

FILES=(
  ".gitignore"
  "dispatcher/engine.py"
  "manifest_engine/engine.py"
  "tools/preflight.sh"
  "tools/manifest_guard_scan.py"
  "tools/manifest_write.py"
  "tools/cleanup_manifest_guard_worktree.sh"
)

for f in "${FILES[@]}"; do
  if [[ ! -e "$f" ]]; then
    echo "[ERR] missing file: $f" >&2
    exit 2
  fi
done

# Ensure no project outputs are staged by accident
git restore --staged projects 2>/dev/null || true

for f in "${FILES[@]}"; do
  git add "$f"
  echo "[OK] staged: $f" >&2
done

echo "[INFO] staged manifest single-writer fix set." >&2
git status --porcelain >&2 || true
