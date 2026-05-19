# FINAL_RENDER_EXECUTOR_CONTRACT_V1

Status: TRUSTED CONTRACT
Version: 1.0.0
Scope: FlowMind final video render executor
Renderer: ffmpeg only
Target project: P2026_TEST_001

## 1. Purpose

Final Render Executor creates the first real final video artifact from an already validated FlowMind project.

It must produce a real playable MP4 video and a machine-readable render report.

Required outputs:
- `projects/P2026_TEST_001/final_render/final_video.mp4`
- `projects/P2026_TEST_001/final_render/final_render_report.json`

Required PROJECT_STATE updates after success:
- `artifacts.final_video_path`
- `artifacts.final_render_report_path`

Forbidden:
- fake success
- placeholder outputs
- dummy outputs
- stub outputs
- text-only proof without real video

## 2. Current upstream truth

This executor is allowed to run only after the upstream pipeline has already produced valid inputs.

Expected verified state before final render:
- `PROJECT_STATE.phase = "QA"`
- `audio_render.audio_status = "ready"`
- `audio_render.audio_ready = true`
- `audio_render.duration_validated = true`
- `audio_render.loudness_validated = true`
- `audio_render.failed_segment_count = 0`
- `audio_render.blockers = []`
- `audio_render.missing_requirements = []`
- `assembly_plan.assets_ready = true`
- `assembly_plan.audio_ready = true`
- `assembly_plan.render_ready = false`
- `assembly_plan.missing_requirements = ["final render executor"]`

Important:
- `render_ready = false` is correct before this executor runs.
- This executor closes the last render blocker by producing the final MP4 artifact.

## 3. Renderer decision

Final Render Executor v1 uses:
- `ffmpeg`
- `ffprobe`

Remotion is not used in v1.

Reason:
- all required visual assets already exist locally
- all required audio segments already exist locally
- ffmpeg and ffprobe are already available
- local ffmpeg render is the fastest stable proof of execution
- Remotion can be introduced later after baseline rendering is proven

## 4. Non-goals

This executor must not:
- call ElevenLabs
- call OpenAI
- call any external media API
- download new assets
- rewrite script
- rewrite scenes
- modify source visual assets
- modify source audio segments
- approve upload
- set `qa_passed = true`
- set `approved_for_upload = true`
- claim completion if final video is missing or invalid

## 5. Required inputs

The executor reads canonical paths from `PROJECT_STATE.artifacts`.

Required artifact keys:
- `assembly_plan_path`
- `resolved_assets_path`
- `audio_render_path`
- `audio_loudness_report_path`

The executor must fail closed if:
- any required artifact key is missing
- any artifact path is empty
- any artifact file does not exist
- any required JSON is invalid

## 6. Source of truth

The executor must use these files as canonical truth:

From `assembly_plan.json`:
- `timeline`
- `scene_count`
- `target_duration_sec`

From `resolved_assets.json`:
- resolved visual asset records
- local media paths
- license and resolution statuses

From `audio_render.json`:
- rendered audio segment records
- `audio_path`
- `duration_sec`
- `duration_validated`
- segment order and scene linkage

From `PROJECT_STATE.json`:
- artifact registry
- project id
- current phase

The executor must not trust stale planning placeholders if they disagree with resolved artifacts.

## 7. Required pre-run validation

The executor must validate all of the following before rendering:

State checks:
- `PROJECT_STATE.phase == "QA"`

Assembly checks:
- `assembly_plan.assets_ready == true`
- `assembly_plan.audio_ready == true`
- `assembly_plan.render_ready == false`
- `assembly_plan.missing_requirements == ["final render executor"]`

Audio checks:
- `audio_render.audio_ready == true`
- `audio_render.audio_status == "ready"`
- `audio_render.duration_validated == true`
- `audio_render.loudness_validated == true`
- `audio_render.failed_segment_count == 0`
- `audio_render.blockers == []`
- `audio_render.missing_requirements == []`

Loudness report checks:
- loudness report exists
- loudness report says validation passed
- project id matches

If any validation fails, executor must stop before rendering.

## 8. Required visual asset checks

Every resolved asset used for final render must contain:
- `asset_id`
- `scene_id`
- `order`
- `asset_type`
- `local_path`
- `provider_status`
- `license_status`
- `resolution_status`

Required visual asset states:
- `provider_status = "resolved"`
- `license_status = "cleared"`
- `resolution_status = "ready"`

The file at `local_path` must:
- exist
- be non-empty
- be readable

Allowed visual media types for v1:
- image: `.png`, `.jpg`, `.jpeg`, `.webp`
- video: `.mp4`, `.mov`, `.mkv`

Any unsupported or unreadable asset must fail the executor.

## 9. Required audio checks

Every rendered audio segment used for final render must contain:
- `segment_id`
- `source_scene_id`
- `order`
- `audio_path`
- `duration_sec`
- `tts_status`
- `provider_status`
- `duration_validated`

Required audio segment states:
- `tts_status = "rendered"`
- `provider_status = "rendered"`
- `duration_validated = true`
- `duration_sec > 0`

The file at `audio_path` must:
- exist
- be non-empty
- be readable by ffprobe

The executor must use only the rendered MP3 files as voiceover truth.

If a visual MP4 contains its own audio track, that embedded audio must be ignored.

## 10. Scene matching rule

The executor must build final render pairs by matching timeline entries with both:
- one visual asset
- one audio segment

Matching constraints:
- `timeline.scene_id == resolved_asset.scene_id`
- `timeline.asset_id == resolved_asset.asset_id`
- `timeline.scene_id == audio_segment.source_scene_id`
- `timeline.order == audio_segment.order`

The executor must fail if:
- a timeline item has no matching visual asset
- a timeline item has no matching audio segment
- duplicate visual matches exist
- duplicate audio matches exist
- order mismatch exists
- scene count mismatch exists

No guessing or fuzzy fallback is allowed.

## 11. Render strategy

The executor renders one intermediate scene video per timeline item.

For image assets:
- loop the image for the duration of the matching audio segment
- scale and pad to 1920x1080
- combine with the matching MP3
- encode to MP4

For video assets:
- use the video as visual-only input
- ignore original embedded audio
- trim or loop visual content to match the duration of the matching audio segment
- scale and pad to 1920x1080
- combine with the matching MP3
- encode to MP4

Audio duration is authoritative for each scene.

The executor must not:
- rewrite voiceover text
- stretch audio unnaturally
- truncate audio
- replace audio with silence unless the scene is intentionally silent, which is not the case for this project

## 12. Output directories

The executor writes final outputs under:
- `projects/P2026_TEST_001/final_render/`

Allowed executor-owned paths:
- `projects/P2026_TEST_001/final_render/final_video.mp4`
- `projects/P2026_TEST_001/final_render/final_render_report.json`
- `projects/P2026_TEST_001/final_render/segments/`
- `projects/P2026_TEST_001/final_render/tmp/`

The executor may overwrite only files under its own final render directory.

## 13. Video profile

Final video requirements:
- container: MP4
- video codec: H.264 via `libx264`
- audio codec: AAC
- resolution: 1920x1080
- frame rate: 30 fps
- pixel format: `yuv420p`
- audio sample rate: 48000 Hz
- audio channels: stereo

The final video file must:
- exist
- be non-empty
- contain a readable video stream
- contain a readable audio stream
- be accepted by ffprobe
- have duration greater than zero

## 14. Duration validation

Each scene render must be validated with ffprobe after encoding.

Allowed per-scene duration drift:
- maximum absolute drift: `0.50` seconds

Expected scene duration source:
- matching audio segment `duration_sec`

Final video duration must approximately equal the sum of scene audio durations.

Allowed final total drift:
- maximum absolute drift: `1.50` seconds

If duration validation fails:
- executor fails
- final render must not be marked PASS

## 15. Concatenation rule

After all scene segments are rendered and validated:
- generate a deterministic concat list
- concatenate scene segments strictly in timeline order
- produce `final_video.mp4`

Required order source:
- `assembly_plan.timeline.order`

The concat list must be stored in executor-owned temp space under `final_render/tmp/`.

## 16. Final render report schema

`final_render_report.json` must be a JSON object.

Required top-level fields:
- `project_id`
- `renderer`
- `renderer_version`
- `status`
- `verdict`
- `final_video_path`
- `final_video_exists`
- `final_video_size_bytes`
- `final_duration_sec`
- `expected_duration_sec`
- `duration_delta_sec`
- `scene_count`
- `rendered_scene_count`
- `failed_scene_count`
- `video_profile`
- `source_project_state_path`
- `source_assembly_plan_path`
- `source_resolved_assets_path`
- `source_audio_render_path`
- `segments`
- `warnings`
- `blockers`
- `created_at`

Successful final render must use:
- `status = "FINAL_RENDER_OK"`
- `verdict = "PASS"`
- `final_video_exists = true`
- `failed_scene_count = 0`
- `blockers = []`

Failed final render must use:
- `status = "FINAL_RENDER_FAIL"`
- `verdict = "FAIL"`

## 17. Per-scene report schema

Each item in `final_render_report.segments` must include:
- `timeline_id`
- `scene_id`
- `order`
- `asset_id`
- `visual_asset_path`
- `visual_asset_type`
- `audio_segment_id`
- `audio_path`
- `scene_video_path`
- `scene_duration_sec`
- `audio_duration_sec`
- `duration_delta_sec`
- `render_status`
- `error_message`

Successful scene render must use:
- `render_status = "rendered"`
- `error_message = null`

Failed scene render must use:
- `render_status = "failed"`

## 18. PROJECT_STATE update rule

After successful final render, executor may update only:
- `PROJECT_STATE.artifacts.final_video_path`
- `PROJECT_STATE.artifacts.final_render_report_path`
- `PROJECT_STATE.updated_at`

The executor must not directly change:
- `PROJECT_STATE.phase`
- `PROJECT_STATE.qa_passed`
- `PROJECT_STATE.approved_for_upload`

QA ownership stays outside this executor.

## 19. Assembly update rule

This executor must not directly edit assembly readiness fields.

A separate sync/apply tool may later set:
- `assembly_plan.render_ready = true`
- `assembly_plan.missing_requirements = []`
- `assembly_plan.readiness_status = "render_ready"`

But only after:
- `final_video.mp4` exists
- `final_render_report.verdict = "PASS"`

## 20. Idempotency rule

The executor must be safe to rerun.

It may overwrite:
- final render outputs
- executor-owned temp files
- executor-owned scene segment outputs

It must not modify:
- `manual_assets/*`
- `audio/rendered_segments/*`
- `assets/resolved_assets.json`
- `audio/audio_render.json`
- `audio/audio_loudness_report.json`
- `assembly/assembly_plan.json`

If a rerun happens, new output should replace old final render artifacts deterministically.

## 21. Failure policy

The executor must fail closed.

On failure:
- exit non-zero
- print explicit failure reason to stderr
- do not set final video artifact paths unless final validation passed
- do not claim PASS
- do not claim upload-ready
- do not mutate QA approval state

Partial temp files may remain for debugging, but failure must be explicit.

## 22. Runtime dependencies

Required runtime tools:
- `python3`
- `ffmpeg`
- `ffprobe`

No new Python dependency stack is required for v1.

If `ffmpeg` or `ffprobe` is missing, executor must stop before any render attempt.

## 23. Security and network policy

Final render v1 is local-only.

The executor must not:
- read secrets from `.env` unless strictly required for local path resolution, which it is not
- call network APIs
- print secrets
- depend on internet access

## 24. Forbidden markers

The executor must reject known non-production markers in generated JSON/text outputs.

Forbidden markers:
- `PLACEHOLDER`
- `STUB`
- `STUBBED`
- `DO_NOT_PUBLISH`
- `TODO`
- `FAKE_OUTPUT`
- `LOREM IPSUM`
- `TEST ONLY`
- `DUMMY`
- `MOCK`

Binary video files are not scanned as text, but JSON/text outputs must remain clean.

## 25. Verified current project evidence

Verified project state for `P2026_TEST_001`:
- visual assets exist: 9 of 9
- audio segments rendered: 9 of 9
- audio loudness validated: PASS
- audio layer status: ready
- assembly assets_ready: true
- assembly audio_ready: true
- assembly render_ready: false
- final remaining requirement before executor: `final render executor`

Known visual assets:
- `ASSET_001` image
- `ASSET_002` image
- `ASSET_003` video
- `ASSET_004` image
- `ASSET_005` image
- `ASSET_006` video
- `ASSET_007` video
- `ASSET_008` image
- `ASSET_009` image

Known audio segment count:
- 9

Known total rendered audio duration:
- approximately `390.505` seconds

## 26. Minimal execution plan

Final Render Executor v1 should execute in this order:
1. load `PROJECT_STATE.json`
2. load `assembly_plan.json`
3. load `resolved_assets.json`
4. load `audio_render.json`
5. load `audio_loudness_report.json`
6. validate project ids and required fields
7. validate ffmpeg and ffprobe availability
8. validate all visual assets
9. validate all audio segments
10. build deterministic scene map
11. render one MP4 scene segment per timeline item
12. validate each scene segment with ffprobe
13. concatenate scene segments in order
14. validate final MP4
15. write `final_render_report.json`
16. update `PROJECT_STATE.artifacts`
17. print final JSON result

## 27. Exit condition

Final Render Executor v1 is complete only when all of the following are true:
- `final_video.mp4` exists
- `final_video.mp4` is non-empty
- ffprobe successfully reads `final_video.mp4`
- `final_render_report.json` exists
- `final_render_report.verdict = "PASS"`
- `final_render_report.failed_scene_count = 0`
- `PROJECT_STATE.artifacts.final_video_path` exists
- `PROJECT_STATE.artifacts.final_render_report_path` exists

Until then, final render is not complete.

## 28. Final implementation target

Implementation file:
- `engine/executors/final_render_executor.py`

Required v1 outputs:
- `projects/P2026_TEST_001/final_render/final_video.mp4`
- `projects/P2026_TEST_001/final_render/final_render_report.json`

Accepted v1 approach:
- minimal local ffmpeg renderer
- real media output only
- no stubs
- no fake PASS
- no Remotion in v1
- no upload in v1
