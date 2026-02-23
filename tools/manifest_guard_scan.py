#!/usr/bin/env python3
"""
FlowMind — Manifest Guard Scan (production-grade)

Goal:
- FAIL if production code appears to write ExecutionManifest.json directly
  (bypassing tools/json_write_locked.sh).

Important:
- Ignores tools/ entirely (dev utilities may contain examples/patterns)
- Ignores comments + docstrings using tokenize (avoids false positives)

Usage:
  python3 tools/manifest_guard_scan.py
Exit:
  0 = ok
  2 = suspects found
"""

from __future__ import annotations

import io
import re
import sys
import tokenize
from pathlib import Path
from typing import Iterable, List, Tuple

REPO = Path(__file__).resolve().parents[1]
MANIFEST = "ExecutionManifest.json"

# ---- Scan scope ----
# We scan "production" Python code only; exclude tools/ to avoid dev false positives.
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "tmp",
    "_ARCHIVE",
    "_ARCHIVE_FULL_SYSTEM",
    "_legacy",
    "tools",  # intentionally excluded
}

INCLUDE_ROOTS = [
    REPO / "dispatcher",
    REPO / "manifest_engine",
    REPO / "engine",
    REPO / "intelligence",
]

# ---- Suspicion patterns (code-only, comments removed) ----
# Direct write via open(...,"w"/"a") with manifest path involved.
RE_OPEN_WRITE = re.compile(
    r"""open\(\s*[^)]*ExecutionManifest\.json[^)]*,\s*["']([wa])""",
    re.IGNORECASE,
)

# Path(...).write_text / write_bytes on manifest path
RE_PATH_WRITE = re.compile(
    r"""ExecutionManifest\.json[^;\n]*\.(write_text|write_bytes)\s*\(""",
    re.IGNORECASE,
)

# json.dump(..., fp) where fp is created by open(...,'w') inline:
RE_JSON_DUMP_INLINE_OPEN = re.compile(
    r"""json\.dump\([^)]*,\s*open\(\s*[^)]*ExecutionManifest\.json[^)]*,\s*["']([wa])""",
    re.IGNORECASE,
)

# Any explicit mention of "ExecutionManifest.json" + writey keywords nearby (fallback heuristic)
RE_NEAR_WRITEY = re.compile(
    r"""ExecutionManifest\.json""",
    re.IGNORECASE,
)

RE_WRITEY_HINT = re.compile(
    r"""\b(open\s*\(|write_text\s*\(|write_bytes\s*\(|dump\s*\()\b""",
    re.IGNORECASE,
)

def iter_py_files() -> Iterable[Path]:
    for root in INCLUDE_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.py"):
            rel_parts = p.relative_to(REPO).parts
            if any(part in EXCLUDE_DIRS for part in rel_parts):
                continue
            yield p

def strip_comments_and_docstrings(py_text: str) -> str:
    """
    Return code-only text:
    - Removes COMMENT tokens
    - Removes likely docstrings (STRING tokens that appear right after INDENT or at BOF)
    Note: We keep normal string literals used in code.
    """
    out: List[str] = []
    g = tokenize.generate_tokens(io.StringIO(py_text).readline)

    prev_toktype = tokenize.INDENT
    first_token = True

    for tok in g:
        toktype = tok.type
        tokstr = tok.string

        if toktype == tokenize.COMMENT:
            continue

        if toktype == tokenize.STRING:
            # Heuristic docstring removal:
            # - First statement in module
            # - First statement after indent (function/class docstring)
            if first_token or prev_toktype == tokenize.INDENT:
                # drop docstring
                prev_toktype = toktype
                first_token = False
                continue

        if toktype in (tokenize.NL, tokenize.NEWLINE):
            out.append("\n")
        else:
            out.append(tokstr)

        prev_toktype = toktype
        first_token = False

    return "".join(out)

def find_suspects(code_only: str) -> List[Tuple[int, str]]:
    """
    Returns list of (line_number, reason_line_excerpt).
    We map back to original code-only lines.
    """
    suspects: List[Tuple[int, str]] = []
    lines = code_only.splitlines()

    for i, line in enumerate(lines, start=1):
        if "ExecutionManifest.json" not in line:
            continue

        # Strong signals:
        if RE_OPEN_WRITE.search(line) or RE_PATH_WRITE.search(line) or RE_JSON_DUMP_INLINE_OPEN.search(line):
            suspects.append((i, line.strip()))
            continue

        # Weak signal: mention + write-ish token on same line
        if RE_NEAR_WRITEY.search(line) and RE_WRITEY_HINT.search(line):
            suspects.append((i, line.strip()))
            continue

        # Weak-ish: mention manifest and next few lines include open/write/dump
        window = "\n".join(lines[i - 1 : min(i + 3, len(lines))])
        if RE_NEAR_WRITEY.search(window) and RE_WRITEY_HINT.search(window) and (
            "json_write_locked.sh" not in window and "json_write_locked" not in window
        ):
            suspects.append((i, line.strip()))
            continue

    return suspects

def main() -> int:
    checked = 0
    total_suspects = 0

    for p in iter_py_files():
        checked += 1
        try:
            raw = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[WARN] cannot read: {p}: {e}", file=sys.stderr)
            continue

        code_only = strip_comments_and_docstrings(raw)
        suspects = find_suspects(code_only)
        if suspects:
            total_suspects += len(suspects)
            rel = p.relative_to(REPO)
            for (ln, excerpt) in suspects:
                print(f"[FAIL] direct manifest WRITE suspected: {rel}:{ln}", file=sys.stderr)
                print(f"       {excerpt}", file=sys.stderr)

    if total_suspects:
        print(f"[ERR] manifest guard failed: suspects={total_suspects} checked_files={checked}", file=sys.stderr)
        return 2

    print(f"[OK] manifest guard passed: checked_files={checked}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
