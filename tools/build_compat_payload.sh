#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "USAGE: tools/build_compat_payload.sh <PROJECT_ID> [OUTPUT_PATH]" >&2
  exit 2
fi

PROJECT_ID="$1"
STATE_PATH="projects/${PROJECT_ID}/PROJECT_STATE.json"

if [[ ! -f "$STATE_PATH" ]]; then
  echo "ERROR: canonical state not found: $STATE_PATH" >&2
  exit 1
fi

if [[ $# -eq 2 ]]; then
  OUTPUT_PATH="$2"
else
  OUTPUT_PATH="projects/${PROJECT_ID}/compat_payload_v1.json"
fi

python3 adapters/read_only_compat_adapter.py \
  --state "$STATE_PATH" \
  --output "$OUTPUT_PATH" \
  --pretty

echo "COMPAT_PAYLOAD_OK"
echo "project_id=${PROJECT_ID}"
echo "state=${STATE_PATH}"
echo "output=${OUTPUT_PATH}"
