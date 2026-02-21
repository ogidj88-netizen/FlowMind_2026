#!/usr/bin/env python3
"""
FlowMind 2026
DISPATCHER ENGINE v16.2-MANIFEST
Stable Core with Manifest + Boot Marker
"""

import sys
import subprocess
from manifest_engine.engine import load_manifest, update_phase

DISPATCHER_VERSION = "16.2-MANIFEST"
DISPATCHER_BOOT_MARKER = "FLOWMIND_DISPATCHER_OK"

def run_module(module_path, project_id):
    print(f"[MODULE RUNNER] Executing {module_path} for {project_id}")
    result = subprocess.run(["python3", module_path, project_id])
    if result.returncode != 0:
        print("[ERROR] Module execution failed")
        sys.exit(1)

def main():
    print(f"[DISPATCHER BOOT] {DISPATCHER_VERSION}")
    print(f"[MARKER] {DISPATCHER_BOOT_MARKER}")

    if len(sys.argv) < 4:
        print("Usage: python3 engine_v16.py <PROJECT_ID> --advance <PHASE>")
        sys.exit(0)

    project_id = sys.argv[1]
    next_phase = sys.argv[3]

    manifest = load_manifest(project_id)
    current_phase = manifest["current_phase"]

    if current_phase == "CREATED" and next_phase == "S1_DONE":
        run_module("engine/modules/s1_strategy.py", project_id)
        update_phase(project_id, "S1_DONE")
        print("[OK] Transition CREATED → S1_DONE")
        return

    if current_phase == "S1_DONE" and next_phase == "S2_DONE":
        run_module("engine/modules/s2_script.py", project_id)
        update_phase(project_id, "S2_DONE")
        print("[OK] Transition S1_DONE → S2_DONE")
        return

    print("[ERROR] Illegal phase order")
    sys.exit(1)

if __name__ == "__main__":
    main()
