#!/usr/bin/env bash
set -euo pipefail

# Safe editor wrapper (no big pastes).
# Usage:
#   tools/fm_edit.sh <path>

TARGET="${1:-}"
if [[ -z "${TARGET}" ]]; then
  echo "[ERR] Usage: tools/fm_edit.sh <path>" >&2
  exit 2
fi

mkdir -p "$(dirname -- "${TARGET}")"

nano "${TARGET}"

echo "[INFO] running lint after edit..." >&2
make lint
echo "[OK] edit+lint passed: ${TARGET}" >&2
