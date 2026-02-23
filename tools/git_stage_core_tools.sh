#!/usr/bin/env bash
set -euo pipefail

# Stage only the repo hygiene + toolchain files.
# Avoid staging tmp/ and run outputs.

FILES=(
  ".gitignore"
  "Makefile"
  "tools/README_SAFE_EDITING.md"
  "tools/fm_edit.sh"
  "tools/preflight.sh"
  "tools/shell_lint_quick.sh"
  "tools/json_lint_quick.sh"
  "tools/json_repair_or_quarantine.sh"
  "tools/json_write_safe.sh"
  "tools/rewrite_json_write_safe.sh"
  "tools/write_text_atomic.sh"
  "tools/stub_s2_script_v1.json"
  "tools/git_stage_core_tools.sh"
)

for f in "${FILES[@]}"; do
  if [[ -e "$f" ]]; then
    git add "$f"
    echo "[OK] staged: $f" >&2
  else
    echo "[WARN] missing (skip): $f" >&2
  fi
done

echo "[INFO] staged core toolchain files." >&2
git status --porcelain
