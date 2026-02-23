#!/usr/bin/env bash
set -euo pipefail

# FlowMind — SELFTEST :: Manifest Single-Writer
# Creates a temporary project, writes ExecutionManifest.json via locked writer,
# validates JSON, runs manifest guard, and cleans up.
#
# PASS criteria:
# - manifest file exists
# - json parses
# - manifest_guard_scan.py passes
# - preflight passes (note: may warn about other things, but should not fail)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PROJECT_ID="FM_SMOKE_SINGLE_WRITER"
PROJ_DIR="projects/${PROJECT_ID}"
MANIFEST="${PROJ_DIR}/ExecutionManifest.json"

cleanup() {
  rm -rf "${PROJ_DIR}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

mkdir -p "${PROJ_DIR}"

if [[ ! -x "tools/json_write_locked.sh" ]]; then
  echo "[ERR] missing or not executable: tools/json_write_locked.sh" >&2
  exit 2
fi

if [[ ! -x "tools/manifest_guard_scan.py" ]]; then
  echo "[ERR] missing or not executable: tools/manifest_guard_scan.py" >&2
  exit 2
fi

if [[ ! -f "tools/manifest_write.py" ]]; then
  echo "[ERR] missing: tools/manifest_write.py" >&2
  exit 2
fi

echo "[INFO] writing manifest via locked writer: ${MANIFEST}" >&2

python3 - << 'PY'
import json, os, subprocess, sys
from pathlib import Path

project_id = os.environ.get("PROJECT_ID", "FM_SMOKE_SINGLE_WRITER")
proj_dir = Path("projects") / project_id
manifest_path = proj_dir / "ExecutionManifest.json"

manifest = {
  "schema": "EXECUTION_MANIFEST_V1",
  "project_id": project_id,
  "manifest_version": 1,
  "status": "CREATED",
  "phase": "CREATED",
  "created_utc": "SELFTEST",
  "artifact_registry": [],
  "notes": {
    "selftest": True,
    "rule": "manifest written ONLY via tools/json_write_locked.sh"
  }
}

data = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
writer = Path("tools") / "json_write_locked.sh"

proc = subprocess.run(
  [str(writer), str(manifest_path)],
  input=data.encode("utf-8"),
  stdout=subprocess.PIPE,
  stderr=subprocess.PIPE,
)

if proc.returncode != 0:
  sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))
  raise SystemExit(proc.returncode)

print("[OK] manifest written (locked writer):", manifest_path)
PY

echo "[INFO] validating JSON parse..." >&2
python3 -c 'import json; json.load(open("'"${MANIFEST}"'", "r", encoding="utf-8")); print("[OK] json parses")'

echo "[INFO] running manifest guard..." >&2
python3 tools/manifest_guard_scan.py

echo "[INFO] running preflight..." >&2
tools/preflight.sh

echo "[OK] SELFTEST PASS (single-writer + guard + preflight)" >&2
