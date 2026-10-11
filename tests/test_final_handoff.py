"""Isolated handoff runtime tests. No FlowMind production executor is executed."""
from __future__ import annotations

import copy
from contextlib import ExitStack
import multiprocessing
import json
import shutil
import subprocess
import tempfile
from fractions import Fraction
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from engine import final_handoff as evidence
from engine.canonical_dispatcher import CanonicalDispatcher, DispatcherTransitionError
from engine.state_store import save_state_atomic, save_state_with_disk_guard, state_lock
from engine.state_validator import StateValidationError, compute_manifest_hash, load_state
from tools import apply_final_render_readiness as readiness
from tools import flowmind_run_phase as runner


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, sort_keys=True) + "\n", encoding="utf-8")


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_dir = tempfile.TemporaryDirectory(prefix="flowmind_media_")
        cls.media = {}
        # Tiny local fixture media only: no production renderer or remote service.
        for name, dimensions, duration, fps in [
                ("landscape", "32x18", 2, 30),
                ("shorts", "18x32", 2, 30),
                ("long", "32x18", 600, 1)]:
            path = Path(cls.media_dir.name) / (name + ".mp4")
            subprocess.run([
                "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                f"color=c=black:s={dimensions}:r={fps}:d={duration}",
                "-f", "lavfi", "-i", "anullsrc=r=8000:cl=mono", "-t", str(duration),
                "-c:v", "libx264", "-threads", "1", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-y", str(path),
            ], check=True, timeout=30)
            cls.media[name] = path

    @classmethod
    def tearDownClass(cls):
        cls.media_dir.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="flowmind_handoff_")
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.root_patches = [patch.object(m, "REPO_ROOT", self.root)
                             for m in (evidence, readiness, runner)]
        for p in self.root_patches:
            p.start()
            self.addCleanup(p.stop)
        self.executed = []
        actual_subprocess_run = subprocess.run
        def only_ffprobe(command, *args, **kwargs):
            self.assertEqual(command[0], "ffprobe", "production/API subprocess forbidden")
            return actual_subprocess_run(command, *args, **kwargs)
        p = patch.object(subprocess, "run", only_ffprobe)
        p.start()
        self.addCleanup(p.stop)
        # resolve_pipeline checks the allowed path exists; the file is never executed.
        qa = self.root / "engine/executors/qa_executor.py"
        qa.parent.mkdir(parents=True)
        qa.write_text("# isolated QA test double; never launched\n")
        self.command_patch = patch.object(runner, "run_command", self.qa_double)
        self.command_patch.start()
        self.addCleanup(self.command_patch.stop)

    def fixture(self, scenes=3, segments=2, media="landscape"):
        pid = "ISOLATED_HANDOFF"
        base = self.root / "projects" / pid
        self.state_path = base / "PROJECT_STATE.json"
        self.plan_path = base / "assembly/assembly_plan.json"
        self.report_path = base / "final_render/final_render_report.json"
        self.video_path = base / "final_render/final_video.mp4"
        self.video_path.parent.mkdir(parents=True)
        shutil.copyfile(self.media[media], self.video_path)
        probe = evidence.probe_video(self.video_path)
        duration = float(probe["format"]["duration"])
        video = next(s for s in probe["streams"] if s["codec_type"] == "video")
        audio_stream = next(s for s in probe["streams"] if s["codec_type"] == "audio")
        rel = lambda p: str(p.relative_to(self.root))
        audio = base / "audio/segment.mp3"
        audio.parent.mkdir()
        audio.write_bytes(b"isolated audio input")
        resolved = base / "assets/resolved_assets.json"
        audio_render = base / "audio/audio_render.json"
        write(resolved, {"project_id": pid})
        write(audio_render, {"project_id": pid})
        manifest = {
            "manifest_id": pid + ":v1", "manifest_version": 1,
            "mode": "cashflow-mode", "niche": "isolated", "audience": "test",
            "content_language": "en", "primary_platform": "youtube",
            "topic": "isolated", "working_title": "isolated", "hook": "isolated",
            "target_duration_sec": 600 if media == "long" else 2,
            "render_profile": "isolated_" + media, "stock_policy": "isolated",
            "created_at": "2026-10-01T00:00:00Z", "locked": True,
        }
        manifest["manifest_hash"] = compute_manifest_hash(manifest)
        state = {
            "project_id": pid, "phase": "ASSEMBLY", "phase_history": [],
            "updated_at": "2026-10-01T00:00:00Z", "halted": False,
            "halt_reason": None, "resume_hint": None, "approval_status": "PENDING",
            "approved_for_upload": False, "qa_passed": False, "manifest": manifest,
            "artifacts": {
                "assembly_plan_path": rel(self.plan_path),
                "final_render_report_path": rel(self.report_path),
                "final_video_path": rel(self.video_path),
                "resolved_assets_path": rel(resolved), "audio_render_path": rel(audio_render),
            },
        }
        for key, name in (("script_path", "script.txt"), ("script_meta_path", "script_meta.json"),
                          ("script_qa_path", "script_qa.json"), ("scenes_path", "scenes.json"),
                          ("assets_path", "assets.json"), ("audio_plan_path", "audio_plan.json")):
            path = base / name
            if path.suffix == ".json":
                write(path, {"project_id": pid})
            else:
                path.write_text("Isolated script text")
            state["artifacts"][key] = rel(path)
        visual_path = base / "assets/visual.jpg"
        visual_path.write_bytes(b"isolated visual input")
        save_state_atomic(self.state_path, state)
        timeline, outputs = [], []
        total_visuals = 0
        for i in range(1, scenes + 1):
            count = segments + (i % 2)
            visuals = [{"segment_id": f"S{i}_V{j}", "asset_id": f"A{i}_{j}",
                        "duration_sec": duration / scenes / count, "visual_asset_path": rel(visual_path)}
                       for j in range(count)]
            entry = {"scene_id": f"S{i}", "timeline_id": f"T{i}", "order": i,
                     "audio_segment_id": f"AUDIO{i}", "audio_path": rel(audio),
                     "audio_duration_sec": duration / scenes, "visual_segments": visuals}
            timeline.append(entry)
            output = copy.deepcopy(entry)
            output["render_status"] = "rendered"
            output["visual_segment_count"] = count
            for visual in output["visual_segments"]:
                visual["expected_duration_sec"] = visual.pop("duration_sec")
                visual["render_status"] = "rendered"
            outputs.append(output)
            total_visuals += count
        plan = {"project_id": pid, "assets_ready": True, "audio_ready": True,
                "render_ready": False, "readiness_status": "blocked_by_final_render_executor",
                "missing_requirements": ["final render executor"],
                "scene_count": scenes, "timeline": timeline,
                "source_resolved_assets_path": rel(resolved),
                "source_audio_render_path": rel(audio_render)}
        report = {
            "project_id": pid, "status": "FINAL_RENDER_OK", "verdict": "PASS",
            "final_video_exists": True, "final_video_path": rel(self.video_path),
            "final_video_size_bytes": self.video_path.stat().st_size,
            "final_duration_sec": duration, "expected_duration_sec": duration,
            "duration_delta_sec": 0, "scene_count": scenes, "rendered_scene_count": scenes,
            "visual_segment_count": total_visuals, "failed_scene_count": 0, "blockers": [],
            "video_profile": {"resolution": f'{video["width"]}x{video["height"]}',
                              "fps": float(Fraction(video["r_frame_rate"])),
                              "video_codec": video["codec_name"], "pixel_format": video["pix_fmt"],
                              "audio_codec": audio_stream["codec_name"],
                              "audio_channels": audio_stream["channels"],
                              "audio_sample_rate": int(audio_stream["sample_rate"])},
            "source_project_state_path": rel(self.state_path),
            "source_assembly_plan_path": rel(self.plan_path),
            "source_resolved_assets_path": rel(resolved),
            "source_audio_render_path": rel(audio_render), "scenes": outputs,
        }
        write(self.plan_path, plan)
        write(self.report_path, report)
        return state

    def ready(self):
        return readiness.apply_final_render_readiness(
            self.state_path, self.plan_path, self.report_path)

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def qa_double(self, command, *, label):
        self.assertEqual(command[1], "engine/executors/qa_executor.py")
        self.executed.append(command[1])
        state = load_state(self.state_path)
        self.assertEqual(state["phase"], "QA")
        packet = evidence.validate_final_handoff(self.state_path, state)
        report_path = self.state_path.parent / "qa/qa_report.json"
        report = {
            "project_id": state["project_id"], "source_phase": "QA",
            "executor": "qa_executor", "handoff_input_fingerprint": packet["input_fingerprint"],
            "verdict": "BLOCKED", "qa_passed": False, "approved_for_upload": False,
            "checks": [{"check_id": "upload_readiness", "status": "BLOCKED"}],
            "blockers": ["upload_readiness"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        write(report_path, report)
        state["artifacts"]["qa_report_path"] = str(report_path.relative_to(self.root))
        save_state_with_disk_guard(self.state_path, state)
        return 0

    def assert_complete(self):
        state = load_state(self.state_path)
        self.assertEqual(state["phase"], "QA")
        self.assertEqual([(e["from"], e["to"]) for e in state["phase_history"]],
                         [("ASSEMBLY", "QA")])
        self.assertFalse(state["qa_passed"])
        self.assertFalse(state["approved_for_upload"])
        self.assertEqual(state["approval_status"], "PENDING")
        self.assertTrue(evidence.read_object(self.plan_path)["render_ready"])
        packet = evidence.validate_final_handoff(self.state_path, state)
        report = runner.validate_qa_receipt(self.state_path, state, packet["input_fingerprint"])
        self.assertEqual(report["verdict"], "BLOCKED")

    def test_actual_long_shorts_and_variable_counts(self):
        for media, scenes, segments in [("landscape", 1, 1), ("shorts", 13, 3), ("long", 37, 5)]:
            with self.subTest(media=media, scenes=scenes):
                # New isolated canonical project for each actual-media scenario.
                shutil.rmtree(self.root / "projects", ignore_errors=True)
                self.executed.clear()
                self.fixture(scenes, segments, media)
                video = self.video_path.read_bytes()
                self.assertEqual(runner.handoff_to_qa(self.state_path), 0)
                self.assert_complete()
                before = self.snapshot()
                self.assertEqual(runner.handoff_to_qa(self.state_path), 0)
                self.assertEqual(before, self.snapshot())
                self.assertEqual(self.video_path.read_bytes(), video)
                self.assertEqual(self.executed, ["engine/executors/qa_executor.py"])

    def test_readiness_is_idempotent_and_state_unchanged(self):
        self.fixture()
        state_bytes = self.state_path.read_bytes()
        self.assertTrue(self.ready()["changed"])
        before = self.snapshot()
        self.assertFalse(self.ready()["changed"])
        self.assertEqual(before, self.snapshot())
        self.assertEqual(state_bytes, self.state_path.read_bytes())

    def test_interruption_after_render(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        self.assert_complete()

    def test_interruption_after_readiness(self):
        self.fixture()
        self.ready()
        with patch.object(CanonicalDispatcher, "transition", side_effect=RuntimeError("interrupted")):
            with self.assertRaises(RuntimeError):
                runner.handoff_to_qa(self.state_path)
        self.assertEqual(load_state(self.state_path)["phase"], "ASSEMBLY")
        runner.handoff_to_qa(self.state_path)
        self.assert_complete()

    def test_interruption_after_transition(self):
        self.fixture()
        with patch.object(runner, "run_phase", side_effect=RuntimeError("interrupted")):
            with self.assertRaises(RuntimeError):
                runner.handoff_to_qa(self.state_path)
        self.assertEqual(load_state(self.state_path)["phase"], "QA")
        self.assertEqual(self.executed, [])
        runner.handoff_to_qa(self.state_path)
        self.assert_complete()

    def test_guard_rejects_unready_without_writes(self):
        self.fixture()
        before = self.snapshot()
        with self.assertRaises(DispatcherTransitionError):
            CanonicalDispatcher(self.state_path).transition("QA")
        self.assertEqual(before, self.snapshot())

    def test_guard_negative_packets(self):
        cases = [
            ("foreign_state", lambda s, p, r: self.change_state_id(s)),
            ("foreign_plan", lambda s, p, r: p.update(project_id="FOREIGN")),
            ("plan_wrong_audio", lambda s, p, r: p.update(source_audio_render_path=s["artifacts"]["resolved_assets_path"])),
            ("foreign_report", lambda s, p, r: r.update(project_id="FOREIGN")),
            ("wrong_video", lambda s, p, r: r.update(final_video_path=s["artifacts"]["audio_render_path"])),
            ("outside_path", lambda s, p, r: s["artifacts"].update(final_video_path="/etc/passwd")),
            ("parent_escape", lambda s, p, r: s["artifacts"].update(final_video_path="../../etc/passwd")),
            ("missing_video", lambda s, p, r: self.video_path.unlink()),
            ("empty_video", lambda s, p, r: self.video_path.write_bytes(b"")),
            ("corrupt_same_size", lambda s, p, r: self.video_path.write_bytes(b"x" * self.video_path.stat().st_size)),
            ("size_mismatch", lambda s, p, r: r.update(final_video_size_bytes=1)),
            ("failed_render", lambda s, p, r: r.update(verdict="FAIL")),
            ("blockers", lambda s, p, r: r.update(blockers=["missing"])),
            ("failed_scenes", lambda s, p, r: r.update(failed_scene_count=1)),
            ("scene_count", lambda s, p, r: r.update(scene_count=13)),
            ("missing_scene", lambda s, p, r: r["scenes"].pop()),
            ("segment_count", lambda s, p, r: r.update(visual_segment_count=999)),
            ("scene_order", lambda s, p, r: r["scenes"].reverse()),
            ("foreign_scene", lambda s, p, r: r["scenes"][0].update(scene_id="FOREIGN")),
            ("wrong_dimensions", lambda s, p, r: r["video_profile"].update(resolution="1920x1080")),
            ("wrong_fps", lambda s, p, r: r["video_profile"].update(fps=24)),
            ("wrong_codec", lambda s, p, r: r["video_profile"].update(video_codec="hevc")),
            ("nan_duration", lambda s, p, r: r.update(final_duration_sec=float("nan"))),
            ("actual_duration", lambda s, p, r: r.update(final_duration_sec=3, duration_delta_sec=1)),
            ("not_audio_ready", lambda s, p, r: p.update(audio_ready=False)),
            ("stale_missing", lambda s, p, r: p.update(missing_requirements=["final render executor"])),
        ]
        for name, mutate in cases:
            with self.subTest(case=name):
                shutil.rmtree(self.root / "projects", ignore_errors=True)
                self.fixture()
                self.ready()
                state = load_state(self.state_path)
                plan, report = evidence.read_object(self.plan_path), evidence.read_object(self.report_path)
                mutate(state, plan, report)
                write(self.plan_path, plan)
                write(self.report_path, report)
                save_state_atomic(self.state_path, state)
                before = self.snapshot()
                with self.assertRaises(DispatcherTransitionError):
                    CanonicalDispatcher(self.state_path).transition("QA")
                self.assertEqual(before, self.snapshot())
                self.assertEqual(self.executed, [])

    def test_resume_cannot_bypass_guard(self):
        self.fixture()
        dispatcher = CanonicalDispatcher(self.state_path)
        dispatcher.halt("isolated interruption")
        before = self.snapshot()
        with self.assertRaises(DispatcherTransitionError):
            dispatcher.resume_from_halt("QA")
        self.assertEqual(before, self.snapshot())

    def test_readiness_bad_arguments_do_not_write(self):
        self.fixture()
        before = self.snapshot()
        with self.assertRaises(readiness.ApplyFinalRenderReadinessError):
            readiness.apply_final_render_readiness(self.state_path, self.report_path, self.report_path)
        self.assertEqual(before, self.snapshot())

    def test_dry_run_is_read_only(self):
        self.fixture()
        before = self.snapshot()
        self.assertEqual(runner.handoff_to_qa(self.state_path, dry_run=True), 0)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(self.executed, [])

    def test_exit_zero_without_qa_evidence_rejected(self):
        self.fixture()
        with patch.object(runner, "run_command", return_value=0):
            with self.assertRaises(evidence.FinalHandoffError):
                runner.handoff_to_qa(self.state_path)
        state = load_state(self.state_path)
        self.assertEqual(state["phase"], "QA")
        self.assertFalse(state["qa_passed"])
        runner.handoff_to_qa(self.state_path)
        self.assert_complete()

    def test_stale_qa_receipt_rejected_without_writes(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        report_path = self.state_path.parent / "qa/qa_report.json"
        report = evidence.read_object(report_path)
        report["handoff_input_fingerprint"] = "stale"
        write(report_path, report)
        before = self.snapshot()
        with self.assertRaises(runner.FlowMindRunPhaseError):
            runner.handoff_to_qa(self.state_path)
        self.assertEqual(before, self.snapshot())

    def test_changed_video_after_qa_not_reused(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        report = evidence.read_object(self.report_path)
        report["warnings"] = ["new input evidence"]
        write(self.report_path, report)
        with self.assertRaises(runner.FlowMindRunPhaseError):
            runner.handoff_to_qa(self.state_path)

    def test_qa_failure_recoverable_without_duplicate_transition(self):
        self.fixture()
        with patch.object(runner, "run_command", return_value=9):
            self.assertEqual(runner.handoff_to_qa(self.state_path), 9)
        self.assertEqual(len(load_state(self.state_path)["phase_history"]), 1)
        runner.handoff_to_qa(self.state_path)
        self.assert_complete()

    def change_state_id(self, state):
        state["project_id"] = "OTHER"
        state["manifest"]["manifest_id"] = "OTHER:v1"
        state["manifest"]["manifest_hash"] = compute_manifest_hash(state["manifest"])

    def test_probe_failure_no_state_mutation(self):
        self.fixture()
        self.ready()
        before = self.snapshot()
        for error in [OSError("ffprobe unavailable"), subprocess.TimeoutExpired("ffprobe", 60)]:
            with self.subTest(error=str(error)), patch.object(subprocess, "run", side_effect=error):
                with self.assertRaises(DispatcherTransitionError):
                    CanonicalDispatcher(self.state_path).transition("QA")
                self.assertEqual(before, self.snapshot())

    def test_symlink_escape_rejected(self):
        self.fixture()
        self.ready()
        outside = self.root / "outside.mp4"
        shutil.copyfile(self.video_path, outside)
        self.video_path.unlink()
        self.video_path.symlink_to(outside)
        before = self.snapshot()
        with self.assertRaises(DispatcherTransitionError):
            CanonicalDispatcher(self.state_path).transition("QA")
        self.assertEqual(before, self.snapshot())

    def test_interruption_after_qa_report_before_state_link(self):
        self.fixture()
        self.ready()
        CanonicalDispatcher(self.state_path).transition("QA")
        old_state = load_state(self.state_path)
        self.qa_double([str(Path("python")), "engine/executors/qa_executor.py"], label="isolated")
        save_state_atomic(self.state_path, old_state)
        self.executed.clear()
        runner.handoff_to_qa(self.state_path)
        self.assert_complete()
        self.assertEqual(self.executed, [])
        before = self.snapshot()
        runner.handoff_to_qa(self.state_path)
        self.assertEqual(before, self.snapshot())

    def test_future_phases_refused_without_writes(self):
        self.fixture()
        state = load_state(self.state_path)
        state["phase"] = "READY_FOR_UPLOAD"
        save_state_atomic(self.state_path, state)
        before = self.snapshot()
        with self.assertRaises(runner.FlowMindRunPhaseError):
            runner.handoff_to_qa(self.state_path)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(self.executed, [])

    def test_changed_audio_evidence_not_reused(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        audio = self.root / load_state(self.state_path)["artifacts"]["audio_render_path"]
        write(audio, {"project_id": "ISOLATED_HANDOFF", "changed_input": True})
        before = self.snapshot()
        with self.assertRaises(runner.FlowMindRunPhaseError):
            runner.handoff_to_qa(self.state_path)
        self.assertEqual(before, self.snapshot())

    def test_zero_transition_without_persisted_state_rejected(self):
        self.fixture()
        with patch.object(CanonicalDispatcher, "transition", return_value={}):
            with self.assertRaises(runner.FlowMindRunPhaseError):
                runner.handoff_to_qa(self.state_path)
        self.assertEqual(load_state(self.state_path)["phase"], "ASSEMBLY")
        self.assertEqual(load_state(self.state_path)["phase_history"], [])
        self.assertEqual(self.executed, [])

    def test_stale_state_cannot_overwrite_concurrent_halt(self):
        self.fixture()
        self.ready()
        original = load_state(self.state_path)
        candidate = CanonicalDispatcher(self.state_path)._build_transition_candidate(
            current_state=original, target_phase="QA", halt_reason=None, resume_hint=None,
            approval_status=None, approved_for_upload=None, qa_passed=None, artifacts_patch=None)
        ctx = multiprocessing.get_context("fork")
        started, proceed, result = ctx.Event(), ctx.Event(), ctx.Queue()
        def delayed_write():
            started.set()
            proceed.wait(10)
            try:
                save_state_with_disk_guard(self.state_path, candidate, expected_state=original)
                result.put("OVERWROTE")
            except StateValidationError:
                result.put("STALE_REJECTED")
        child = ctx.Process(target=delayed_write)
        child.start()
        self.assertTrue(started.wait(10))
        halted = CanonicalDispatcher(self.state_path).halt("concurrent halt")
        proceed.set()
        child.join(10)
        self.assertFalse(child.is_alive())
        self.assertEqual(result.get(timeout=2), "STALE_REJECTED")
        self.assertEqual(load_state(self.state_path), halted)

    def test_state_lock_excludes_other_process(self):
        self.fixture()
        ctx = multiprocessing.get_context("fork")
        waiting, acquired, release = ctx.Event(), ctx.Event(), ctx.Event()
        def hold():
            with state_lock(self.state_path):
                acquired.set()
                release.wait(10)
        holder = ctx.Process(target=hold)
        holder.start()
        self.assertTrue(acquired.wait(10))
        result = ctx.Queue()
        def write_waiter():
            waiting.set()
            CanonicalDispatcher(self.state_path).halt("after lock")
            result.put("persisted")
        waiter = ctx.Process(target=write_waiter)
        waiter.start()
        self.assertTrue(waiting.wait(10))
        self.assertEqual(load_state(self.state_path)["phase"], "ASSEMBLY")
        self.assertTrue(result.empty())
        release.set()
        holder.join(10); waiter.join(10)
        self.assertEqual(holder.exitcode, 0)
        self.assertEqual(waiter.exitcode, 0)
        self.assertEqual(result.get(timeout=2), "persisted")
        self.assertEqual(load_state(self.state_path)["phase"], "HALT")

    def test_resume_protected_targets_and_no_arbitrary_jump(self):
        self.fixture()
        dispatcher = CanonicalDispatcher(self.state_path)
        dispatcher.halt("ASSEMBLY interruption")
        for target in ("READY_FOR_UPLOAD", "ASSETS", "UPLOADED"):
            before = self.snapshot()
            with self.assertRaises(DispatcherTransitionError):
                dispatcher.resume_from_halt(target)
            self.assertEqual(before, self.snapshot())
        dispatcher.resume_from_halt("ASSEMBLY")
        self.ready()
        dispatcher.transition("QA")
        dispatcher.halt("QA interruption")
        before = self.snapshot()
        with self.assertRaises(DispatcherTransitionError):
            dispatcher.resume_from_halt("READY_FOR_UPLOAD")
        self.assertEqual(before, self.snapshot())
        dispatcher.resume_from_halt("QA")
        # No synthetic QA PASS: test rejection even for direct protected transition.
        before = self.snapshot()
        with self.assertRaises(DispatcherTransitionError):
            dispatcher.transition("READY_FOR_UPLOAD")
        self.assertEqual(before, self.snapshot())

    def test_fingerprint_covers_all_qa_inputs_and_media(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        state = load_state(self.state_path)
        initial = evidence.validate_final_handoff(self.state_path, state)["input_fingerprint"]
        keys = ("script_path", "script_meta_path", "script_qa_path", "scenes_path",
                "assets_path", "audio_plan_path", "audio_render_path", "resolved_assets_path")
        for key in keys:
            with self.subTest(key=key):
                path = self.root / state["artifacts"][key]
                original = path.read_bytes()
                if path.suffix == ".json":
                    payload = evidence.read_object(path)
                    payload["changed_qa_input"] = True
                    write(path, payload)
                else:
                    path.write_bytes(original + b" new script")
                changed = evidence.validate_final_handoff(self.state_path, state)["input_fingerprint"]
                self.assertNotEqual(initial, changed)
                with self.assertRaises(runner.FlowMindRunPhaseError):
                    runner.validate_qa_receipt(self.state_path, state, changed)
                path.write_bytes(original)
        for path in (self.state_path.parent / "assets/visual.jpg",
                     self.state_path.parent / "audio/segment.mp3"):
            original = path.read_bytes()
            path.write_bytes(original + b" changed")
            self.assertNotEqual(initial, evidence.validate_final_handoff(self.state_path, state)["input_fingerprint"])
            path.write_bytes(original)
        changed = copy.deepcopy(state)
        changed["manifest"]["topic"] = "changed topic"
        changed["manifest"]["manifest_hash"] = compute_manifest_hash(changed["manifest"])
        self.assertNotEqual(initial, evidence.validate_final_handoff(self.state_path, changed)["input_fingerprint"])

    def test_visual_path_change_rejects_previous_render(self):
        self.fixture()
        self.ready()
        path = self.state_path.parent / "assets/another.jpg"
        path.write_bytes(b"another visual")
        plan = evidence.read_object(self.plan_path)
        plan["timeline"][0]["visual_segments"][0]["visual_asset_path"] = str(path)
        write(self.plan_path, plan)
        before = self.snapshot()
        with self.assertRaises(DispatcherTransitionError):
            CanonicalDispatcher(self.state_path).transition("QA")
        self.assertEqual(before, self.snapshot())

    def test_json_format_and_key_order_do_not_invalidate_receipt(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        state = load_state(self.state_path)
        initial = evidence.validate_final_handoff(self.state_path, state)["input_fingerprint"]
        for path in self.state_path.parent.rglob("*.json"):
            payload = json.loads(path.read_text())
            path.write_text(json.dumps(dict(reversed(list(payload.items()))), indent=4))
        self.assertEqual(initial, evidence.validate_final_handoff(self.state_path, load_state(self.state_path))["input_fingerprint"])
        before = self.snapshot()
        runner.handoff_to_qa(self.state_path)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(len(self.executed), 1)

    def test_stale_qa_retry_archives_and_recovers_without_render(self):
        self.fixture()
        runner.handoff_to_qa(self.state_path)
        report = self.state_path.parent / "qa/qa_report.json"
        old = report.read_bytes()
        script = self.root / load_state(self.state_path)["artifacts"]["script_path"]
        script.write_text("Changed isolated script")
        before_state = self.state_path.read_bytes()
        video = self.video_path.read_bytes()
        with self.assertRaises(runner.FlowMindRunPhaseError):
            runner.handoff_to_qa(self.state_path)
        self.assertEqual(before_state, self.state_path.read_bytes())
        with patch.object(runner, "run_phase", side_effect=RuntimeError("interrupted after archive")):
            with self.assertRaises(RuntimeError):
                runner.handoff_to_qa(self.state_path, rerun_stale_qa=True)
        archives = list(report.parent.glob("qa_report.*.json"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].read_bytes(), old)
        runner.handoff_to_qa(self.state_path, rerun_stale_qa=True)
        self.assert_complete()
        self.assertEqual(self.video_path.read_bytes(), video)
        self.assertEqual(len(self.executed), 2)
        self.assertEqual(len(list(report.parent.glob("qa_report.*.json"))), 1)
        before = self.snapshot()
        runner.handoff_to_qa(self.state_path, rerun_stale_qa=True)
        self.assertEqual(before, self.snapshot())

    def test_concurrent_readiness_one_write_and_no_tmp_leak(self):
        self.fixture()
        state_bytes = self.state_path.read_bytes()
        ctx = multiprocessing.get_context("fork")
        go, result = ctx.Event(), ctx.Queue()
        def apply():
            go.wait(10)
            result.put(self.ready()["changed"])
        children = [ctx.Process(target=apply) for _ in range(2)]
        for child in children:
            child.start()
        go.set()
        for child in children:
            child.join(15)
            self.assertEqual(child.exitcode, 0)
        self.assertEqual(sorted([result.get(timeout=2), result.get(timeout=2)]), [False, True])
        self.assertEqual(self.state_path.read_bytes(), state_bytes)
        self.assertEqual(list(self.plan_path.parent.glob("*.tmp")), [])
        before = self.snapshot()
        self.assertFalse(self.ready()["changed"])
        self.assertEqual(before, self.snapshot())

    def test_readiness_failed_postcondition_rolls_back(self):
        self.fixture()
        before = self.snapshot()
        original = readiness.validate_final_handoff
        calls = 0
        def fail_post(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise evidence.FinalHandoffError("postcondition failure")
            return original(*args, **kwargs)
        with patch.object(readiness, "validate_final_handoff", side_effect=fail_post):
            with self.assertRaises(readiness.ApplyFinalRenderReadinessError):
                self.ready()
        self.assertEqual(before, self.snapshot())
        self.assertFalse(evidence.read_object(self.plan_path)["render_ready"])

    def test_real_qa_executor_isolated_contract_and_recovery(self):
        from engine.executors import qa_executor
        state = self.fixture(scenes=6, segments=3, media="shorts")
        # Real QA's existing contracts; no changes to its verdict policy.
        base = self.state_path.parent
        for key in state["artifacts"]:
            state["artifacts"][key] = str(self.root / state["artifacts"][key])
        save_state_atomic(self.state_path, state)
        write(Path(state["artifacts"]["script_qa_path"]), {"verdict": "PASS"})
        scenes, assets, audio_plan, audio_render = [], [], [], []
        for i in range(1, 7):
            scenes.append({"scene_id": f"S{i}", "order": i,
                           "voiceover_text": "Isolated narration", "visual_intent": "Isolated visual",
                           "on_screen_text": "Caption", "asset_type": "image",
                           "estimated_duration_sec": 1, "production_notes": "Isolated notes"})
            assets.append({"asset_id": f"A{i}", "scene_id": f"S{i}", "order": i,
                           "asset_type": "image", "asset_query": "image", "visual_intent": "visual",
                           "usage_role": "primary", "required": True, "provider_status": "resolved",
                           "resolution_status": "ready", "local_path": str(base / "assets/visual.jpg"),
                           "source_provider": "isolated", "source_url": "isolated",
                           "license_status": "cleared", "license_note": "isolated",
                           "production_notes": "isolated"})
            audio_plan.append({"segment_id": f"AUDIO_SEGMENT_{i}", "source_scene_id": f"S{i}",
                               "order": i, "voiceover_text": "Narration", "estimated_word_count": 1,
                               "estimated_duration_sec": 1, "tts_status": "rendered"})
            audio_render.append({"segment_id": f"AUDIO_SEGMENT_{i}", "source_scene_id": f"S{i}",
                                 "order": i, "audio_path": str(base / "audio/segment.mp3"),
                                 "duration_sec": .4, "tts_status": "rendered", "provider_status": "rendered",
                                 "duration_validated": True})
        write(Path(state["artifacts"]["scenes_path"]), {"scene_count": 6, "scenes": scenes})
        write(Path(state["artifacts"]["resolved_assets_path"]),
              {"project_id": state["project_id"], "asset_count": 6, "assets": assets})
        write(Path(state["artifacts"]["audio_plan_path"]), {"audio_segments": audio_plan})
        write(Path(state["artifacts"]["audio_render_path"]),
              {"project_id": state["project_id"], "audio_status": "rendered", "audio_ready": True,
               "duration_validated": True, "loudness_validated": True, "rendered_segment_count": 6,
               "segment_count": 6, "failed_segment_count": 0, "segments": audio_render,
               "missing_requirements": [], "blockers": []})
        def actual_qa(command, *, label):
            self.assertEqual(command[1], "engine/executors/qa_executor.py")
            self.executed.append(command[1])
            result = qa_executor.run_qa_executor(self.state_path)
            self.assertEqual(result["verdict"], "BLOCKED")
            return 0
        video = self.video_path.read_bytes()
        with patch.object(runner, "run_command", side_effect=actual_qa):
            self.assertEqual(runner.handoff_to_qa(self.state_path), 0)
            self.assert_complete()
            old_report = (base / "qa/qa_report.json").read_bytes()
            Path(state["artifacts"]["script_path"]).write_text("Changed narration")
            self.assertEqual(runner.handoff_to_qa(self.state_path, rerun_stale_qa=True), 0)
            self.assert_complete()
            archives = list((base / "qa").glob("qa_report.*.json"))
            self.assertEqual([p.read_bytes() for p in archives], [old_report])
            before = self.snapshot()
            runner.handoff_to_qa(self.state_path, rerun_stale_qa=True)
            self.assertEqual(before, self.snapshot())
        self.assertEqual(self.video_path.read_bytes(), video)
        self.assertEqual(len(self.executed), 2)

    def test_fork_child_does_not_inherit_lock_ownership(self):
        self.fixture()
        ctx = multiprocessing.get_context("fork")
        waiting, acquired = ctx.Event(), ctx.Event()
        def child_lock():
            waiting.set()
            with state_lock(self.state_path):
                acquired.set()
        with state_lock(self.state_path):
            child = ctx.Process(target=child_lock)
            child.start()
            self.assertTrue(waiting.wait(10))
            self.assertFalse(acquired.wait(.1))
        child.join(10)
        self.assertEqual(child.exitcode, 0)
        self.assertTrue(acquired.is_set())

    def test_dispatcher_cli_guard_and_resume_are_fail_closed(self):
        import sys
        from tools import dispatcher_cli
        self.fixture()
        before = self.snapshot()
        with patch.object(sys, "argv", ["dispatcher_cli", "--state", str(self.state_path),
                                       "transition", "--to", "QA"]):
            with self.assertRaises(SystemExit) as result:
                dispatcher_cli.main()
            self.assertEqual(result.exception.code, 2)
        self.assertEqual(before, self.snapshot())
        CanonicalDispatcher(self.state_path).halt("CLI resume check")
        before = self.snapshot()
        with patch.object(sys, "argv", ["dispatcher_cli", "--state", str(self.state_path),
                                       "resume", "--to", "READY_FOR_UPLOAD"]):
            with self.assertRaises(SystemExit) as result:
                dispatcher_cli.main()
            self.assertEqual(result.exception.code, 2)
        self.assertEqual(before, self.snapshot())

    def test_state_store_contract_rejects_immutable_change(self):
        self.fixture()
        state = load_state(self.state_path)
        candidate = copy.deepcopy(state)
        candidate["manifest"]["topic"] = "not a runtime mutation"
        candidate["manifest"]["manifest_hash"] = compute_manifest_hash(candidate["manifest"])
        before = self.snapshot()
        with self.assertRaises(StateValidationError):
            save_state_with_disk_guard(self.state_path, candidate, expected_state=state)
        self.assertEqual(before, self.snapshot())

    def join_without_deadlock(self, process):
        process.join(15)
        if process.is_alive():
            process.terminate()
            process.join(5)
            self.fail("interprocess operation deadlocked")
        self.assertEqual(process.exitcode, 0)

    def stale_active_writer(self, kind, concurrent_phase="HALT"):
        from engine.executors import assembly_executor, final_render_executor
        from tools import apply_assembly_readiness
        self.fixture()
        if concurrent_phase == "QA":
            self.ready()
        original = load_state(self.state_path)
        canonical_before = {path: path.read_bytes() for path in (self.plan_path, self.video_path, self.report_path)}
        for key, filename in (("visual_pacing_plan_path", "visual_pacing.json"),
                              ("audio_loudness_report_path", "loudness.json")):
            path = self.state_path.parent / filename
            write(path, {"project_id": original["project_id"]})
            original["artifacts"][key] = str(path)
        save_state_atomic(self.state_path, original)
        plan = evidence.read_object(self.plan_path)
        timeline = copy.deepcopy(plan["timeline"])
        for scene in timeline:
            scene["visual_segment_count"] = len(scene["visual_segments"])
        beats = [{"scene_id": scene["scene_id"]} for scene in timeline
                 for _ in scene["visual_segments"]]
        duration = sum(scene["audio_duration_sec"] for scene in timeline)
        ctx = multiprocessing.get_context("fork")
        read, proceed, publish_attempt = ctx.Event(), ctx.Event(), ctx.Event()
        result = ctx.Queue()
        def writer():
            module = {"assembly": assembly_executor, "render": final_render_executor,
                      "assembly_readiness": apply_assembly_readiness}[kind]
            def pause_load(path):
                state = load_state(path)
                read.set()
                if not proceed.wait(10):
                    raise RuntimeError("HALT ordering timeout")
                return state
            try:
                with ExitStack() as stack:
                    stack.enter_context(patch.object(module, "REPO_ROOT", self.root))
                    actual_publish = module.publish_artifacts
                    def attempt_publish(*args, **kwargs):
                        publish_attempt.set()
                        return actual_publish(*args, **kwargs)
                    stack.enter_context(patch.object(module, "publish_artifacts", side_effect=attempt_publish))
                    if kind == "assembly":
                        stack.enter_context(patch.object(module, "load_state", side_effect=pause_load))
                        for name, value in (("validate_visual_pacing", (beats, len(timeline), duration)),
                                            ("validate_assets", []), ("validate_resolved_assets", {}),
                                            ("validate_audio_render", {}), ("build_scene_timeline", timeline)):
                            stack.enter_context(patch.object(module, name, return_value=value))
                        module.run_assembly_executor(self.state_path)
                    elif kind == "render":
                        stack.enter_context(patch.object(module, "load_state", side_effect=pause_load))
                        # Only the real publication/state path is exercised. No media executor runs.
                        for name in ("require_tool", "validate_project_ids", "validate_resolved_assets",
                                     "validate_audio_render", "validate_loudness_report",
                                     "print_progress"):
                            stack.enter_context(patch.object(module, name))
                        def existing_video_only(inputs, output, *args):
                            self.assertEqual(output.name, module.FINAL_VIDEO_FILENAME)
                            destination = module.absolute_repo_path(output)
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copyfile(self.video_path, destination)
                        stack.enter_context(patch.object(module, "concat_video_segments", side_effect=existing_video_only))
                        stack.enter_context(patch.object(module, "validate_state", return_value=(original["project_id"], original["artifacts"])))
                        stack.enter_context(patch.object(module, "validate_assembly_plan", return_value=[]))
                        stack.enter_context(patch.object(module, "validate_final_video", return_value=(duration, self.video_path.stat().st_size)))
                        stack.enter_context(patch.object(module, "build_success_report", return_value=evidence.read_object(self.report_path)))
                        stack.enter_context(patch.object(module, "render_visual_segment", side_effect=AssertionError("render forbidden")))
                        module.run_final_render_executor(self.state_path)
                    else:
                        actual_read = module.read_json_file
                        def read_state(path):
                            if (self.root / path).resolve() == self.state_path:
                                return pause_load(self.state_path)
                            return actual_read(path)
                        stack.enter_context(patch.object(module, "read_json_file", side_effect=read_state))
                        stack.enter_context(patch.object(module, "validate_assets_ready"))
                        stack.enter_context(patch.object(module, "validate_audio_ready"))
                        module.apply_assembly_readiness(
                            self.state_path, self.plan_path,
                            Path(original["artifacts"]["resolved_assets_path"]),
                            Path(original["artifacts"]["audio_render_path"]))
                result.put("UNEXPECTED_WRITE")
            except Exception as exc:
                result.put(type(exc).__name__ + ": " + str(exc))
        child = ctx.Process(target=writer)
        child.start()
        self.assertTrue(read.wait(10), "executor did not read fixture state")
        guard_done, commit = ctx.Event(), ctx.Event()
        transition_result = ctx.Queue()
        def advance():
            if concurrent_phase == "HALT":
                CanonicalDispatcher(self.state_path).halt("concurrent executor halt")
            else:
                actual_guard = CanonicalDispatcher._assert_phase_guards
                def paused_guard(dispatcher, *args):
                    actual_guard(dispatcher, *args)
                    guard_done.set()
                    if not commit.wait(10):
                        raise RuntimeError("dispatcher commit ordering timeout")
                with patch.object(CanonicalDispatcher, "_assert_phase_guards", paused_guard):
                    CanonicalDispatcher(self.state_path).transition("QA")
            transition_result.put("STATE_PERSISTED")
        advancer = ctx.Process(target=advance)
        advancer.start()
        if concurrent_phase == "QA":
            self.assertTrue(guard_done.wait(10))
            proceed.set()
            self.assertTrue(publish_attempt.wait(10))
            child.join(.2)
            self.assertTrue(child.is_alive(), "writer must wait for dispatcher state-lock")
            for path, data in canonical_before.items():
                self.assertEqual(path.read_bytes(), data)
            commit.set()
        self.join_without_deadlock(advancer)
        self.assertEqual(transition_result.get(timeout=2), "STATE_PERSISTED")
        protected_bytes = self.state_path.read_bytes()
        proceed.set()
        self.join_without_deadlock(child)
        self.assertIn("stale canonical state", result.get(timeout=2))
        self.assertEqual(self.state_path.read_bytes(), protected_bytes)
        for path, data in canonical_before.items():
            self.assertEqual(path.read_bytes(), data, "stale writer changed canonical artifact")
        current = load_state(self.state_path)
        self.assertEqual(current["phase"], concurrent_phase)
        self.assertEqual(current["phase_history"][-1]["from"], "ASSEMBLY")
        self.assertEqual(current["phase_history"][-1]["to"], concurrent_phase)
        self.assertFalse(current["qa_passed"])
        self.assertFalse(current["approved_for_upload"])
        self.assertEqual(current["approval_status"], "PENDING")

    def test_physical_assembly_writer_rejects_stale_state(self):
        self.stale_active_writer("assembly")

    def test_physical_render_writer_rejects_stale_state_without_render(self):
        self.stale_active_writer("render")

    def test_physical_assembly_readiness_writer_rejects_stale_state(self):
        self.stale_active_writer("assembly_readiness")

    def test_physical_dispatcher_waits_for_readiness_rollback(self):
        self.fixture()
        initial_state = self.state_path.read_bytes()
        initial_plan = self.plan_path.read_bytes()
        ctx = multiprocessing.get_context("fork")
        transient, rollback, attempting, loaded = [ctx.Event() for _ in range(4)]
        ready_result, dispatch_result = ctx.Queue(), ctx.Queue()
        def apply_then_rollback():
            actual = readiness.validate_final_handoff
            calls = 0
            def fail_after_write(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    assert evidence.read_object(self.plan_path)["render_ready"] is True
                    transient.set()
                    if not rollback.wait(10):
                        raise RuntimeError("rollback ordering timeout")
                    raise evidence.FinalHandoffError("controlled postcondition failure")
                return actual(*args, **kwargs)
            try:
                with patch.object(readiness, "validate_final_handoff", side_effect=fail_after_write):
                    self.ready()
                ready_result.put("UNEXPECTED_PASS")
            except readiness.ApplyFinalRenderReadinessError:
                ready_result.put("ROLLED_BACK")
        def transition():
            actual_load = CanonicalDispatcher.load
            def record_read(dispatcher):
                loaded.set()
                return actual_load(dispatcher)
            attempting.set()
            try:
                with patch.object(CanonicalDispatcher, "load", record_read):
                    CanonicalDispatcher(self.state_path).transition("QA")
                dispatch_result.put("UNEXPECTED_QA")
            except DispatcherTransitionError:
                dispatch_result.put("GUARD_REJECTED")
        applier = ctx.Process(target=apply_then_rollback)
        applier.start()
        self.assertTrue(transient.wait(10))
        self.assertTrue(evidence.read_object(self.plan_path)["render_ready"])
        dispatcher = ctx.Process(target=transition)
        dispatcher.start()
        self.assertTrue(attempting.wait(10))
        self.assertFalse(loaded.wait(.2), "dispatcher read transient readiness before state-lock")
        rollback.set()
        self.join_without_deadlock(applier)
        self.join_without_deadlock(dispatcher)
        self.assertEqual(ready_result.get(timeout=2), "ROLLED_BACK")
        self.assertEqual(dispatch_result.get(timeout=2), "GUARD_REJECTED")
        self.assertEqual(self.state_path.read_bytes(), initial_state)
        self.assertEqual(self.plan_path.read_bytes(), initial_plan)

    def test_physical_resume_waits_for_plan_rollback_under_state_lock(self):
        self.fixture()
        self.ready()
        CanonicalDispatcher(self.state_path).halt("resume race fixture")
        halted = self.state_path.read_bytes()
        ctx = multiprocessing.get_context("fork")
        attempting, loaded = ctx.Event(), ctx.Event()
        result = ctx.Queue()
        def resume():
            actual_load = CanonicalDispatcher.load
            def record_read(dispatcher):
                loaded.set()
                return actual_load(dispatcher)
            attempting.set()
            try:
                with patch.object(CanonicalDispatcher, "load", record_read):
                    CanonicalDispatcher(self.state_path).resume_from_halt("QA")
                result.put("UNEXPECTED_QA")
            except DispatcherTransitionError:
                result.put("GUARD_REJECTED")
        with state_lock(self.state_path):
            child = ctx.Process(target=resume)
            child.start()
            self.assertTrue(attempting.wait(10))
            self.assertFalse(loaded.wait(.2), "resume read state outside lock")
            plan = evidence.read_object(self.plan_path)
            plan.update(render_ready=False, missing_requirements=["final render executor"],
                        readiness_status="blocked_by_final_render_executor")
            write(self.plan_path, plan)
        self.join_without_deadlock(child)
        self.assertEqual(result.get(timeout=2), "GUARD_REJECTED")
        self.assertEqual(self.state_path.read_bytes(), halted)

    def test_physical_dispatcher_vs_stale_assembly_publication(self):
        self.stale_active_writer("assembly", "QA")

    def test_physical_dispatcher_vs_stale_readiness_publication(self):
        self.stale_active_writer("assembly_readiness", "QA")

    def test_physical_dispatcher_vs_stale_render_publication(self):
        self.stale_active_writer("render", "QA")

    def test_publication_crash_blocks_guard_and_recovers_old_packet(self):
        from engine import state_store
        import os
        self.fixture()
        self.ready()
        original = load_state(self.state_path)
        before = {path: path.read_bytes() for path in (self.plan_path, self.video_path, self.report_path)}
        stage = self.state_path.parent / ".staging/crash-fixture"
        stage.mkdir(parents=True)
        staged_video, staged_report = stage / "final_video.mp4", stage / "final_render_report.json"
        staged_video.write_bytes(self.video_path.read_bytes())
        report = evidence.read_object(self.report_path)
        report["warnings"] = ["new staged generation"]
        report["source_assembly_plan_digest"] = state_store.artifact_digest(self.plan_path)
        write(staged_report, report)
        staged_plan = stage / "assembly_plan.json"
        staged_plan.write_bytes(self.plan_path.read_bytes())
        ctx = multiprocessing.get_context("fork")
        def crash():
            with patch.object(state_store, "save_state_with_disk_guard", side_effect=lambda *a, **k: os._exit(23)):
                state_store.publish_artifacts(self.state_path, original, expected_state=original,
                    staged={self.video_path: staged_video, self.report_path: staged_report, self.plan_path: staged_plan})
        child = ctx.Process(target=crash)
        child.start(); child.join(15)
        self.assertFalse(child.is_alive())
        self.assertEqual(child.exitcode, 23)
        self.assertTrue((self.state_path.parent / state_store.PUBLICATION_JOURNAL).exists())
        with self.assertRaises(DispatcherTransitionError):
            CanonicalDispatcher(self.state_path).transition("QA")
        self.assertEqual(load_state(self.state_path), original)
        self.assertFalse(load_state(self.state_path)["qa_passed"])
        state_store.recover_artifact_publication(self.state_path)
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data)
        snapshot = self.snapshot()
        state_store.recover_artifact_publication(self.state_path)
        self.assertEqual(snapshot, self.snapshot())
        evidence.validate_final_handoff(self.state_path, load_state(self.state_path))

    def test_publication_receipt_rejects_orphan_and_allows_readiness(self):
        from engine import state_store
        self.fixture()
        original = load_state(self.state_path)
        stage = self.state_path.parent / ".staging/receipt-fixture"
        stage.mkdir(parents=True)
        staged_plan = stage / "assembly_plan.json"
        staged_plan.write_bytes(self.plan_path.read_bytes())
        staged_report = stage / "final_render_report.json"
        report = evidence.read_object(self.report_path)
        report["source_assembly_plan_digest"] = state_store.artifact_digest(staged_plan)
        write(staged_report, report)
        staged_video = stage / "final_video.mp4"
        staged_video.write_bytes(self.video_path.read_bytes())
        state_store.publish_artifacts(self.state_path, original, expected_state=original,
                                     staged={self.plan_path: staged_plan, self.report_path: staged_report,
                                             self.video_path: staged_video})
        self.ready()
        runner.handoff_to_qa(self.state_path)
        before = self.snapshot()
        runner.handoff_to_qa(self.state_path)
        self.assertEqual(before, self.snapshot())
        plan = evidence.read_object(self.plan_path)
        plan["timing_source"] = "changed uncommitted producer"
        write(self.plan_path, plan)
        with self.assertRaises(evidence.FinalHandoffError):
            evidence.validate_final_handoff(self.state_path, load_state(self.state_path))

    def test_partial_publication_crash_recovers_and_after_state_crash_commits(self):
        from engine import state_store
        import os
        for point in ("first_artifact", "after_state"):
            with self.subTest(point=point):
                shutil.rmtree(self.root / "projects", ignore_errors=True)
                self.fixture()
                self.ready()
                original = load_state(self.state_path)
                original_bytes = self.report_path.read_bytes()
                stage = self.state_path.parent / ".staging/partial-fixture"
                stage.mkdir(parents=True)
                staged_report = stage / "final_render_report.json"
                staged_video = stage / "final_video.mp4"
                report = evidence.read_object(self.report_path)
                report["warnings"] = [point]
                report["source_assembly_plan_digest"] = state_store.artifact_digest(self.plan_path)
                write(staged_report, report)
                staged_video.write_bytes(self.video_path.read_bytes())
                staged_plan = stage / "assembly_plan.json"
                staged_plan.write_bytes(self.plan_path.read_bytes())
                ctx = multiprocessing.get_context("fork")
                def child_publish():
                    if point == "first_artifact":
                        actual_replace = os.replace
                        def crash_replace(source, target):
                            actual_replace(source, target)
                            if Path(target) == self.report_path:
                                os._exit(24)
                        context = patch.object(os, "replace", side_effect=crash_replace)
                    else:
                        actual_save = state_store.save_state_with_disk_guard
                        def save_then_crash(*args, **kwargs):
                            actual_save(*args, **kwargs)
                            os._exit(24)
                        context = patch.object(state_store, "save_state_with_disk_guard", side_effect=save_then_crash)
                    with context:
                        state_store.publish_artifacts(self.state_path, original, expected_state=original,
                            staged={self.report_path: staged_report, self.video_path: staged_video, self.plan_path: staged_plan})
                child = ctx.Process(target=child_publish)
                child.start(); child.join(15)
                self.assertFalse(child.is_alive())
                self.assertEqual(child.exitcode, 24)
                with self.assertRaises(DispatcherTransitionError):
                    CanonicalDispatcher(self.state_path).transition("QA")
                state_store.recover_artifact_publication(self.state_path)
                current = load_state(self.state_path)
                self.assertEqual(current["phase"], "ASSEMBLY")
                self.assertFalse(current["qa_passed"])
                self.assertFalse(current["approved_for_upload"])
                if point == "first_artifact":
                    self.assertEqual(current, original)
                    self.assertEqual(self.report_path.read_bytes(), original_bytes)
                else:
                    self.assertIn("artifact_publication", current["artifacts"])
                    self.assertEqual(evidence.read_object(self.report_path)["warnings"], [point])
                evidence.validate_final_handoff(self.state_path, current)
                before = self.snapshot()
                state_store.recover_artifact_publication(self.state_path)
                self.assertEqual(before, self.snapshot())

    def test_published_new_plan_cannot_reuse_old_render_evidence(self):
        from engine import state_store
        self.fixture()
        original = load_state(self.state_path)
        stage = self.state_path.parent / ".staging/new-plan"
        stage.mkdir(parents=True)
        plan = evidence.read_object(self.plan_path)
        plan["director_instruction"] = "new current assembly input"
        staged = stage / "assembly_plan.json"
        write(staged, plan)
        current = state_store.publish_artifacts(self.state_path, original, expected_state=original,
                                               staged={self.plan_path: staged})
        with self.assertRaises(readiness.ApplyFinalRenderReadinessError):
            self.ready()
        self.assertEqual(load_state(self.state_path), current)
        self.assertFalse(load_state(self.state_path)["qa_passed"])

    def test_publication_binding_cannot_be_bypassed_by_dispatcher_patch(self):
        from engine import state_store
        self.fixture()
        stage = self.state_path.parent / ".staging/patch-fixture"
        stage.mkdir(parents=True)
        staged = {}
        for target in (self.plan_path, self.video_path, self.report_path):
            path = stage / target.name
            path.write_bytes(target.read_bytes())
            staged[target] = path
        report = evidence.read_object(staged[self.report_path])
        report["source_assembly_plan_digest"] = state_store.artifact_digest(staged[self.plan_path])
        write(staged[self.report_path], report)
        original = load_state(self.state_path)
        state_store.publish_artifacts(self.state_path, original, expected_state=original, staged=staged)
        self.ready()
        other_report = self.state_path.parent / "other_report.json"
        other_report.write_bytes(self.report_path.read_bytes())
        before = self.snapshot()
        for patch_artifacts in ({"artifact_publication": {"files": {}}},
                                {"final_render_report_path": str(other_report)}):
            with self.assertRaises(DispatcherTransitionError):
                CanonicalDispatcher(self.state_path).transition("QA", artifacts_patch=patch_artifacts)
            self.assertEqual(before, self.snapshot())

    def test_publisher_cannot_advance_phase_or_change_gates(self):
        from engine import state_store
        original = self.fixture()
        stage = self.state_path.parent / ".staging/authority-fixture"
        stage.mkdir(parents=True)
        staged_plan = stage / "assembly_plan.json"
        staged_plan.write_bytes(self.plan_path.read_bytes())
        before = self.snapshot()
        for key, value in (("phase", "QA"), ("qa_passed", True),
                           ("approved_for_upload", True), ("approval_status", "APPROVED")):
            candidate = copy.deepcopy(original)
            candidate[key] = value
            with self.assertRaises(StateValidationError):
                state_store.publish_artifacts(self.state_path, candidate, expected_state=original,
                                             staged={self.plan_path: staged_plan})
            self.assertEqual(before, self.snapshot())

    def test_default_pipeline_unchanged(self):
        self.assertEqual(runner.PHASE_PIPELINES["ASSEMBLY"], (
            "engine/executors/assembly_executor.py", "tools/apply_assembly_readiness.py",
            "engine/executors/final_render_executor.py", "tools/apply_final_render_readiness.py"))
        self.assertFalse(runner.build_parser().parse_args(["--state", "x"]).handoff_to_qa)


if __name__ == "__main__":
    unittest.main(verbosity=2)
