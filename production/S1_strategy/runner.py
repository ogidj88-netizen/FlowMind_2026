#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from datetime import datetime, UTC

class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def cprint(msg, color):
    print(color + msg + Color.RESET)

def main():
    if len(sys.argv) < 2:
        cprint("Usage: runner.py <PROJECT_ID>", Color.YELLOW)
        sys.exit(1)

    project_id = sys.argv[1]
    project_path = Path("projects") / project_id

    if not project_path.exists():
        cprint(f"[ERROR] Project {project_id} not found.", Color.RED)
        sys.exit(1)

    output = {
        "project_id": project_id,
        "phase": "S1",
        "strategy_version": 1,
        "hook": "Why Most People Stay Broke",
        "thumbnail_angle": "Shock + Fear of Loss",
        "core_conflict": "Daily invisible financial mistakes",
        "target_emotion": "Anxiety",
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S1_strategy.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S1 RESTORED] {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
