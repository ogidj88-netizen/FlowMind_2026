#!/usr/bin/env bash
set -euo pipefail

# FlowMind Preflight (MIN+JSON+STUB-WARN)
# - shell lint
# - json lint
# - warn if STUB/DO_NOT_PUBLISH markers exist
# - self-check for paste-corruption markers (ignore the detector line itself)
# - basic git sanity

SELF_BAD_RE='(\&2>\&2|with shebang|safe\.shrt|chmod \+x .*unt\}|EOF:\ команду\ не\ знайдено|syntax valid"sh|git add tools/preflight\.shd")'

# Self-check: scan this file, but IGNORE the line that defines SELF_BAD_RE=
self_hits="$(grep -nE "${SELF_BAD_RE}" "$0" 2>/dev/null | grep -v 'SELF_BAD_RE=' || true)"
if [[ -n "${self_hits}" ]]; then
  echo "[FAIL] preflight.sh looks corrupted (paste artifacts detected):" >&2
  echo "${self_hits}" >&2
  exit 1
fi

echo "[PRE] shell lint..." >&2
make lint

echo "[PRE] json lint..." >&2
tools/json_lint_quick.sh

# Warn on stubbed scripts (do not fail; just loud warning)
if [[ -d "projects" ]]; then
  hits="$(grep -R --line-number --fixed-strings -e '"DO_NOT_PUBLISH"' -e '"STUBBED' projects 2>/dev/null | head -n 20 || true)"
  if [[ -n "${hits}" ]]; then
    echo "[WARN] STUB/DO_NOT_PUBLISH markers found (review before any publish):" >&2
    echo "${hits}" >&2
  fi
fi

if command -v git >/dev/null 2>&1; then
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[PRE] git status..." >&2
    git status --porcelain || true
  else
    echo "[WARN] not inside a git repo (skip git checks)" >&2
  fi
else
  echo "[WARN] git not found (skip git checks)" >&2
fi

echo "[OK] preflight passed" >&2
