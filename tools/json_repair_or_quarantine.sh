#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   tools/json_repair_or_quarantine.sh <path_to_json>
#
# Behavior:
# - if valid JSON -> OK
# - if invalid -> move to quarantine with timestamp suffix and FAIL

F="${1:-}"
if [[ -z "${F}" ]]; then
  echo "[ERR] Usage: tools/json_repair_or_quarantine.sh <path_to_json>" >&2
  exit 2
fi

if [[ ! -f "${F}" ]]; then
  echo "[ERR] file not found: ${F}" >&2
  exit 2
fi

if python3 -m json.tool "${F}" >/dev/null 2>&1; then
  echo "[OK] valid JSON: ${F}" >&2
  exit 0
fi

TS="$(date +%Y%m%d_%H%M%S)"
QDIR="tmp/_json_quarantine"
mkdir -p "${QDIR}"

base="$(basename -- "${F}")"
dst="${QDIR}/${base}.${TS}.INVALID.json"

mv -f "${F}" "${dst}"
echo "[FAIL] invalid JSON quarantined: ${F} -> ${dst}" >&2
exit 1
