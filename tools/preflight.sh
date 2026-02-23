#!/usr/bin/env bash
set -euo pipefail

# FlowMind — Preflight (canonical)
# Order:
# 1) shell lint
# 2) json lint
# 3) warn if STUB/DO_NOT_PUBLISH markers exist
# 4) manifest guard scan
# 5) git status summary (porcelain)
#
# This script MUST be deterministic and not depend on interactive shell state.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

c_err() { echo -e "[ERR] $*" >&2; }
c_pre() { echo -e "[PRE] $*" >&2; }
c_ok()  { echo -e "[OK] $*" >&2; }
c_warn(){ echo -e "[WARN] $*" >&2; }

need_exec() {
  local p="$1"
  if [[ ! -x "$p" ]]; then
    c_err "missing or not executable: $p"
    exit 2
  fi
}

# 1) shell lint
c_pre "shell lint..."
need_exec "${ROOT}/tools/shell_lint_quick.sh"
"${ROOT}/tools/shell_lint_quick.sh"
c_ok "shell lint done"

# 2) json lint
c_pre "json lint..."
need_exec "${ROOT}/tools/json_lint_quick.sh"
"${ROOT}/tools/json_lint_quick.sh"
c_ok "json lint done"

# 3) STUB / DO_NOT_PUBLISH scan (warn only)
c_warn "STUB/DO_NOT_PUBLISH scan..."
# scan only projects/*.json
if command -v rg >/dev/null 2>&1; then
  if rg -n --no-heading --glob 'projects/**/*.json' 'DO_NOT_PUBLISH|STUBBED' "${ROOT}" >/dev/null 2>&1; then
    rg -n --no-heading --glob 'projects/**/*.json' 'DO_NOT_PUBLISH|STUBBED' "${ROOT}" \
      | sed 's/^/[WARN] /' >&2 || true
  fi
else
  # grep fallback
  if grep -RIn --include='*.json' -E 'DO_NOT_PUBLISH|STUBBED' "${ROOT}/projects" >/dev/null 2>&1; then
    grep -RIn --include='*.json' -E 'DO_NOT_PUBLISH|STUBBED' "${ROOT}/projects" \
      | sed 's/^/[WARN] /' >&2 || true
  fi
fi

# 4) manifest guard
c_pre "manifest guard..."
if [[ -x "${ROOT}/tools/manifest_guard_scan.py" ]]; then
  python3 "${ROOT}/tools/manifest_guard_scan.py"
  c_ok "manifest guard passed"
else
  c_warn "manifest guard skipped (missing or not executable): tools/manifest_guard_scan.py"
fi

# 5) git status
c_pre "git status..."
git -C "${ROOT}" status --porcelain
c_ok "preflight passed"
