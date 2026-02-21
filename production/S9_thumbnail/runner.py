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

    s1_path = project_path / "S1_strategy.json"
    s8_path = project_path / "S8_assembly.json"

    # ===== DEPENDENCY CHECK =====
    if not s1_path.exists():
        cprint("[ERROR] Missing S1_strategy.json dependency", Color.RED)
        sys.exit(1)

    if not s8_path.exists():
        cprint("[ERROR] Missing S8_assembly.json dependency", Color.RED)
        sys.exit(1)

    with open(s1_path) as f:
        s1 = json.load(f)

    angle = s1.get("thumbnail_angle")
    emotion = s1.get("target_emotion")

    if not angle:
        cprint("[ERROR] thumbnail_angle missing — thumbnail gate blocked", Color.RED)
        sys.exit(1)

    # ===== A/B Thumbnail Contract =====
    output = {
        "project_id": project_id,
        "phase": "S9",
        "thumbnail_version": 1,
        "variants": {
            "A": {
                "angle": angle,
                "emotion_trigger": emotion,
                "style": "high contrast, large text"
            },
            "B": {
                "angle": angle + " (alt)",
                "emotion_trigger": emotion,
                "style": "minimal text, face close-up"
            }
        },
        "ab_testing_enabled": True,
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S9_thumbnail.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S9 OK] Thumbnail contract created for {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
