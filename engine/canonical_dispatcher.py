from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from engine.state_store import save_state_with_disk_guard
from engine.state_validator import StateValidationError, load_state


class DispatcherTransitionError(StateValidationError):
    """Raised when a phase transition violates dispatcher rules."""


ALLOWED_PHASE_TRANSITIONS: dict[str, set[str]] = {
    "TOPIC": {"SCRIPT", "HALT"},
    "SCRIPT": {"SCENES", "HALT"},
    "SCENES": {"ASSETS", "HALT"},
    "ASSETS": {"ASSEMBLY", "HALT"},
    "ASSEMBLY": {"QA", "HALT"},
    "QA": {"READY_FOR_UPLOAD", "HALT"},
    "READY_FOR_UPLOAD": {"UPLOADED", "HALT"},
    "UPLOADED": {"ARCHIVED"},
    "ARCHIVED": set(),
    "HALT": set(),
}

PHASE_ORDER: dict[str, int] = {
    "TOPIC": 10,
    "SCRIPT": 20,
    "SCENES": 30,
    "ASSETS": 40,
    "ASSEMBLY": 50,
    "QA": 60,
    "READY_FOR_UPLOAD": 70,
    "UPLOADED": 80,
    "ARCHIVED": 90,
    "HALT": 999,
}

NO_ROLLBACK_AFTER_PHASES = frozenset({"ASSEMBLY", "QA", "READY_FOR_UPLOAD", "UPLOADED", "ARCHIVED"})
RESUMABLE_PHASES = frozenset({"TOPIC", "SCRIPT", "SCENES", "ASSETS", "ASSEMBLY", "QA", "READY_FOR_UPLOAD"})


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class CanonicalDispatcher:
    def __init__(self, state_path: str | Path) -> None:
        self.state_path = Path(state_path)

    def load(self) -> dict[str, Any]:
        return load_state(self.state_path)

    def transition(
        self,
        target_phase: str,
        *,
        halt_reason: str | None = None,
        resume_hint: str | None = None,
        approval_status: str | None = None,
        approved_for_upload: bool | None = None,
        qa_passed: bool | None = None,
        artifacts_patch: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        current_state = self.load()
        candidate_state = self._build_transition_candidate(
            current_state=current_state,
            target_phase=target_phase,
            halt_reason=halt_reason,
            resume_hint=resume_hint,
            approval_status=approval_status,
            approved_for_upload=approved_for_upload,
            qa_passed=qa_passed,
            artifacts_patch=artifacts_patch,
        )
        return save_state_with_disk_guard(self.state_path, candidate_state)

    def halt(self, halt_reason: str, *, resume_hint: str | None = None) -> dict[str, Any]:
        return self.transition(
            "HALT",
            halt_reason=halt_reason,
            resume_hint=resume_hint,
        )

    def resume_from_halt(self, target_phase: str) -> dict[str, Any]:
        current_state = self.load()

        if current_state["phase"] != "HALT":
            raise DispatcherTransitionError("resume_from_halt is allowed only from phase 'HALT'")

        normalized_target = self._normalize_phase(target_phase)
        if normalized_target not in RESUMABLE_PHASES:
            raise DispatcherTransitionError(
                f"resume target '{normalized_target}' is not allowed"
            )

        candidate_state = deepcopy(current_state)
        candidate_state["phase"] = normalized_target
        candidate_state["halted"] = False
        candidate_state["halt_reason"] = None
        candidate_state["resume_hint"] = None
        candidate_state["updated_at"] = utc_now_iso()

        candidate_state["phase_history"] = list(candidate_state.get("phase_history", []))
        candidate_state["phase_history"].append(
            {
                "from": "HALT",
                "to": normalized_target,
                "at": candidate_state["updated_at"],
            }
        )

        self._assert_phase_guards("HALT", normalized_target, candidate_state)
        return save_state_with_disk_guard(self.state_path, candidate_state)

    def mark_qa_passed(self) -> dict[str, Any]:
        current_state = self.load()
        current_phase = current_state["phase"]

        if current_phase != "QA":
            raise DispatcherTransitionError("qa_passed can only be set while phase is 'QA'")

        candidate_state = deepcopy(current_state)
        candidate_state["qa_passed"] = True
        candidate_state["updated_at"] = utc_now_iso()
        return save_state_with_disk_guard(self.state_path, candidate_state)

    def approve_for_upload(self) -> dict[str, Any]:
        current_state = self.load()
        current_phase = current_state["phase"]

        if current_phase != "READY_FOR_UPLOAD":
            raise DispatcherTransitionError(
                "approved_for_upload can only be set while phase is 'READY_FOR_UPLOAD'"
            )

        candidate_state = deepcopy(current_state)
        candidate_state["approved_for_upload"] = True
        candidate_state["approval_status"] = "APPROVED"
        candidate_state["updated_at"] = utc_now_iso()
        return save_state_with_disk_guard(self.state_path, candidate_state)

    def _build_transition_candidate(
        self,
        *,
        current_state: Mapping[str, Any],
        target_phase: str,
        halt_reason: str | None,
        resume_hint: str | None,
        approval_status: str | None,
        approved_for_upload: bool | None,
        qa_passed: bool | None,
        artifacts_patch: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        current_phase = current_state["phase"]
        target_phase = self._normalize_phase(target_phase)

        self._assert_transition_allowed(current_phase, target_phase)

        candidate_state = deepcopy(dict(current_state))
        previous_phase = current_phase

        candidate_state["phase"] = target_phase
        candidate_state["updated_at"] = utc_now_iso()
        candidate_state["halted"] = target_phase == "HALT"
        candidate_state["halt_reason"] = halt_reason if target_phase == "HALT" else None
        candidate_state["resume_hint"] = resume_hint if target_phase == "HALT" else None

        if approval_status is not None:
            candidate_state["approval_status"] = approval_status

        if approved_for_upload is not None:
            candidate_state["approved_for_upload"] = approved_for_upload

        if qa_passed is not None:
            candidate_state["qa_passed"] = qa_passed

        if artifacts_patch:
            artifacts = dict(candidate_state.get("artifacts", {}))
            artifacts.update(dict(artifacts_patch))
            candidate_state["artifacts"] = artifacts

        self._assert_phase_guards(previous_phase, target_phase, candidate_state)

        candidate_state["phase_history"] = list(candidate_state.get("phase_history", []))
        candidate_state["phase_history"].append(
            {
                "from": previous_phase,
                "to": target_phase,
                "at": candidate_state["updated_at"],
            }
        )

        return candidate_state

    def _assert_transition_allowed(self, current_phase: str, target_phase: str) -> None:
        if current_phase == target_phase:
            raise DispatcherTransitionError("no-op phase transition is not allowed")

        allowed_targets = ALLOWED_PHASE_TRANSITIONS.get(current_phase)
        if allowed_targets is None:
            raise DispatcherTransitionError(f"unknown current phase '{current_phase}'")

        if target_phase == "HALT":
            return

        self._assert_no_unsafe_rollback(current_phase, target_phase)

        if target_phase not in allowed_targets:
            raise DispatcherTransitionError(
                f"transition '{current_phase}' -> '{target_phase}' is not allowed"
            )

    def _assert_no_unsafe_rollback(self, current_phase: str, target_phase: str) -> None:
        current_rank = PHASE_ORDER.get(current_phase)
        target_rank = PHASE_ORDER.get(target_phase)

        if current_rank is None or target_rank is None:
            raise DispatcherTransitionError(
                f"phase order is undefined for transition '{current_phase}' -> '{target_phase}'"
            )

        if current_phase in NO_ROLLBACK_AFTER_PHASES and target_rank < current_rank:
            raise DispatcherTransitionError(
                f"rollback is forbidden after phase '{current_phase}'"
            )

    def _assert_phase_guards(
        self,
        previous_phase: str,
        target_phase: str,
        candidate_state: Mapping[str, Any],
    ) -> None:
        if previous_phase == "ASSEMBLY" and target_phase == "QA":
            artifacts = candidate_state.get("artifacts", {})
            if "final_video_path" not in artifacts:
                raise DispatcherTransitionError(
                    "cannot transition ASSEMBLY -> QA without artifacts.final_video_path"
                )

        if previous_phase == "QA" and target_phase == "READY_FOR_UPLOAD":
            if candidate_state.get("qa_passed") is not True:
                raise DispatcherTransitionError(
                    "cannot transition QA -> READY_FOR_UPLOAD while qa_passed is not true"
                )

        if previous_phase == "READY_FOR_UPLOAD" and target_phase == "UPLOADED":
            if candidate_state.get("approved_for_upload") is not True:
                raise DispatcherTransitionError(
                    "cannot transition READY_FOR_UPLOAD -> UPLOADED while approved_for_upload is not true"
                )

    @staticmethod
    def _normalize_phase(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise DispatcherTransitionError("target_phase must be a non-empty string")
        return value.strip().upper()


__all__ = [
    "ALLOWED_PHASE_TRANSITIONS",
    "CanonicalDispatcher",
    "DispatcherTransitionError",
    "NO_ROLLBACK_AFTER_PHASES",
    "PHASE_ORDER",
    "RESUMABLE_PHASES",
    "utc_now_iso",
]
