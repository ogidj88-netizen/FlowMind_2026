#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.state_validator import StateValidationError, load_state


RUNNER_VERSION = "2.0.0"

REFUSED_PHASES = {
    "READY_FOR_UPLOAD",
    "UPLOADED",
    "ARCHIVED",
}

FORBIDDEN_EXECUTOR_FRAGMENTS = (
    "engine/module_runner.py",
    "engine/modules/",
)

PHASE_PIPELINES: dict[str, tuple[str, ...]] = {
    "SCRIPT": (
        "engine/executors/script_executor.py",
        "engine/executors/script_qa.py",
    ),
    "SCENES": (
        "engine/executors/scenes_executor.py",
        "engine/executors/audio_executor.py",
        "engine/executors/audio_renderer.py",
        "tools/audio_loudness_report.py",
        "tools/apply_audio_loudness_report.py",
        "engine/executors/visual_pacing_executor.py",
    ),
    "ASSETS": (
        "engine/executors/assets_executor.py",
    ),
    "ASSEMBLY": (
        "engine/executors/assembly_executor.py",
        "tools/apply_assembly_readiness.py",
        "engine/executors/final_render_executor.py",
        "tools/apply_final_render_readiness.py",
    ),
    "QA": (
        "engine/executors/qa_executor.py",
    ),
}


class FlowMindRunPhaseError(RuntimeError):
    """Raised when the active phase runner cannot safely run."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"FlowMind active phase runner v{RUNNER_VERSION}"
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to canonical PROJECT_STATE.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the phase pipeline without executing it",
    )
    return parser


def resolve_python_bin() -> str:
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def repo_relative(path: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise FlowMindRunPhaseError(
            f"path must be inside repo root: {path}"
        ) from exc


def load_canonical_state(state_path: Path) -> dict[str, Any]:
    try:
        return load_state(state_path)
    except StateValidationError as exc:
        raise FlowMindRunPhaseError(f"Invalid PROJECT_STATE: {exc}") from exc


def supported_phases_message() -> str:
    supported = ", ".join(sorted(PHASE_PIPELINES))
    return f"This runner v{RUNNER_VERSION} supports only {supported}."


def resolve_pipeline_for_phase(phase: str) -> list[Path]:
    values = PHASE_PIPELINES.get(phase)
    if not values:
        raise FlowMindRunPhaseError(
            f"No active pipeline mapped for phase '{phase}'. "
            f"{supported_phases_message()}"
        )

    result: list[Path] = []
    for value in values:
        if any(fragment in value for fragment in FORBIDDEN_EXECUTOR_FRAGMENTS):
            raise FlowMindRunPhaseError(
                f"Forbidden executor path resolved for phase '{phase}': {value}"
            )

        path = REPO_ROOT / value
        if not path.is_file():
            raise FlowMindRunPhaseError(f"Runtime file not found: {path}")
        result.append(path)

    return result


def require_artifact(
    state: dict[str, Any],
    key: str,
) -> str:
    artifacts = state.get("artifacts")
    if not isinstance(artifacts, dict):
        raise FlowMindRunPhaseError("PROJECT_STATE.artifacts must be an object")

    value = artifacts.get(key)
    if not isinstance(value, str) or not value.strip():
        raise FlowMindRunPhaseError(
            f"Required artifact missing from PROJECT_STATE: artifacts.{key}"
        )
    return value.strip()


def build_simple_state_command(state_path: Path, runtime_path: Path) -> list[str]:
    return [
        resolve_python_bin(),
        str(runtime_path.relative_to(REPO_ROOT)),
        "--state",
        str(repo_relative(state_path)),
    ]


def build_command(
    *,
    phase: str,
    runtime_path: Path,
    state_path: Path,
    state: dict[str, Any],
) -> list[str]:
    relative = str(runtime_path.relative_to(REPO_ROOT))

    if relative == "tools/audio_loudness_report.py":
        audio_render = require_artifact(state, "audio_render_path")
        report_path = str(Path(audio_render).parent / "audio_loudness_report.json")
        return [
            resolve_python_bin(),
            relative,
            "--audio-render",
            audio_render,
            "--out",
            report_path,
        ]

    if relative == "tools/apply_audio_loudness_report.py":
        audio_render = require_artifact(state, "audio_render_path")
        report_path = str(Path(audio_render).parent / "audio_loudness_report.json")
        return [
            resolve_python_bin(),
            relative,
            "--state",
            str(repo_relative(state_path)),
            "--audio-render",
            audio_render,
            "--loudness-report",
            report_path,
        ]

    if relative == "tools/apply_assembly_readiness.py":
        return [
            resolve_python_bin(),
            relative,
            "--state",
            str(repo_relative(state_path)),
            "--assembly-plan",
            require_artifact(state, "assembly_plan_path"),
            "--resolved-assets",
            require_artifact(state, "resolved_assets_path"),
            "--audio-render",
            require_artifact(state, "audio_render_path"),
        ]

    if relative == "tools/apply_final_render_readiness.py":
        return [
            resolve_python_bin(),
            relative,
            "--state",
            str(repo_relative(state_path)),
            "--assembly-plan",
            require_artifact(state, "assembly_plan_path"),
            "--final-render-report",
            require_artifact(state, "final_render_report_path"),
        ]

    return build_simple_state_command(state_path, runtime_path)


def run_command(command: list[str], *, label: str) -> int:
    print(f"[FLOWMIND_RUN_PHASE] START {label}", flush=True)
    print(
        "[FLOWMIND_RUN_PHASE] command=" + " ".join(command),
        flush=True,
    )

    result = subprocess.run(command, cwd=REPO_ROOT)
    if result.returncode != 0:
        print(
            f"[FLOWMIND_RUN_PHASE] FAIL {label} exit={result.returncode}",
            file=sys.stderr,
            flush=True,
        )
        return int(result.returncode)

    print(f"[FLOWMIND_RUN_PHASE] PASS {label}", flush=True)
    return 0


def validate_phase_unchanged(
    state_path: Path,
    expected_phase: str,
    *,
    after_label: str,
) -> dict[str, Any]:
    state = load_canonical_state(state_path)
    actual_phase = str(state.get("phase", "")).strip().upper()
    if actual_phase != expected_phase:
        raise FlowMindRunPhaseError(
            f"Canonical phase changed during '{after_label}': "
            f"expected={expected_phase}, actual={actual_phase}. "
            "Internal runtime steps must not advance canonical phase."
        )
    return state


def run_phase(state_path: Path, dry_run: bool = False) -> int:
    if not state_path.is_file():
        raise FlowMindRunPhaseError(f"State file not found: {state_path}")

    state_path = state_path.resolve()
    repo_relative(state_path)

    state = load_canonical_state(state_path)
    phase = str(state.get("phase", "")).strip().upper()

    if phase == "HALT":
        raise FlowMindRunPhaseError(
            "Refusing to run while PROJECT_STATE.phase is HALT"
        )

    if phase in REFUSED_PHASES:
        raise FlowMindRunPhaseError(
            f"Runner v{RUNNER_VERSION} refuses phase '{phase}'. "
            "Upload/archive phases require explicit approval commands."
        )

    if phase == "AUDIO":
        raise FlowMindRunPhaseError(
            "AUDIO is not a canonical lifecycle phase. "
            "Canonical audio execution belongs inside SCENES."
        )

    pipeline = resolve_pipeline_for_phase(phase)

    print(f"[FLOWMIND_RUN_PHASE] version={RUNNER_VERSION}", flush=True)
    print(f"[FLOWMIND_RUN_PHASE] phase={phase}", flush=True)
    print(f"[FLOWMIND_RUN_PHASE] steps={len(pipeline)}", flush=True)

    if dry_run:
        dry_state = state
        for index, runtime_path in enumerate(pipeline, start=1):
            relative = runtime_path.relative_to(REPO_ROOT)
            print(
                f"[FLOWMIND_RUN_PHASE] dry_step={index}/{len(pipeline)} "
                f"runtime={relative}",
                flush=True,
            )

            try:
                command = build_command(
                    phase=phase,
                    runtime_path=runtime_path,
                    state_path=state_path,
                    state=dry_state,
                )
            except FlowMindRunPhaseError:
                command = build_simple_state_command(state_path, runtime_path)

            print(
                "[FLOWMIND_RUN_PHASE] dry_command=" + " ".join(command),
                flush=True,
            )

        print("[FLOWMIND_RUN_PHASE] dry_run=true", flush=True)
        return 0

    for index, runtime_path in enumerate(pipeline, start=1):
        state = validate_phase_unchanged(
            state_path,
            phase,
            after_label=f"pre-step-{index}",
        )

        relative = runtime_path.relative_to(REPO_ROOT)
        label = f"{index}/{len(pipeline)} {relative}"

        command = build_command(
            phase=phase,
            runtime_path=runtime_path,
            state_path=state_path,
            state=state,
        )

        exit_code = run_command(command, label=label)
        if exit_code != 0:
            return exit_code

        validate_phase_unchanged(
            state_path,
            phase,
            after_label=str(relative),
        )

    print(
        f"[FLOWMIND_RUN_PHASE] PHASE_PIPELINE_PASS phase={phase} "
        f"steps={len(pipeline)}",
        flush=True,
    )
    return 0


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        exit_code = run_phase(
            Path(args.state),
            dry_run=bool(args.dry_run),
        )
    except FlowMindRunPhaseError as exc:
        print(f"FLOWMIND_RUN_PHASE_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
