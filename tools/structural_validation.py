#!/usr/bin/env python3
"""
FlowMind 2026
Structural Validator v2
Supports S1 and S2
"""

import sys
import json
from pathlib import Path


PROJECTS_DIR = Path("projects")


def validate_s1(project_id):
    path = PROJECTS_DIR / project_id / "S1_strategy.json"

    if not path.exists():
        print("[FAIL] S1_strategy.json missing.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required = ["project_id", "phase", "niche", "strategy_version"]

    missing = [r for r in required if r not in data]

    if missing:
        print("[FAIL] Missing required fields:")
        for m in missing:
            print(" -", m)
        return False

    print("[PASS] S1 contract valid")
    return True


def validate_s2(project_id):
    path = PROJECTS_DIR / project_id / "S2_script.json"

    if not path.exists():
        print("[FAIL] S2_script.json missing.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required = ["project_id", "phase", "based_on_strategy"]

    missing = [r for r in required if r not in data]

    if missing:
        print("[FAIL] Missing required fields:")
        for m in missing:
            print(" -", m)
        return False

    print("[PASS] S2 contract valid")
    return True


def main():
    if len(sys.argv) != 4:
        sys.exit(1)

    project_id = sys.argv[1]
    phase = sys.argv[3]

    if phase == "S1":
        ok = validate_s1(project_id)
    elif phase == "S2":
        ok = validate_s2(project_id)
    else:
        print("[ERROR] Phase not supported yet")
        sys.exit(1)

    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
