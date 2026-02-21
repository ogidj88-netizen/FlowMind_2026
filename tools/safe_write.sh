#!/usr/bin/env bash

TARGET="$1"

if [ -z "$TARGET" ]; then
  echo "Usage: safe_write.sh <target_file>"
  exit 1
fi

cat > /tmp/_fm_tmp_base64.txt
base64 -d /tmp/_fm_tmp_base64.txt > "$TARGET"
rm /tmp/_fm_tmp_base64.txt

echo "[SAFE WRITE] Written to $TARGET"
