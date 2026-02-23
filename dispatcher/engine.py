#!/usr/bin/env python3
"""
FlowMind 2026
Dispatcher v15
Strict Order
Structural Validation
Semantic Cross-Phase Validation
Artifact Registry
"""

import json
import sys
import subprocess
import hashlib
from pathlib import Path

# === Single-writer enforcement (ExecutionManifest.json) ===
from pathlib import Path as _Path

def _fm_write_json_locked(path: _Path, manifest_obj) -> None:
    """
    Write JSON ONLY via tools/json_write_locked.sh (atomic + locked).
    """
    import json as _json
    import subprocess as _subprocess

    tools_dir = _Path(__file__).resolve().parents[1] / "tools"
    writer = tools_dir / "json_write_locked.sh"
    if not writer.exists():
        raise RuntimeError(f"locked writer missing: {writer}")

    data = _json.dumps(manifest_obj, ensure_ascii=False, indent=2) + "\n"
    proc = _subprocess.run(
        [str(writer), str(path)],
        input=data.encode("utf-8"),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip())


PROJECTS_DIR = Path("projects")
MANIFEST_NAME = "ExecutionManifest.json"

class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def cprint(msg, color):
    print(color + msg + Color.RESET)

PHASE_ORDER = [
    "CREATED",
    "S1_DONE",
    "S2_DONE",
    "S5_DONE",
    "S6_DONE",
    "S7_DONE",
    "S8_DONE",
    "S9_DONE",
    "S10_DONE",
]

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

# ================= Manifest =================

def load_manifest(project_id):
    path = PROJECTS_DIR / project_id / MANIFEST_NAME
    if not path.exists():
        cprint("[ERROR] Manifest not found.", Color.RED)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def save_manifest(manifest, path):
    # Single-writer enforcement: no direct open(...,'w')
    _fm_write_json_locked(Path(path), manifest)

