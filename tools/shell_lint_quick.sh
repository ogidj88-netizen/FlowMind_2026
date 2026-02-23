#!/usr/bin/env bash
set -euo pipefail

# FlowMind — Shell Lint Quick
# Lints all *.sh inside tools/ (excluding itself).
# No external deps beyond bash.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${ROOT}/tools"

fail=0
checked=0

while IFS= read -r -d '' f; do
  bn="$(basename "$f")"
  if [[ "$bn" == "shell_lint_quick.sh" ]]; then
    echo "[OK] tools/shell_lint_quick.sh (self-skip)" >&2
    continue
  fi

  checked=$((checked+1))

  if [[ ! -f "$f" ]]; then
    continue
  fi

  # Must have shebang for executable scripts, but we won't enforce executable bit here.
  # Syntax check:
  if bash -n "$f" >/dev/null 2>&1; then
    echo "[OK] $f" >&2
  else
    echo "[FAIL] $f" >&2
    bash -n "$f" 2>&1 | sed 's/^/       /' >&2 || true
    fail=$((fail+1))
  fi
done < <(find "$TOOLS_DIR" -maxdepth 1 -type f -name "*.sh" -print0 | sort -z)

echo "[INFO] checked scripts: ${checked}, failures: ${fail}" >&2
if [[ "$fail" -gt 0 ]]; then
  exit 1
fi
