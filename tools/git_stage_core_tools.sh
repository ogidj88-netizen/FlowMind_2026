#!/usr/bin/env bash
set -euo pipefail

# FlowMind — Stage Core Tools (canonical)
# Goal: stage only stable tooling + hygiene files (no project outputs, no temp scripts)

FILES=(
  ".gitignore"
  "Makefile"
  "tools/README_SAFE_EDITING.md"
  "tools/preflight.sh"
  "tools/shell_lint_quick.sh"
  "tools/json_lint_quick.sh"
  "tools/json_write_safe.sh"
  "tools/json_write_locked.sh"
  "tools/json_repair_or_quarantine.sh"
  "tools/json_autofix_s2_or_quarantine.sh"
  "tools/rewrite_json_write_safe.sh"
  "tools/write_text_atomic.sh"
  "tools/fm_edit.sh"
  "tools/git_stage_core_tools.sh"
  "tools/git_stage_manifest_single_writer_fix.sh"
  "tools/cleanup_manifest_guard_worktree.sh"
  "tools/manifest_guard_scan.py"
  "tools/manifest_write.py"
)

missing=0
for f in "${FILES[@]}"; do
  if [[ ! -e "$f" ]]; then
    echo "[WARN] missing: $f" >&2
    missing=$((missing+1))
    continue
  fi
  git add "$f"
  echo "[OK] staged: $f" >&2
done

if [[ "$missing" -gt 0 ]]; then
  echo "[WARN] missing files: $missing (stage continued)" >&2
fi

echo "[INFO] staged core tools + hygiene set." >&2
