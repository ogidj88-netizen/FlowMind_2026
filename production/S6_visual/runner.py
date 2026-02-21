#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from datetime import datetime, UTC

# ===== COLOR =====
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
    s5_path = project_path / "S5_assets.json"

    # ===== DEPENDENCY CHECK =====
    if not s5_path.exists():
        cprint("[ERROR] Missing S5_assets.json dependency", Color.RED)
        sys.exit(1)

    with open(s5_path) as f:
        s5 = json.load(f)

    required_assets = s5.get("required_assets", [])

    if not required_assets:
        cprint("[ERROR] required_assets is empty — anti-static rule triggered", Color.RED)
        sys.exit(1)

    # ===== ANTI-STATIC RULE =====
    visual_plan = {
        "motion_required": True,
        "min_dynamic_elements": 2,
        "static_frames_allowed": False
    }

    output = {
        "project_id": project_id,
        "phase": "S6",
        "visual_version": 1,
        "assets_used": required_assets,
        "visual_rules": visual_plan,
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S6_visual.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S6 OK] Visual contract created for {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
