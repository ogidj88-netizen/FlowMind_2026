#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   tools/write_text_atomic.sh <path> << 'TXT'
#   ...content...
#   TXT
#
# Guarantees:
# - atomic write (temp + mv)
# - directory auto-create

TARGET="${1:-}"
if [[ -z "${TARGET}" ]]; then
  echo "[ERR] Usage: tools/write_text_atomic.sh <path>" >&2
  exit 2
fi

DIR="$(dirname -- "${TARGET}")"
mkdir -p "${DIR}"

TMP="${TARGET}.tmp.$$"
cleanup() { rm -f "${TMP}" 2>/dev/null || true; }
trap cleanup EXIT

cat > "${TMP}"
mv -f "${TMP}" "${TARGET}"
trap - EXIT

echo "[OK] wrote atomically: ${TARGET}" >&2
