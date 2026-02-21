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

LOUDNESS_TARGET = -14  # YouTube standard LUFS

def main():
    if len(sys.argv) < 2:
        cprint("Usage: runner.py <PROJECT_ID>", Color.YELLOW)
        sys.exit(1)

    project_id = sys.argv[1]
    project_path = Path("projects") / project_id
    s5_path = project_path / "S5_assets.json"

    if not s5_path.exists():
        cprint("[ERROR] Missing S5_assets.json dependency", Color.RED)
        sys.exit(1)

    with open(s5_path) as f:
        s5 = json.load(f)

    assets = s5.get("required_assets", [])

    if "voice_track.wav" not in assets:
        cprint("[ERROR] voice_track.wav missing — audio gate failed", Color.RED)
        sys.exit(1)

    output = {
        "project_id": project_id,
        "phase": "S7",
        "audio_version": 1,
        "loudness_target_lufs": LOUDNESS_TARGET,
        "ducking_enabled": True,
        "voice_track_verified": True,
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S7_audio.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S7 OK] Audio contract created for {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
