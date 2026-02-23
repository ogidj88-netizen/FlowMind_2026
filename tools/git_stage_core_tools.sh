#!/usr/bin/env bash
set -euo pipefail

# FlowMind — Stage Core Tools (canonical)
# Goal: stage only stable tooling + hygiene files (no project outputs, no temp scripts)

FILES=(
  ".gitignore"
  "Makefile"
  "tools/README_SAFE_EDITING.md"

  # Preflight + linters
  "tools/preflight.sh"
  "tools/shell_lint_quick.sh"
  "tools/json_lint_quick.sh"
  "tools/manifest_guard_scan.py"

  # Safe writers
  "tools/json_write_safe.sh"
  "tools/json_write_locked.sh"
  "tools/write_text_atomic.sh"
  "tools/fm_edit.sh"

  # JSON repair/autofix
  "tools/json_repair_or_quarantine.sh"
  "tools/json_autofix_s2_or_quarantine.sh"
  "tools/rewrite_json_write_safe.sh"

  # Manifest helpers
  "tools/manifest_write.py"
  "tools/git_stage_manifest_single_writer_fix.sh"
  "tools/cleanup_manifest_guard_worktree.sh"

  # Staging/commit helpers
  "tools/git_stage_core_tools.sh"
  "tools/git_commit_core_tools.sh"
)

ok=0
fail=0

for f in "${FILES[@]}"; do
  if [[ -e "$f" ]]; then
    git add "$f"
    echo "[OK] staged: $f" >&2
    ok=$((ok+1))
  else
    echo "[WARN] missing (skip): $f" >&2
    fail=$((fail+1))
  fi
done

echo "[INFO] staged core tools + hygiene set." >&2
echo "[INFO] ok=${ok} missing=${fail}" >&2
