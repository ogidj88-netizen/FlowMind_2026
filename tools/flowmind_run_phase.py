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

from engine.canonical_dispatcher import CanonicalDispatcher
from engine.final_handoff import validate_final_handoff, project_file, read_object
from engine.state_validator import StateValidationError, load_state


RUNNER_VERSION = "2.1.0"

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
    parser.add_argument(
        "--handoff-to-qa", action="store_true",
        help="Resume an existing final render: readiness -> guarded QA transition -> QA only",
    )
    parser.add_argument("--rerun-stale-qa", action="store_true",
                        help="With --handoff-to-qa: archive stale evidence and rerun QA only")
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


def validate_qa_receipt(state_path: Path, state: dict[str, Any], fingerprint: str) -> dict[str, Any]:
    from datetime import datetime

    path = project_file(state["artifacts"].get("qa_report_path"), state_path)
    if path != (state_path.parent / "qa" / "qa_report.json").resolve():
        raise FlowMindRunPhaseError("QA report path is not canonical")
    report = read_object(path)
    if (report.get("project_id") != state["project_id"]
            or report.get("source_phase") != "QA"
            or report.get("executor") != "qa_executor"
            or report.get("handoff_input_fingerprint") != fingerprint):
        raise FlowMindRunPhaseError("QA report is not bound to the current handoff packet")
    if report.get("verdict") not in {"PASS", "FAIL", "BLOCKED"}:
        raise FlowMindRunPhaseError("QA report has no valid verdict")
    if (type(report.get("qa_passed")) is not bool
            or report["qa_passed"] != state["qa_passed"]
            or report["qa_passed"] != (report["verdict"] == "PASS")
            or type(report.get("approved_for_upload")) is not bool
            or report["approved_for_upload"] != state["approved_for_upload"]
            or not isinstance(report.get("checks"), list) or not report["checks"]
            or not isinstance(report.get("blockers"), list)):
        raise FlowMindRunPhaseError("QA verdict/state evidence is inconsistent")
    if report["verdict"] == "PASS" and (
            report["blockers"] or any(check.get("status") in {"FAIL", "BLOCKED"}
                                      for check in report["checks"])):
        raise FlowMindRunPhaseError("QA PASS conflicts with checks")
    transitions = [entry for entry in state["phase_history"] if entry["to"] == "QA"]
    if not transitions:
        raise FlowMindRunPhaseError("QA state has no recorded entry transition")
    try:
        created = datetime.fromisoformat(report["created_at"].replace("Z", "+00:00"))
        entered = datetime.fromisoformat(transitions[-1]["at"].replace("Z", "+00:00"))
        if created < entered:
            raise FlowMindRunPhaseError("QA report predates QA transition")
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise FlowMindRunPhaseError("Invalid QA report timestamp") from exc
    return report


def handoff_to_qa(state_path: Path, dry_run: bool = False, *, rerun_stale_qa: bool = False) -> int:
    from engine.state_store import file_lock, recover_artifact_publication

    state_path = state_path.resolve()
    repo_relative(state_path)
    initial = load_canonical_state(state_path)
    if initial["phase"] not in {"ASSEMBLY", "QA"}:
        raise FlowMindRunPhaseError("Handoff supports only ASSEMBLY or interrupted QA")
    if dry_run:
        return _handoff_to_qa(state_path, dry_run=True)
    with file_lock(str(state_path) + ".handoff.lock"):
        recover_artifact_publication(state_path)
        return _handoff_to_qa(state_path, rerun_stale_qa=rerun_stale_qa)


def _handoff_to_qa(state_path: Path, dry_run: bool = False, *, rerun_stale_qa: bool = False) -> int:
    """Explicit opt-in continuation. Never calls assembly/render/upload executors."""
    from tools.apply_final_render_readiness import apply_final_render_readiness

    state_path = state_path.resolve()
    repo_relative(state_path)
    state = load_canonical_state(state_path)
    if state["phase"] not in {"ASSEMBLY", "QA"}:
        raise FlowMindRunPhaseError("Handoff supports only ASSEMBLY or interrupted QA")
    original_approval = (state["approval_status"], state["approved_for_upload"])
    packet = validate_final_handoff(state_path, state, require_ready=state["phase"] == "QA")
    if dry_run:
        print("[HANDOFF] dry_run=true; readiness -> dispatcher QA -> QA; no render/upload")
        return 0
    if state["phase"] == "ASSEMBLY":
        apply_final_render_readiness(
            state_path, packet["assembly_plan_path"], packet["render_report_path"],
        )
        ready_state = load_canonical_state(state_path)
        if ready_state != state:
            raise FlowMindRunPhaseError("Readiness changed canonical state")
        validate_final_handoff(state_path, ready_state)
        CanonicalDispatcher(state_path).transition("QA")
        current = load_canonical_state(state_path)
        expected_history = state["phase_history"]
        if (current["phase"] != "QA"
                or len(current["phase_history"]) != len(expected_history) + 1
                or current["phase_history"][:-1] != expected_history
                or current["phase_history"][-1]["from"] != "ASSEMBLY"
                or current["phase_history"][-1]["to"] != "QA"
                or current["qa_passed"] != state["qa_passed"]
                or (current["approval_status"], current["approved_for_upload"]) != original_approval):
            raise FlowMindRunPhaseError("Dispatcher QA transition postconditions failed")
        state = current
    packet = validate_final_handoff(state_path, state)
    # Recover valid orphan receipts; stale evidence requires explicit QA-only retry.
    from copy import deepcopy
    from engine.state_store import save_state_with_disk_guard, state_lock, write_bytes_atomic
    import hashlib

    orphan_path = state_path.parent / "qa" / "qa_report.json"
    linked = "qa_report_path" in state["artifacts"]
    if linked or orphan_path.exists():
        candidate = deepcopy(state)
        if not linked:
            candidate["artifacts"]["qa_report_path"] = str(repo_relative(orphan_path))
        try:
            receipt = validate_qa_receipt(state_path, candidate, packet["input_fingerprint"])
        except (FlowMindRunPhaseError, StateValidationError):
            if not rerun_stale_qa:
                raise
            # Do not redirect arbitrary/noncanonical artifact paths or alter approval/QA flags.
            receipt_path = project_file(candidate["artifacts"]["qa_report_path"], state_path)
            if receipt_path != orphan_path.resolve() or state["qa_passed"] is not False:
                raise FlowMindRunPhaseError("Stale QA retry requires canonical receipt and qa_passed=false")
            with state_lock(state_path):
                if load_canonical_state(state_path) != state:
                    raise FlowMindRunPhaseError("state changed before stale QA retry")
                data = receipt_path.read_bytes()
                archive = receipt_path.parent / ("qa_report." + hashlib.sha256(data).hexdigest() + ".json")
                if archive.exists() and archive.read_bytes() != data:
                    raise FlowMindRunPhaseError("QA archive conflict")
                if not archive.exists():
                    write_bytes_atomic(archive, data)
                # Keep canonical evidence until QA replaces it. Retry after interruption
                # reuses the immutable archive and cannot duplicate phase history.
        else:
            if not linked:
                state = save_state_with_disk_guard(state_path, candidate, expected_state=state)
            print(f'[HANDOFF] QA_ALREADY_RECORDED verdict={receipt["verdict"]}; no QA execution')
            return 0
    history = state["phase_history"]
    if not history or history[-1]["to"] != "QA":
        raise FlowMindRunPhaseError("Interrupted QA has no entry transition")
    exit_code = run_phase(state_path)
    if exit_code != 0:
        return exit_code
    after = load_canonical_state(state_path)
    if (after["phase"] != "QA" or after["phase_history"] != history
            or (after["approval_status"], after["approved_for_upload"]) != original_approval
            or after["manifest"] != state["manifest"]):
        raise FlowMindRunPhaseError("QA changed protected handoff state")
    final_packet = validate_final_handoff(state_path, after)
    if final_packet["input_fingerprint"] != packet["input_fingerprint"]:
        raise FlowMindRunPhaseError("QA changed final handoff inputs")
    receipt = validate_qa_receipt(state_path, after, packet["input_fingerprint"])
    print(f'[HANDOFF] QA_RECORDED verdict={receipt["verdict"]}; phase=QA; upload not requested')
    return 0


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.rerun_stale_qa and not args.handoff_to_qa:
            raise FlowMindRunPhaseError("--rerun-stale-qa requires --handoff-to-qa")
        if args.handoff_to_qa:
            exit_code = handoff_to_qa(Path(args.state), dry_run=bool(args.dry_run),
                                      rerun_stale_qa=bool(args.rerun_stale_qa))
        else:
            exit_code = run_phase(Path(args.state), dry_run=bool(args.dry_run))
    except (FlowMindRunPhaseError, StateValidationError, OSError, ValueError) as exc:
        print(f"FLOWMIND_RUN_PHASE_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
