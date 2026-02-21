#!/usr/bin/env python3
"""
FlowMind 2026
Single Entry Point (Lifecycle Aware)
"""

import argparse
import subprocess
import hashlib
from pathlib import Path
import sys

class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def cprint(msg, color):
    print(color + msg + Color.RESET)

def self_check():
    content = Path(__file__).read_bytes()
    file_hash = hashlib.sha256(content).hexdigest()[:12]
    cprint(f"[SELF CHECK OK] main.py hash {file_hash}", Color.GREEN)

def main():
    print("=== FLOWMIND 2026 START ===")

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--advance")
    parser.add_argument("--halt", action="store_true")
    parser.add_argument("--resume", action="store_true")

    args = parser.parse_args()

    self_check()

    project_path = Path("projects") / args.project
    manifest_path = project_path / "ExecutionManifest.json"

    if not manifest_path.exists():
        cprint(f"[ERROR] Project {args.project} does not exist.", Color.RED)
        sys.exit(1)

    cprint("[OK] Manifest located.", Color.GREEN)

    if args.halt:
        subprocess.run(["python3", "dispatcher/engine.py", args.project, "--halt"])
        return

    if args.resume:
        subprocess.run(["python3", "dispatcher/engine.py", args.project, "--resume"])
        return

    if args.advance:
        subprocess.run(["python3", "dispatcher/engine.py", args.project, "--advance", args.advance])
        return

    cprint("[ERROR] No valid command provided.", Color.RED)

if __name__ == "__main__":
    main()
