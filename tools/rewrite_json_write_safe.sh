#!/usr/bin/env bash
set -euo pipefail

# This script regenerates tools/json_write_safe.sh deterministically (no base64).
# Usage:
#   tools/rewrite_json_write_safe.sh

OUT="tools/json_write_safe.sh"

cat > "${OUT}" << 'SH'
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

cat > "${TMP}"
python3 -m json.tool "${TMP}" >/dev/null
mv -f "${TMP}" "${TARGET}"
trap - EXIT

echo "[OK] wrote valid JSON atomically: ${TARGET}" >&2
SH

chmod +x "${OUT}"
echo "[OK] regenerated: ${OUT}" >&2
