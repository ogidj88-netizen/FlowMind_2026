#!/usr/bin/env python3
import sys
import subprocess

PHASE_TO_MODULE = {
    "S1": "engine/modules/s1_strategy.py",
    "S2": "engine/modules/s2_script.py"
}


def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    project_id = sys.argv[1]
    phase = sys.argv[2]

    module_path = PHASE_TO_MODULE.get(phase)

    if not module_path:
        print(f"[ERROR] Unknown phase: {phase}")
        sys.exit(2)

    print(f"[MODULE RUNNER] Executing {module_path} for {project_id}")

    result = subprocess.run(["python3", module_path, project_id])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
