#!/usr/bin/env bash
set -euo pipefail

# FlowMind JSON Lint (Quick)
# - validates JSON syntax via python -m json.tool
# - scans key folders (projects/, dispatcher/, manifest_engine/, engine/, intelligence/) if present
# - fails fast on first invalid JSON

ROOTS=()
[[ -d "projects" ]] && ROOTS+=("projects")
[[ -d "dispatcher" ]] && ROOTS+=("dispatcher")
[[ -d "manifest_engine" ]] && ROOTS+=("manifest_engine")
[[ -d "engine" ]] && ROOTS+=("engine")
[[ -d "intelligence" ]] && ROOTS+=("intelligence")

if [[ "${#ROOTS[@]}" -eq 0 ]]; then
  echo "[WARN] no known roots found for JSON scan (projects/engine/etc). Skipping." >&2
  exit 0
fi

count=0
bad=0

# Exclude huge/temporary dirs
EXCLUDES=(
  "./tmp/*"
  "./.venv/*"
  "./node_modules/*"
  "./_ARCHIVE_FULL_SYSTEM/*"
)

is_excluded() {
  local f="$1"
  for pat in "${EXCLUDES[@]}"; do
    if [[ "$f" == $pat ]]; then
      return 0
    fi
  done
  return 1
}

while IFS= read -r -d '' f; do
  is_excluded "$f" && continue
  count=$((count+1))

  if [[ ! -s "$f" ]]; then
    echo "[FAIL] empty JSON file: $f" >&2
    bad=$((bad+1))
    break
  fi

  if ! python3 -m json.tool "$f" >/dev/null 2>&1; then
    echo "[FAIL] invalid JSON: $f" >&2
    python3 -m json.tool "$f" >/dev/null 2>&1 || true
    bad=$((bad+1))
    break
  fi

  echo "[OK] $f" >&2
done < <(find "${ROOTS[@]}" -type f -name "*.json" -print0)

echo "[INFO] checked json files: ${count}, failures: ${bad}" >&2
if [[ "${bad}" -gt 0 ]]; then
  exit 1
fi
