#!/usr/bin/env python3
"""
FlowMind — Manifest Writer (Single-Writer)
Writes JSON via tools/json_write_locked.sh to guarantee:
- atomic write
- valid JSON
- consistent formatting
- deny writing outside repo unintentionally (best-effort)

Usage:
  python3 tools/manifest_write.py <path-to-manifest> <json-string>
  python3 tools/manifest_write.py <path-to-manifest> --from-file <json-file>
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    # best-effort: assume this file lives in <repo>/tools/
    return Path(__file__).resolve().parents[1]


def _fail(msg: str, code: int = 2) -> None:
    print(f"[ERR] {msg}", file=sys.stderr)
    raise SystemExit(code)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="Path to ExecutionManifest.json (or other JSON) to write")
    ap.add_argument("json_string", nargs="?", help="JSON string to write (ignored if --from-file used)")
    ap.add_argument("--from-file", dest="from_file", default="", help="Read JSON from this file instead of argument")
    args = ap.parse_args()

    repo = _repo_root()
    target = Path(args.target).expanduser()
    if not target.is_absolute():
        target = (repo / target).resolve()

    # Safety: target must be inside repo
    try:
        target.relative_to(repo)
    except Exception:
        _fail(f"Refusing to write outside repo. target={target} repo={repo}")

    writer = repo / "tools" / "json_write_locked.sh"
    if not writer.exists():
        _fail(f"writer not found: {writer}")

    if args.from_file:
        src = Path(args.from_file).expanduser()
        if not src.is_absolute():
            src = (repo / src).resolve()
        if not src.exists():
            _fail(f"--from-file not found: {src}")
        data = src.read_text(encoding="utf-8")
    else:
        if args.json_string is None:
            _fail("Provide json_string or use --from-file")
        data = args.json_string

    # Call locked writer, pass JSON via stdin
    proc = subprocess.run(
        [str(writer), str(target)],
        input=data.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))
        _fail("manifest write failed", code=proc.returncode)
    sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
