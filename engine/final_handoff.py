"""Read-only evidence validation shared by readiness, dispatcher and QA.

No renderer, API calls, canonical writes, or fixture-specific dimensions/counts.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

from engine.state_validator import StateValidationError, validate_state
from engine.state_store import assert_published_artifacts, artifact_digest

REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_RENDER_REQUIREMENT = "final render executor"


class FinalHandoffError(StateValidationError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FinalHandoffError(message)


def number(value: Any, name: str, *, positive: bool = True) -> float:
    require(type(value) in (int, float) and math.isfinite(value), f"{name} must be finite")
    require(not positive or value > 0, f"{name} must be positive")
    return float(value)


def project_file(value: Any, state_path: Path) -> Path:
    require(isinstance(value, str) and bool(value.strip()), "artifact path must be non-empty")
    raw = Path(value)
    path = (raw if raw.is_absolute() else REPO_ROOT / raw).resolve()
    require(path.is_relative_to(state_path.parent.resolve()), f"artifact outside project: {value}")
    require(path.is_file() and path.stat().st_size > 0, f"missing or empty artifact: {value}")
    return path


def read_object(path: Path) -> dict[str, Any]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise FinalHandoffError(f"invalid JSON artifact: {path}: {exc}") from exc
    require(isinstance(result, dict), f"JSON artifact must be object: {path}")
    return result


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def structured_digest(path: Path) -> str:
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                        ensure_ascii=False, allow_nan=False).encode()).hexdigest()
    return digest(path)


def probe_video(path: Path) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        require(proc.returncode == 0, f"ffprobe rejected final video: {proc.stderr.strip()}")
        result = json.loads(proc.stdout)
        require(isinstance(result, dict), "ffprobe must return object")
        return result
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        raise FinalHandoffError(f"cannot probe final video: {exc}") from exc


def validate_final_handoff(
    state_path: Path,
    state: Mapping[str, Any],
    *,
    require_ready: bool = True,
) -> dict[str, Any]:
    """Validate one canonical project's current final packet, without mutating it."""
    try:
        return _validate_final_handoff(Path(state_path).resolve(), state, require_ready)
    except FinalHandoffError:
        raise
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise FinalHandoffError(f"invalid final handoff: {exc}") from exc


def _validate_final_handoff(
    state_path: Path, state: Mapping[str, Any], require_ready: bool,
) -> dict[str, Any]:
    state = validate_state(state)
    pid = state["project_id"]
    require(Path(pid).name == pid and pid not in {".", ".."}, "invalid project_id path")
    require(state_path.is_relative_to((REPO_ROOT / "projects").resolve()),
            "state outside canonical projects")
    require(state_path == (REPO_ROOT / "projects" / pid / "PROJECT_STATE.json").resolve(),
            "state path must match canonical project_id")
    assert_published_artifacts(state_path, state)
    artifacts = state["artifacts"]
    plan_path = project_file(artifacts.get("assembly_plan_path"), state_path)
    report_path = project_file(artifacts.get("final_render_report_path"), state_path)
    video_path = project_file(artifacts.get("final_video_path"), state_path)
    plan = read_object(plan_path)
    report = read_object(report_path)
    published = artifacts.get("artifact_publication", {}).get("files", {})
    if "artifact_publication" in artifacts:
        require(all(str(path) in published for path in (plan_path, report_path, video_path)),
                "handoff paths are not bound to current canonical publication")
    if str(plan_path) in published or str(report_path) in published:
        require(report.get("source_assembly_plan_digest") == artifact_digest(plan_path),
                "render evidence is not bound to current published assembly plan")
    require(plan.get("project_id") == report.get("project_id") == pid, "project_id mismatch")
    require(report.get("status") == "FINAL_RENDER_OK" and report.get("verdict") == "PASS",
            "final render must be FINAL_RENDER_OK / PASS")
    require(report.get("final_video_exists") is True, "final_video_exists must be true")
    require(type(report.get("failed_scene_count")) is int and report["failed_scene_count"] == 0,
            "failed_scene_count must be zero")
    require(report.get("blockers") == [], "final render blockers must be empty")
    require(project_file(report.get("final_video_path"), state_path) == video_path,
            "report video path mismatch")
    require(project_file(report.get("source_assembly_plan_path"), state_path) == plan_path,
            "report assembly path mismatch")
    require(project_file(report.get("source_project_state_path"), state_path) == state_path,
            "report state path mismatch")
    source_paths = []
    for key in ("resolved_assets_path", "audio_render_path"):
        source = project_file(artifacts.get(key), state_path)
        require(project_file(report.get("source_" + key), state_path) == source,
                f"report {key} mismatch")
        require(project_file(plan.get("source_" + key), state_path) == source,
                f"assembly {key} mismatch")
        require(read_object(source).get("project_id") == pid, f"source {key} project_id mismatch")
        source_paths.append(source)
    require(plan.get("assets_ready") is True and plan.get("audio_ready") is True,
            "assembly assets/audio must be ready")
    if plan.get("render_ready") is True:
        require(plan.get("missing_requirements") == [] and plan.get("readiness_status") == "render_ready",
                "inconsistent ready assembly")
        require(project_file(plan.get("source_final_render_report_path"), state_path) == report_path,
                "readiness report path mismatch")
        require(project_file(plan.get("source_final_video_path"), state_path) == video_path,
                "readiness video path mismatch")
    else:
        require(not require_ready and plan.get("render_ready") is False,
                "assembly render_ready must be true")
        require(plan.get("missing_requirements") == [FINAL_RENDER_REQUIREMENT],
                "unexpected assembly missing requirements")

    timeline = plan.get("timeline")
    scenes = report.get("scenes")
    require(isinstance(timeline, list) and bool(timeline), "assembly timeline must be non-empty")
    require(isinstance(scenes, list) and len(scenes) == len(timeline), "render scene coverage mismatch")
    for key, payload in (("scene_count", plan), ("scene_count", report),
                         ("rendered_scene_count", report)):
        require(type(payload.get(key)) is int and payload[key] == len(timeline), f"{key} mismatch")
    seen_scenes: set[str] = set()
    seen_segments: set[str] = set()
    expected_duration = 0.0
    segment_count = 0
    audio_paths: set[Path] = set()
    visual_paths: set[Path] = set()
    for index, (scene, rendered) in enumerate(zip(timeline, scenes), 1):
        require(isinstance(scene, dict) and isinstance(rendered, dict), "invalid scene record")
        sid = scene.get("scene_id")
        require(isinstance(sid, str) and bool(sid) and sid not in seen_scenes, "duplicate/invalid scene")
        seen_scenes.add(sid)
        for key in ("scene_id", "timeline_id", "audio_segment_id"):
            require(isinstance(scene.get(key), str) and bool(scene[key])
                    and scene[key] == rendered.get(key), f"render {key} mismatch")
        require(scene.get("order") == rendered.get("order") == index, "scene order mismatch")
        require(rendered.get("render_status") == "rendered", "scene not rendered")
        duration = number(scene.get("audio_duration_sec"), "scene audio duration")
        require(abs(number(rendered.get("audio_duration_sec"), "render audio duration") - duration) < .01,
                "scene duration mismatch")
        require(project_file(scene.get("audio_path"), state_path)
                == project_file(rendered.get("audio_path"), state_path), "scene audio path mismatch")
        audio_paths.add(project_file(scene["audio_path"], state_path))
        expected_duration += duration
        visuals = scene.get("visual_segments")
        rendered_visuals = rendered.get("visual_segments")
        require(isinstance(visuals, list) and bool(visuals) and isinstance(rendered_visuals, list)
                and len(visuals) == len(rendered_visuals), "visual coverage mismatch")
        require(type(rendered.get("visual_segment_count")) is int
                and rendered["visual_segment_count"] == len(visuals), "visual segment count mismatch")
        visual_duration = 0.0
        for visual, output in zip(visuals, rendered_visuals):
            require(isinstance(visual, dict) and isinstance(output, dict), "invalid visual record")
            vid = visual.get("segment_id")
            require(isinstance(vid, str) and bool(vid) and vid not in seen_segments,
                    "duplicate/invalid visual segment")
            seen_segments.add(vid)
            for key in ("segment_id", "asset_id"):
                require(isinstance(visual.get(key), str) and bool(visual[key])
                        and visual[key] == output.get(key), f"visual {key} mismatch")
            visual_path = project_file(visual.get("visual_asset_path"), state_path)
            require(visual_path == project_file(output.get("visual_asset_path"), state_path),
                    "visual_asset_path mismatch")
            visual_paths.add(visual_path)
            require(output.get("render_status") == "rendered", "visual not rendered")
            vd = number(visual.get("duration_sec"), "visual duration")
            visual_duration += vd
            require(abs(number(output.get("expected_duration_sec"), "render visual duration") - vd) < .01,
                    "visual duration mismatch")
        require(abs(visual_duration - duration) <= .05, "visual/audio timeline mismatch")
        segment_count += len(visuals)
    require(type(report.get("visual_segment_count")) is int
            and report["visual_segment_count"] == segment_count, "total visual count mismatch")
    require(abs(number(report.get("expected_duration_sec"), "expected duration") - expected_duration) <= .01,
            "expected duration mismatch")
    final_duration = number(report.get("final_duration_sec"), "final duration")
    delta = number(report.get("duration_delta_sec"), "duration delta", positive=False)
    require(abs(final_duration - expected_duration - delta) <= .01 and abs(delta) <= 1.5,
            "final duration drift mismatch")
    require(type(report.get("final_video_size_bytes")) is int
            and report["final_video_size_bytes"] == video_path.stat().st_size, "video size mismatch")
    probe = probe_video(video_path)
    actual_duration = number(float(probe["format"]["duration"]), "actual video duration")
    require(abs(actual_duration - final_duration) <= .05, "actual video duration mismatch")
    streams = probe.get("streams")
    require(isinstance(streams, list), "missing video streams")
    videos = [stream for stream in streams if stream.get("codec_type") == "video"]
    require(len(videos) == 1 and any(s.get("codec_type") == "audio" for s in streams),
            "final video must contain video and audio")
    profile = report.get("video_profile")
    require(isinstance(profile, dict), "missing video profile")
    require(profile.get("resolution") == f'{videos[0]["width"]}x{videos[0]["height"]}',
            "actual video resolution mismatch")
    audio = next(stream for stream in streams if stream.get("codec_type") == "audio")
    require(profile.get("video_codec") in {videos[0].get("codec_name"),
                                           videos[0].get("codec_name", "") + "/libx264"},
            "actual video codec mismatch")
    require(profile.get("audio_codec") == audio.get("codec_name"),
            "actual audio codec mismatch")
    require(profile.get("pixel_format") == videos[0].get("pix_fmt"),
            "actual pixel format mismatch")
    actual_fps = float(Fraction(videos[0]["r_frame_rate"]))
    require(abs(number(profile.get("fps"), "profile fps") - actual_fps) <= .01,
            "actual fps mismatch")
    require(profile.get("audio_sample_rate") == int(audio["sample_rate"])
            and profile.get("audio_channels") == audio["channels"],
            "actual audio profile mismatch")
    # Exact current QA inputs, not output receipt or mutable transition metadata.
    # These artifact keys are already required by run_qa_executor.
    qa_keys = ("script_path", "script_meta_path", "script_qa_path", "scenes_path",
               "assets_path", "resolved_assets_path", "assembly_plan_path",
               "audio_plan_path", "audio_render_path", "final_video_path")
    qa_files = {key: project_file(artifacts.get(key), state_path) for key in qa_keys}
    referenced = set(audio_paths) | visual_paths
    # QA also checks file existence from resolved assets and audio-render records.
    existence = {}
    for key, records, field in (("resolved_assets_path", "assets", "local_path"),
                                ("audio_render_path", "segments", "audio_path")):
        for record in read_object(qa_files[key]).get(records, []):
            value = record.get(field) if isinstance(record, dict) else None
            if isinstance(value, str) and value.strip():
                raw = Path(value)
                path = (raw if raw.is_absolute() else REPO_ROOT / raw).resolve()
                require(path.is_relative_to(state_path.parent), "QA media outside project")
                existence[str(path.relative_to(REPO_ROOT))] = path.exists()
                if path.is_file():
                    referenced.add(path)
    inputs = {"project_id": pid, "manifest": state["manifest"],
              "qa_passed": state["qa_passed"],
              "approved_for_upload": state["approved_for_upload"],
              "files": {str(path.relative_to(REPO_ROOT)): structured_digest(path)
                        for path in set(qa_files.values()) | {report_path} | referenced},
              "bindings": {key: str(path.relative_to(REPO_ROOT)) for key, path in qa_files.items()},
              "existence": existence}
    fingerprint = hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":"),
                                            ensure_ascii=False, allow_nan=False).encode()).hexdigest()
    return {"assembly_plan": plan, "render_report": report, "video_path": video_path,
            "assembly_plan_path": plan_path, "render_report_path": report_path,
            "input_fingerprint": fingerprint}
