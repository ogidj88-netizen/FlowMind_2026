#!/usr/bin/env python3

import sys
import py_compile
from pathlib import Path

# ===== COLOR SYSTEM =====
class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def cprint(message, color):
    print(color + message + Color.RESET)

def check_file(file_path):
    try:
        py_compile.compile(file_path, doraise=True)
        cprint(f"[OK] {file_path} syntax valid", Color.GREEN)
        return True
    except py_compile.PyCompileError as e:
        cprint(f"[ERROR] {file_path}", Color.RED)
        print(e)
        return False

def main():
    if len(sys.argv) < 2:
        cprint("Usage: python3 tools/code_check.py <file_or_folder>", Color.YELLOW)
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        check_file(target)
    elif target.is_dir():
        for file in target.rglob("*.py"):
            check_file(file)
    else:
        cprint("Invalid path.", Color.RED)

if __name__ == "__main__":
    main()
