#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .githooks ]]; then
  echo "[ERR] missing .githooks/ directory" >&2
  exit 2
fi

if [[ ! -f .githooks/pre-commit ]]; then
  echo "[ERR] missing .githooks/pre-commit" >&2
  exit 2
fi

chmod +x .githooks/pre-commit

echo "[INFO] configuring git to use repo hooks path..." >&2
git config core.hooksPath .githooks

echo "[OK] core.hooksPath=$(git config core.hooksPath)" >&2

echo "[INFO] running preflight..." >&2
if [[ ! -x tools/preflight.sh ]]; then
  echo "[ERR] tools/preflight.sh missing or not executable" >&2
  exit 2
fi
tools/preflight.sh

echo "[OK] hooks installed + preflight OK" >&2
