#!/usr/bin/env python3
"""
FlowMind 2026 — Contract Validation Engine v1 (No-Dependency)
Deterministic schema validation for S1–S10
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# ===== COLOR =====
class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

def cprint(msg, color):
    print(color + msg + Color.RESET)

PROJECTS_DIR = Path("projects")

PHASE_TO_FILE = {
    "S1": "S1_strategy.json",
    "S2": "S2_script.json",
    "S5": "S5_assets.json",
    "S6": "S6_visual.json",
    "S7": "S7_audio.json",
    "S8": "S8_assembly.json",
    "S9": "S9_thumbnail.json",
    "S10": "S10_qa.json",
}

def load_phase_json(project_id: str, phase: str):
    if phase not in PHASE_TO_FILE:
        raise ValueError(f"Unknown phase '{phase}'")

    path = PROJECTS_DIR / project_id / PHASE_TO_FILE[phase]

    if not path.exists():
        raise FileNotFoundError(f"Missing output file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


# ===== Minimal deterministic validation =====

def require_fields(obj, required):
    errors = []
    for k in required:
        if k not in obj:
            errors.append(f"Missing required field '{k}'")
    return errors

def validate_s1(obj):
    required = [
        "project_id",
        "phase",
        "strategy_version",
        "hook",
        "thumbnail_angle",
        "core_conflict",
        "target_emotion",
        "created_at",
    ]
    return require_fields(obj, required)

def validate_s2(obj):
    required = [
        "project_id",
        "phase",
        "script_version",
        "title",
        "intro_hook",
        "body_outline",
        "ending",
        "created_at",
    ]
    return require_fields(obj, required)

VALIDATORS = {
    "S1": validate_s1,
    "S2": validate_s2,
}

def validate_phase(project_id: str, phase: str):
    obj, path = load_phase_json(project_id, phase)

    if phase not in VALIDATORS:
        return [], path

    errors = VALIDATORS[phase](obj)
    return errors, path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--phase", required=True)
    args = parser.parse_args()

    phase = args.phase.upper()

    try:
        errors, path = validate_phase(args.project, phase)
    except Exception as e:
        cprint(f"[ERROR] {e}", Color.RED)
        sys.exit(1)

    if errors:
        cprint(f"[FAIL] {args.project} {phase} contract invalid:", Color.RED)
        for err in errors:
            cprint(f" - {err}", Color.RED)
        sys.exit(2)

    cprint(f"[PASS] {args.project} {phase} contract valid: {path}", Color.GREEN)
    sys.exit(0)


if __name__ == "__main__":
    main()
