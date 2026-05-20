#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.state_validator import StateValidationError, load_state


PHASE_TO_EXECUTOR: dict[str, str] = {
    "SCRIPT": "engine/executors/script_executor.py",
    "SCENES": "engine/executors/scenes_executor.py",
    "ASSETS": "engine/executors/assets_executor.py",
    "ASSEMBLY": "engine/executors/assembly_executor.py",
    "AUDIO": "engine/executors/audio_executor.py",
}


FORBIDDEN_EXECUTOR_FRAGMENTS = (
    "engine/module_runner.py",
    "engine/modules/",
)


class FlowMindRunPhaseError(RuntimeError):
    """Raised when the active phase runner cannot safely run."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FlowMind minimal active phase runner v1"
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to canonical PROJECT_STATE.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the executor command without running it",
    )
    return parser


def resolve_python_bin() -> str:
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def resolve_executor_for_phase(phase: str) -> Path:
    executor_value = PHASE_TO_EXECUTOR.get(phase)
    if not executor_value:
        raise FlowMindRunPhaseError(
            f"No active executor mapped for phase '{phase}'. "
            "This runner v1 supports only SCRIPT, SCENES, ASSETS, ASSEMBLY, AUDIO."
        )

    if any(fragment in executor_value for fragment in FORBIDDEN_EXECUTOR_FRAGMENTS):
        raise FlowMindRunPhaseError(
            f"Forbidden executor path resolved for phase '{phase}': {executor_value}"
        )

    executor_path = REPO_ROOT / executor_value
    if not executor_path.is_file():
        raise FlowMindRunPhaseError(f"Executor file not found: {executor_path}")

    return executor_path


def build_executor_command(state_path: Path, executor_path: Path) -> list[str]:
    python_bin = resolve_python_bin()
    return [
        python_bin,
        str(executor_path.relative_to(REPO_ROOT)),
        "--state",
        str(state_path),
    ]


def run_phase(state_path: Path, dry_run: bool = False) -> int:
    if not state_path.is_file():
        raise FlowMindRunPhaseError(f"State file not found: {state_path}")

    try:
        state = load_state(state_path)
    except StateValidationError as exc:
        raise FlowMindRunPhaseError(f"Invalid PROJECT_STATE: {exc}") from exc

    phase = str(state.get("phase", "")).strip().upper()

    if phase == "HALT":
        raise FlowMindRunPhaseError("Refusing to run while PROJECT_STATE.phase is HALT")

    if phase in {"QA", "READY_FOR_UPLOAD", "UPLOADED", "ARCHIVED"}:
        raise FlowMindRunPhaseError(
            f"Runner v1 refuses phase '{phase}'. "
            "QA-compatible tools and upload/archive phases require explicit commands."
        )

    executor_path = resolve_executor_for_phase(phase)
    command = build_executor_command(state_path, executor_path)

    print("[FLOWMIND_RUN_PHASE] phase=", phase)
    print("[FLOWMIND_RUN_PHASE] executor=", executor_path.relative_to(REPO_ROOT))
    print("[FLOWMIND_RUN_PHASE] command=", " ".join(command))

    if dry_run:
        print("[FLOWMIND_RUN_PHASE] dry_run=true")
        return 0

    result = subprocess.run(command, cwd=REPO_ROOT)
    return int(result.returncode)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        exit_code = run_phase(Path(args.state), dry_run=bool(args.dry_run))
    except FlowMindRunPhaseError as exc:
        print(f"FLOWMIND_RUN_PHASE_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
