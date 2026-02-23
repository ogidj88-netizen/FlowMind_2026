#!/usr/bin/env bash
set -euo pipefail

# FlowMind JSON AutoFix (limited)
# - Scans projects/**.json
# - If invalid JSON:
#   - If file ends with /S2_script.json -> quarantine invalid + install stub
#   - Else -> quarantine invalid and FAIL (manual action required)
#
# Usage:
#   tools/json_autofix_s2_or_quarantine.sh

if [[ ! -x "tools/json_repair_or_quarantine.sh" ]]; then
  echo "[ERR] missing or not executable: tools/json_repair_or_quarantine.sh" >&2
  exit 2
fi

if [[ ! -f "tools/stub_s2_script_v1.json" ]]; then
  echo "[ERR] missing: tools/stub_s2_script_v1.json" >&2
  exit 2
fi

if [[ ! -d "projects" ]]; then
  echo "[WARN] no projects/ folder; nothing to scan" >&2
  exit 0
fi

count=0
fixed=0
quarantined=0
failed=0

while IFS= read -r -d '' f; do
  count=$((count+1))

  if python3 -m json.tool "$f" >/dev/null 2>&1; then
    continue
  fi

  echo "[WARN] invalid JSON detected: $f" >&2

  if [[ "$f" == */S2_script.json ]]; then
    # quarantine invalid
    tools/json_repair_or_quarantine.sh "$f" || true
    # install stub
    cp -f tools/stub_s2_script_v1.json "$f"
    echo "[OK] stub installed: $f" >&2
    fixed=$((fixed+1))
  else
    tools/json_repair_or_quarantine.sh "$f" || true
    quarantined=$((quarantined+1))
    echo "[FAIL] quarantined non-S2 invalid JSON (manual fix required): $f" >&2
    failed=$((failed+1))
  fi
done < <(find projects -type f -name "*.json" -print0)

echo "[INFO] scanned=${count} fixed_S2=${fixed} quarantined_other=${quarantined} failed=${failed}" >&2

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi
