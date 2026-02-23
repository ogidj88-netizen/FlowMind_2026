#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   tools/json_write_safe.sh <path> << 'JSON'
#   { ... }
#   JSON
#
# Guarantees:
# - atomic write (temp + mv)
# - valid JSON (python -m json.tool)
# - directory auto-create

TARGET="${1:-}"
if [[ -z "${TARGET}" ]]; then
  echo "[ERR] Usage: tools/json_write_safe.sh <path>" >&2
  exit 2
fi

DIR="$(dirname -- "${TARGET}")"
mkdir -p "${DIR}"

TMP="${TARGET}.tmp.$$"
cleanup() { rm -f "${TMP}" 2>/dev/null || true; }
trap cleanup EXIT

# Read stdin into temp file
cat > "${TMP}"

# Validate JSON
python3 -m json.tool "${TMP}" >/dev/null

# Atomic replace
mv -f "${TMP}" "${TARGET}"

# Prevent trap from removing the moved file in weird shells
trap - EXIT

echo "[OK] wrote valid JSON atomically: ${TARGET}" >&2
