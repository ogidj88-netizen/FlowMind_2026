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

REQUIRED_VIDEO_SPEC = {
    "resolution": "1920x1080",
    "fps": 30,
    "codec": "libx264",
    "pixel_format": "yuv420p"
}

def main():
    if len(sys.argv) < 2:
        cprint("Usage: runner.py <PROJECT_ID>", Color.YELLOW)
        sys.exit(1)

    project_id = sys.argv[1]
    project_path = Path("projects") / project_id

    s8_path = project_path / "S8_assembly.json"
    s9_path = project_path / "S9_thumbnail.json"

    if not s8_path.exists():
        cprint("[ERROR] Missing S8_assembly.json", Color.RED)
        sys.exit(1)

    if not s9_path.exists():
        cprint("[ERROR] Missing S9_thumbnail.json", Color.RED)
        sys.exit(1)

    with open(s8_path) as f:
        s8 = json.load(f)

    with open(s9_path) as f:
        s9 = json.load(f)

    video_spec = s8.get("video_spec", {})
    for key, value in REQUIRED_VIDEO_SPEC.items():
        if video_spec.get(key) != value:
            cprint(f"[ERROR] Video spec mismatch: {key}", Color.RED)
            sys.exit(1)

    variants = s9.get("variants", {})
    if "A" not in variants or "B" not in variants:
        cprint("[ERROR] Thumbnail A/B structure invalid", Color.RED)
        sys.exit(1)

    output = {
        "project_id": project_id,
        "phase": "S10",
        "qa_version": 1,
        "status": "PASSED",
        "checked_modules": ["S8", "S9"],
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S10_qa.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S10 OK] QA PASSED for {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
