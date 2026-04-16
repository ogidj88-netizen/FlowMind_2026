#!/usr/bin/env python3
import subprocess
import sys

PHASE_TO_MODULE = {
    "TOPIC": "engine/modules/s1_strategy.py",
    "SCRIPT": "engine/modules/s2_script.py",
}


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python engine/module_runner.py <PROJECT_ID> <PHASE>", file=sys.stderr)
        sys.exit(1)

    project_id = sys.argv[1]
    phase = sys.argv[2].strip().upper()

    module_path = PHASE_TO_MODULE.get(phase)

    if not module_path:
        print(f"[ERROR] No execution module mapped for phase: {phase}", file=sys.stderr)
        sys.exit(2)

    print(f"[MODULE RUNNER] Executing {module_path} for {project_id}")

    result = subprocess.run(["python3", module_path, project_id])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
