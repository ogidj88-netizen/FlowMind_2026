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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def ensure_registry(manifest):
    if "artifact_registry" not in manifest:
        manifest["artifact_registry"] = {}


# ================= Phase Logic =================

def check_phase_order(current_status, next_status):
    return PHASE_ORDER.index(next_status) == PHASE_ORDER.index(current_status) + 1


def phase_from_status(status):
    if status.endswith("_DONE"):
        return status.replace("_DONE", "")
    return None


# ================= Validation =================

def run_structural_validation(project_id, phase):
    cmd = [
        "python3",
        "tools/contract_validation.py",
        "--project",
        project_id,
        "--phase",
        phase,
    ]
    return subprocess.run(cmd).returncode == 0


def run_semantic_validation(project_id, phase):
    cmd = [
        "python3",
        "tools/semantic_validation.py",
        project_id,
        phase,
    ]
    return subprocess.run(cmd).returncode == 0


# ================= Hash =================

def compute_hash(project_id, phase):
    filename = PHASE_TO_FILE[phase]
    path = PROJECTS_DIR / project_id / filename

    if not path.exists():
        cprint(f"[ERROR] Missing artifact file: {path}", Color.RED)
        sys.exit(2)

    with open(path, "rb") as f:
        data = f.read()

    return hashlib.sha256(data).hexdigest()


# ================= Advance =================

def advance(project_id, next_status):
    manifest, manifest_path = load_manifest(project_id)
    current_status = manifest["status"]

    if not check_phase_order(current_status, next_status):
        cprint(f"[ERROR] Illegal phase order: {current_status} → {next_status}", Color.RED)
        sys.exit(1)

    phase = phase_from_status(next_status)

    if phase:

        # Structural validation
        cprint(f"[STRUCTURAL VALIDATION] {phase}", Color.YELLOW)
        if not run_structural_validation(project_id, phase):
            cprint("[ERROR] Structural validation FAILED.", Color.RED)
            sys.exit(2)
        cprint("[STRUCTURAL PASS]", Color.GREEN)

        # Semantic validation
        cprint(f"[SEMANTIC VALIDATION] {phase}", Color.YELLOW)
        if not run_semantic_validation(project_id, phase):
            cprint("[ERROR] Semantic validation FAILED.", Color.RED)
            sys.exit(3)
        cprint("[SEMANTIC PASS]", Color.GREEN)

        # Artifact Registry
        ensure_registry(manifest)
        artifact_hash = compute_hash(project_id, phase)

        previous_hash = manifest["artifact_registry"].get(phase)

        if previous_hash and previous_hash != artifact_hash:
            cprint("[ERROR] Artifact hash mismatch! Mutation detected.", Color.RED)
            sys.exit(4)

        manifest["artifact_registry"][phase] = artifact_hash
        cprint(f"[REGISTRY] Hash stored for {phase}", Color.GREEN)

    manifest["status"] = next_status
    save_manifest(manifest, manifest_path)

    cprint(f"[OK] Transition {current_status} → {next_status}", Color.GREEN)


# ================= Main =================

def main():
    if len(sys.argv) < 4:
        cprint("Usage: engine.py <PROJECT_ID> --advance <STATUS>", Color.RED)
        sys.exit(1)

    project_id = sys.argv[1]
    command = sys.argv[2]
    value = sys.argv[3]

    if command == "--advance":
        advance(project_id, value)
    else:
        cprint("[ERROR] Unknown command.", Color.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()
