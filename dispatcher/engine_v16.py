#!/usr/bin/env python3
"""
FlowMind 2026
DISPATCHER ENGINE v16.5-FINAL
Deterministic phase map + manifest safety
"""

import sys
import subprocess
from manifest_engine.engine import load_manifest, update_phase

DISPATCHER_VERSION = "16.5-FINAL"
DISPATCHER_BOOT_MARKER = "FLOWMIND_DISPATCHER_OK"

PHASE_MAP = {
    ("CREATED", "S1_DONE"): "engine/modules/s1_strategy.py",
    ("S1_DONE", "S2_DONE"): "engine/modules/s2_script.py",
}


def run_module(module_path, project_id):
    print(f"[MODULE RUNNER] Executing {module_path} for {project_id}")
    result = subprocess.run(["python3", module_path, project_id])
    if result.returncode != 0:
        print("[ERROR] Module execution failed")
        sys.exit(1)


def parse_args():
    if len(sys.argv) != 4:
        print("Usage: python3 engine_v16.py <PROJECT_ID> --advance <PHASE>")
        sys.exit(1)

    project_id = sys.argv[1]
    flag = sys.argv[2]
    next_phase = sys.argv[3]

    if flag != "--advance":
        print("[ERROR] Missing --advance flag")
        sys.exit(1)

    return project_id, next_phase


def main():
    print(f"[DISPATCHER BOOT] {DISPATCHER_VERSION}")
    print(f"[MARKER] {DISPATCHER_BOOT_MARKER}")

    project_id, next_phase = parse_args()

    manifest = load_manifest(project_id)

    if not isinstance(manifest, dict):
        print("[ERROR] Manifest is invalid")
        sys.exit(1)

    if "current_phase" not in manifest:
        print("[ERROR] Manifest missing current_phase")
        sys.exit(1)

    current_phase = manifest["current_phase"]

    transition_key = (current_phase, next_phase)

    if transition_key not in PHASE_MAP:
        print("[ERROR] Illegal phase transition")
        sys.exit(1)

    module_path = PHASE_MAP[transition_key]

    run_module(module_path, project_id)
    update_phase(project_id, next_phase)

    print(f"[OK] Transition {current_phase} → {next_phase}")


if __name__ == "__main__":
    main()
