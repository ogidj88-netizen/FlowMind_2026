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
    s2_path = project_path / "S2_script.json"

    # ===== DEPENDENCY CHECK =====
    if not s2_path.exists():
        cprint("[ERROR] Missing S2_script.json dependency", Color.RED)
        sys.exit(1)

    with open(s2_path) as f:
        s2 = json.load(f)

    # ===== CONTRACT STRUCTURE =====
    output = {
        "project_id": project_id,
        "phase": "S5",
        "assets_version": 1,
        "required_assets": [
            "voice_track.wav",
            "background_music.wav",
            "scene_1.mp4"
        ],
        "linked_script_title": s2.get("title"),
        "asset_strategy": "stock-first",
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S5_assets.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S5 OK] Assets contract created for {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
