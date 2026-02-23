#!/usr/bin/env bash
set -euo pipefail

# FlowMind — Commit Core Tools
# - runs preflight
# - stages canonical core toolchain only (via tools/git_stage_core_tools.sh)
# - commits and pushes

MSG="${1:-chore(tools): stabilize preflight + shell lint after paste-corruption}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"

if [[ ! -x tools/preflight.sh ]]; then
  echo "[ERR] missing or not executable: tools/preflight.sh" >&2
  exit 2
fi

if [[ ! -x tools/git_stage_core_tools.sh ]]; then
  echo "[ERR] missing or not executable: tools/git_stage_core_tools.sh" >&2
  exit 2
fi

echo "[PRE] preflight..." >&2
tools/preflight.sh

echo "[PRE] staging core tools..." >&2
tools/git_stage_core_tools.sh

echo "[PRE] verifying staged set..." >&2
git diff --cached --name-only | sed 's/^/[STAGED] /' >&2 || true

if git diff --cached --quiet; then
  echo "[OK] nothing to commit (staging empty)." >&2
  exit 0
fi

echo "[PRE] commit..." >&2
git commit -m "$MSG"

echo "[PRE] push..." >&2
git push

echo "[OK] done." >&2
