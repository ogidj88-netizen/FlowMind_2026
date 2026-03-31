#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[dispatcher-check] py_compile"
python -m py_compile engine/canonical_dispatcher.py
python -m py_compile tools/run_dispatcher_checks.py

echo "[dispatcher-check] running consolidated checks"
python tools/run_dispatcher_checks.py

echo "[dispatcher-check] OK"
