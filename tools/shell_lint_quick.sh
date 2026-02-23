#!/usr/bin/env bash
set -euo pipefail

# Quick lint for FlowMind tools/*.sh
# - bash -n syntax check
# - deny known "copy/paste corruption" markers
# - ignore intentional regex definitions (e.g. SELF_BAD_RE in preflight)

ROOT="${1:-tools}"

if [[ ! -d "${ROOT}" ]]; then
  echo "[WARN] root not found: ${ROOT}" >&2
  exit 0
fi

bad=0
count=0

# Markers that often appear after terminal paste corruption
# NOTE: we will ignore lines that define SELF_BAD_RE=... (intentional)
BODY_CORRUPT_RE='(\&2>\&2|EOF:\ команду\ не\ знайдено|chmod \+x .*unt\}|safe\.shrt|with shebang|syntax valid"sh|EOF > path/to/file|command not found)'

while IFS= read -r -d '' f; do
  count=$((count+1))

  # skip self-lint recursion
  if [[ "$(basename -- "$f")" == "shell_lint_quick.sh" ]]; then
    echo "[OK] $f (self-skip)" >&2
    continue
  fi

  # bash syntax
  if ! bash -n "$f" >/dev/null 2>&1; then
    echo "[FAIL] bash -n: $f" >&2
    bash -n "$f" || true
    bad=$((bad+1))
    continue
  fi

  # body corruption scan with ignore for intentional detector regex
  # ignore any line containing: SELF_BAD_RE=
  hits="$(grep -nE "${BODY_CORRUPT_RE}" "$f" 2>/dev/null | grep -v 'SELF_BAD_RE=' || true)"
  if [[ -n "${hits}" ]]; then
    echo "[FAIL] corruption markers detected (body): $f" >&2
    echo "${hits}" >&2
    bad=$((bad+1))
    continue
  fi

  echo "[OK] $f" >&2
done < <(find "${ROOT}" -maxdepth 1 -type f -name "*.sh" -print0)

echo "[INFO] checked scripts: ${count}, failures: ${bad}" >&2
if [[ "${bad}" -gt 0 ]]; then
  exit 1
fi
