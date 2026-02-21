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

# ===== FFmpeg Stability Standard v1.2 =====
VIDEO_SPEC = {
    "resolution": "1920x1080",
    "fps": 30,
    "codec": "libx264",
    "pixel_format": "yuv420p",
    "audio_codec": "aac",
    "audio_rate": "48kHz",
    "movflags": "+faststart",
    "sar": 1,
    "threads": 2
}

def main():
    if len(sys.argv) < 2:
        cprint("Usage: runner.py <PROJECT_ID>", Color.YELLOW)
        sys.exit(1)

    project_id = sys.argv[1]
    project_path = Path("projects") / project_id

    s6_path = project_path / "S6_visual.json"
    s7_path = project_path / "S7_audio.json"

    # ===== DEPENDENCY CHECK =====
    if not s6_path.exists():
        cprint("[ERROR] Missing S6_visual.json dependency", Color.RED)
        sys.exit(1)

    if not s7_path.exists():
        cprint("[ERROR] Missing S7_audio.json dependency", Color.RED)
        sys.exit(1)

    output = {
        "project_id": project_id,
        "phase": "S8",
        "assembly_version": 1,
        "video_spec": VIDEO_SPEC,
        "audio_linked": True,
        "visual_linked": True,
        "created_at": datetime.now(UTC).isoformat()
    }

    out_path = project_path / "S8_assembly.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    cprint(f"[S8 OK] Assembly contract created for {project_id}", Color.GREEN)

if __name__ == "__main__":
    main()
