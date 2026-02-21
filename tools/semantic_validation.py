#!/usr/bin/env python3
"""
FlowMind 2026
Semantic Validator v2 (Real Cross-Phase)
"""

import sys
import json
from pathlib import Path


PROJECTS_DIR = Path("projects")


def validate_s2(project_id):
    project_dir = PROJECTS_DIR / project_id

    s1_path = project_dir / "S1_strategy.json"
    s2_path = project_dir / "S2_script.json"

    if not s1_path.exists():
        print("[FAIL] S1_strategy.json missing.")
        return False

    if not s2_path.exists():
        print("[FAIL] S2_script.json missing.")
        return False

    with open(s1_path, "r", encoding="utf-8") as f:
        s1 = json.load(f)

    with open(s2_path, "r", encoding="utf-8") as f:
        s2 = json.load(f)

    errors = []

    if s2.get("based_on_niche") != s1.get("niche"):
        errors.append("based_on_niche mismatch")

    if s2.get("strategy_version") != s1.get("strategy_version"):
        errors.append("strategy_version mismatch")

    if errors:
        print("[SEMANTIC FAIL]")
        for e in errors:
            print(" -", e)
        return False

    print("[SEMANTIC PASS]")
    return True


def main():
    if len(sys.argv) != 4:
        sys.exit(1)

    project_id = sys.argv[1]
    phase = sys.argv[3]

    if phase == "S2":
        if validate_s2(project_id):
            sys.exit(0)
        else:
            sys.exit(2)

    sys.exit(1)


if __name__ == "__main__":
    main()
