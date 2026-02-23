#!/usr/bin/env bash
set -euo pipefail

# FlowMind JSON Writer (LOCKED + ATOMIC)
#
# Usage:
#   tools/json_write_locked.sh <path> << 'JSON'
#   { ... }
#   JSON
#
# Guarantees:
# - exclusive lock (flock if available; else mkdir lock)
# - directory auto-create
# - atomic write (temp + mv)
# - valid JSON (python -m json.tool)
#
# Notes:
# - lock is per-target path: <path>.lock

TARGET="${1:-}"
if [[ -z "${TARGET}" ]]; then
  echo "[ERR] Usage: tools/json_write_locked.sh <path>" >&2
  exit 2
fi

DIR="$(dirname -- "${TARGET}")"
mkdir -p "${DIR}"

LOCKFILE="${TARGET}.lock"
TMP="${TARGET}.tmp.$$"

cleanup() {
  rm -f "${TMP}" 2>/dev/null || true
}
trap cleanup EXIT

write_and_validate() {
  cat > "${TMP}"
  python3 -m json.tool "${TMP}" >/dev/null
  mv -f "${TMP}" "${TARGET}"
}

# Prefer flock if available
if command -v flock >/dev/null 2>&1; then
  exec 9>"${LOCKFILE}"
  flock -x 9
  write_and_validate
  flock -u 9 || true
  exec 9>&-
  echo "[OK] wrote valid JSON (locked+atomic): ${TARGET}" >&2
  exit 0
fi

# Fallback: mkdir lock (portable)
LOCKDIR="${LOCKFILE}.d"
tries=0
max_tries=200
sleep_s=0.05

while ! mkdir "${LOCKDIR}" 2>/dev/null; do
  tries=$((tries+1))
  if [[ "${tries}" -ge "${max_tries}" ]]; then
    echo "[ERR] could not acquire lock: ${LOCKDIR}" >&2
    exit 1
  fi
  sleep "${sleep_s}"
done

# Ensure lock release
release_lock() { rmdir "${LOCKDIR}" 2>/dev/null || true; }
trap 'cleanup; release_lock' EXIT

write_and_validate
release_lock

echo "[OK] wrote valid JSON (mkdir-lock+atomic): ${TARGET}" >&2
