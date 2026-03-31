from __future__ import annotations

import tempfile
from pathlib import Path

from engine.canonical_dispatcher import CanonicalDispatcher, DispatcherTransitionError
from engine.state_store import save_state_atomic
from engine.state_validator import compute_manifest_hash, load_state


def build_initial_state() -> dict:
    manifest = {
        "manifest_id": "P2026_SMOKE:v1",
        "manifest_version": 1,
        "mode": "cashflow-mode",
        "niche": "Money Mistakes / Invisible Costs",
        "audience": "Global English",
        "content_language": "en",
        "primary_platform": "youtube",
        "topic": "Smoke test topic",
        "working_title": "Smoke Test Working Title",
        "hook": "You lose money here without noticing it.",
        "target_duration_sec": 480,
        "render_profile": "ffmpeg_stability_standard_v1_2",
        "stock_policy": "stock_first_no_repeat",
        "created_at": "2026-03-31T00:00:00Z",
        "locked": True,
    }
    manifest["manifest_hash"] = compute_manifest_hash(manifest)

    return {
        "project_id": "P2026_SMOKE",
        "phase": "TOPIC",
        "phase_history": [],
        "updated_at": "2026-03-31T00:00:00Z",
        "halted": False,
        "halt_reason": None,
        "resume_hint": None,
        "approval_status": "PENDING",
        "approved_for_upload": False,
        "qa_passed": False,
        "artifacts": {},
        "manifest": manifest,
    }


def expect_failure(fn, expected_text: str) -> None:
    try:
        fn()
    except DispatcherTransitionError as exc:
        message = str(exc)
        if expected_text not in message:
            raise AssertionError(
                f"Expected error containing '{expected_text}', got '{message}'"
            ) from exc
    else:
        raise AssertionError(f"Expected failure containing '{expected_text}'")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="flowmind_dispatcher_smoke_") as tmp_dir:
        state_path = Path(tmp_dir) / "PROJECT_STATE.json"

        initial_state = build_initial_state()
        save_state_atomic(state_path, initial_state)

        dispatcher = CanonicalDispatcher(state_path)

        state = dispatcher.load()
        assert state["phase"] == "TOPIC"

        state = dispatcher.transition("SCRIPT")
        assert state["phase"] == "SCRIPT"

        state = dispatcher.transition("SCENES")
        assert state["phase"] == "SCENES"

        state = dispatcher.transition("ASSETS")
        assert state["phase"] == "ASSETS"

        state = dispatcher.transition("ASSEMBLY")
        assert state["phase"] == "ASSEMBLY"

        expect_failure(
            lambda: dispatcher.transition("QA"),
            "cannot transition ASSEMBLY -> QA without artifacts.final_video_path",
        )

        state = dispatcher.transition(
            "QA",
            artifacts_patch={"final_video_path": "/tmp/final.mp4"},
        )
        assert state["phase"] == "QA"
        assert state["artifacts"]["final_video_path"] == "/tmp/final.mp4"

        expect_failure(
            lambda: dispatcher.transition("READY_FOR_UPLOAD"),
            "cannot transition QA -> READY_FOR_UPLOAD while qa_passed is not true",
        )

        state = dispatcher.mark_qa_passed()
        assert state["qa_passed"] is True

        state = dispatcher.transition("READY_FOR_UPLOAD")
        assert state["phase"] == "READY_FOR_UPLOAD"

        expect_failure(
            lambda: dispatcher.transition("UPLOADED"),
            "cannot transition READY_FOR_UPLOAD -> UPLOADED while approved_for_upload is not true",
        )

        state = dispatcher.approve_for_upload()
        assert state["approved_for_upload"] is True
        assert state["approval_status"] == "APPROVED"

        state = dispatcher.transition("UPLOADED")
        assert state["phase"] == "UPLOADED"

        state = dispatcher.transition("ARCHIVED")
        assert state["phase"] == "ARCHIVED"

        reloaded = load_state(state_path)
        assert reloaded["phase"] == "ARCHIVED"
        assert len(reloaded["phase_history"]) == 7

        print("SMOKE_TEST_OK")
        print(f"state_path={state_path}")
        print(f"final_phase={reloaded['phase']}")
        print(f"phase_history_entries={len(reloaded['phase_history'])}")


if __name__ == "__main__":
    main()
