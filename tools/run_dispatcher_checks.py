from __future__ import annotations

import sys
import tempfile
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.canonical_dispatcher import CanonicalDispatcher, DispatcherTransitionError
from engine.state_store import save_state_atomic
from engine.state_validator import compute_manifest_hash, load_state


def build_manifest(project_id: str) -> dict:
    manifest = {
        "manifest_id": f"{project_id}:v1",
        "manifest_version": 1,
        "mode": "cashflow-mode",
        "niche": "Money Mistakes / Invisible Costs",
        "audience": "Global English",
        "content_language": "en",
        "primary_platform": "youtube",
        "topic": "Dispatcher check topic",
        "working_title": "Dispatcher Check Working Title",
        "hook": "Dispatcher check hook",
        "target_duration_sec": 480,
        "render_profile": "ffmpeg_stability_standard_v1_2",
        "stock_policy": "stock_first_no_repeat",
        "created_at": "2026-03-31T00:00:00Z",
        "locked": True,
    }
    manifest["manifest_hash"] = compute_manifest_hash(manifest)
    return manifest


def build_state(
    project_id: str,
    phase: str,
    *,
    halted: bool = False,
    halt_reason: str | None = None,
    resume_hint: str | None = None,
    qa_passed: bool = False,
    approved_for_upload: bool = False,
    artifacts: dict | None = None,
) -> dict:
    return {
        "project_id": project_id,
        "phase": phase,
        "phase_history": [],
        "updated_at": "2026-03-31T00:00:00Z",
        "halted": halted,
        "halt_reason": halt_reason,
        "resume_hint": resume_hint,
        "approval_status": "PENDING",
        "approved_for_upload": approved_for_upload,
        "qa_passed": qa_passed,
        "artifacts": artifacts or {},
        "manifest": build_manifest(project_id),
    }


def expect_failure(fn, expected_text: str) -> None:
    try:
        fn()
    except DispatcherTransitionError as exc:
        message = str(exc)
        if expected_text not in message:
            raise AssertionError(
                f"Expected '{expected_text}', got '{message}'"
            ) from exc
    else:
        raise AssertionError(f"Expected failure containing '{expected_text}'")


def run_smoke_test() -> None:
    with tempfile.TemporaryDirectory(prefix="flowmind_dispatcher_smoke_") as tmp_dir:
        state_path = Path(tmp_dir) / "PROJECT_STATE.json"
        save_state_atomic(state_path, build_state("P2026_SMOKE_ALL", "TOPIC"))

        dispatcher = CanonicalDispatcher(state_path)

        dispatcher.transition("SCRIPT")
        dispatcher.transition("SCENES")
        dispatcher.transition("ASSETS")
        dispatcher.transition("ASSEMBLY")
        dispatcher.transition("AUDIO")

        expect_failure(
            lambda: dispatcher.transition("QA"),
            "cannot transition AUDIO -> QA without artifacts.audio_plan_path",
        )

        dispatcher.transition("QA", artifacts_patch={"audio_plan_path": "/tmp/audio_plan.json"})

        expect_failure(
            lambda: dispatcher.transition("READY_FOR_UPLOAD"),
            "cannot transition QA -> READY_FOR_UPLOAD while qa_passed is not true",
        )

        dispatcher.mark_qa_passed()
        dispatcher.transition("READY_FOR_UPLOAD")

        expect_failure(
            lambda: dispatcher.transition("UPLOADED"),
            "cannot transition READY_FOR_UPLOAD -> UPLOADED while approved_for_upload is not true",
        )

        dispatcher.approve_for_upload()
        dispatcher.transition("UPLOADED")
        dispatcher.transition("ARCHIVED")

        reloaded = load_state(state_path)
        assert reloaded["phase"] == "ARCHIVED"
        assert len(reloaded["phase_history"]) == 9

        print("SMOKE_TEST_OK")


def run_rollback_guard_test() -> None:
    with tempfile.TemporaryDirectory(prefix="flowmind_rollback_test_") as tmp_dir:
        state_path = Path(tmp_dir) / "PROJECT_STATE.json"
        save_state_atomic(
            state_path,
            build_state(
                "P2026_ROLLBACK_ALL",
                "QA",
                qa_passed=True,
                artifacts={"audio_plan_path": "/tmp/audio_plan.json"},
            ),
        )

        dispatcher = CanonicalDispatcher(state_path)

        try:
            dispatcher.transition("ASSETS")
        except DispatcherTransitionError as exc:
            message = str(exc)
            if "rollback is forbidden after phase 'QA'" not in message:
                raise
            print("ROLLBACK_GUARD_OK")
        else:
            raise AssertionError("Rollback guard failed")


def run_resume_test() -> None:
    with tempfile.TemporaryDirectory(prefix="flowmind_resume_test_") as tmp_dir:
        state_path = Path(tmp_dir) / "PROJECT_STATE.json"
        save_state_atomic(
            state_path,
            build_state(
                "P2026_RESUME_ALL",
                "HALT",
                halted=True,
                halt_reason="TEST_HALT",
                resume_hint="resume_to_audio",
            ),
        )

        dispatcher = CanonicalDispatcher(state_path)
        resumed = dispatcher.resume_from_halt("AUDIO")

        assert resumed["phase"] == "AUDIO"
        assert resumed["halted"] is False
        assert resumed["halt_reason"] is None
        assert resumed["resume_hint"] is None

        print("RESUME_OK")


def main() -> None:
    run_smoke_test()
    run_rollback_guard_test()
    run_resume_test()
    print("DISPATCHER_CHECKS_ALL_OK")


if __name__ == "__main__":
    main()
