#!/usr/bin/env bash
set -euo pipefail

FILE="/home/admi/FlowMind_2026/FLOWMIND_CANONICAL_MAP.md"

echo "[CHECK] file: $FILE"

if [ ! -f "$FILE" ]; then
  echo "[FAIL] file not found"
  exit 1
fi

if [ ! -s "$FILE" ]; then
  echo "[FAIL] file is empty"
  exit 1
fi

LINES=$(wc -l < "$FILE")
LINES=$(echo "$LINES" | tr -d '[:space:]')

echo "[INFO] wc -l: $LINES"

if [ "$LINES" -lt 80 ]; then
  echo "[FAIL] file too short: $LINES lines"
  exit 1
fi

echo "[INFO] required sections:"
grep -n "## 2. ГОЛОВНИЙ ВИСНОВОК\|## 3. ЖИВЕ ЯДРО\|## 4. PRODUCTION-LAYER\|## 5. ENGINE-LAYER\|## 6. CASHFLOW-LAYER\|## 8. НЕ ПІДТВЕРДЖЕНО\|## 9. ПОТОЧНА ПОЗИЦІЯ\|## 10. ГОЛОВНЕ ПРАВИЛО НАДАЛІ" "$FILE"

echo "[INFO] first 5 lines:"
sed -n '1,5p' "$FILE"

echo "[INFO] last 5 lines:"
tail -5 "$FILE"

echo "[OK] canonical map validation passed"
