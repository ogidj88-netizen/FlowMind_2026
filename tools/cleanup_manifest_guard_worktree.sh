#!/usr/bin/env bash
set -euo pipefail

echo "[CLEAN] removing one-off patchers..." >&2
rm -f tools/patch_dispatcher_engine_single_writer.py || true
rm -f tools/patch_manifest_single_writer.py || true

echo "[CLEAN] normalize index state (avoid AM/MM traps)..." >&2
# If something got staged partially, unstage it so you control commits cleanly.
git restore --staged .gitignore 2>/dev/null || true
git restore --staged tools/preflight.sh 2>/dev/null || true
git restore --staged tools/manifest_guard_scan.py 2>/dev/null || true
git restore --staged manifest_engine/engine.py 2>/dev/null || true
git restore --staged tools/manifest_write.py 2>/dev/null || true

echo "[CLEAN] show status..." >&2
git status --porcelain >&2 || true

echo "[OK] cleanup done" >&2
