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
    s1_path = project_path / "S1_strategy.json"

    if not s1_path.exists():
        cprint("[ERROR] Missing S1_strategy.json", Color.RED)
        sys.exit(1)

    with open(s1_path) as f:
        s1 = json.load(f)

    output = {
        "project_id": project_id,
        "phase": "S2",
        "script_version": 1,
        "title": s1["hook"],
        "intro_hook": s1["hook"],
        "body_outline": [
            s1["core_conflict"],
            "Hidden systems that keep you stuck",
            "How to break the pattern"
        ],
        "ending": "Awareness is the first step to freedom.",
        "based_on_strategy": True,
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S2_script.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S2 RESTORED] {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
