#!/usr/bin/env bash
set -euo pipefail

# FlowMind JSON AutoFix (fail-closed)
# - Scans projects/**.json
# - If invalid JSON:
#   - Quarantine invalid file
#   - FAIL immediately
#
# IMPORTANT:
# - No stub installation
# - No placeholder recovery
# - Invalid production JSON must halt the pipeline
#
# Usage:
#   tools/json_autofix_s2_or_quarantine.sh

if [[ ! -x "tools/json_repair_or_quarantine.sh" ]]; then
  echo "[ERR] missing or not executable: tools/json_repair_or_quarantine.sh" >&2
  exit 2
fi

if [[ ! -d "projects" ]]; then
  echo "[WARN] no projects/ folder; nothing to scan" >&2
  exit 0
fi

count=0
quarantined=0
failed=0

while IFS= read -r -d '' f; do
  count=$((count+1))

  if python3 -m json.tool "$f" >/dev/null 2>&1; then
    continue
  fi

  echo "[WARN] invalid JSON detected: $f" >&2

  tools/json_repair_or_quarantine.sh "$f" || true
  quarantined=$((quarantined+1))
  failed=$((failed+1))

  if [[ "$f" == */S2_script.json ]]; then
    echo "[FAIL] invalid S2_script.json quarantined; fail-closed enforced; no stub installation allowed: $f" >&2
  else
    echo "[FAIL] invalid JSON quarantined; manual fix required: $f" >&2
  fi
done < <(find projects -type f -name "*.json" -print0)

echo "[INFO] scanned=${count} quarantined=${quarantined} failed=${failed}" >&2

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi
