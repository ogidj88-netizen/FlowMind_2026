#!/usr/bin/env bash
set -euo pipefail

# FlowMind Preflight (MIN+JSON+STUB-WARN+MANIFEST-GUARD)
# - shell lint
# - json lint
# - warn if STUB/DO_NOT_PUBLISH markers exist
# - manifest guard scan (no direct writes to ExecutionManifest.json)
# - basic git sanity

echo "[PRE] shell lint..." >&2
make lint

echo "[PRE] json lint..." >&2
tools/json_lint_quick.sh projects

echo "[WARN] STUB/DO_NOT_PUBLISH scan..." >&2
# Warning only — does not fail the build
grep -RIn --include='S2_script.json' -E '"status"\s*:\s*"STUB|DO_NOT_PUBLISH' projects 2>/dev/null \
  | sed 's/^/[WARN] /' >&2 || true

echo "[PRE] manifest guard..." >&2
python3 tools/manifest_guard_scan.py

echo "[PRE] git status..." >&2
git status --porcelain >&2 || true

echo "[OK] preflight passed" >&2
