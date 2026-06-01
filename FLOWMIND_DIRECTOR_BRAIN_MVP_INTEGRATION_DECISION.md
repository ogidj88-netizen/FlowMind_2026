# FLOWMIND DIRECTOR BRAIN MVP INTEGRATION DECISION

Status: ACTIVE IMPLEMENTATION DECISION  
Project: FlowMind / Imagine What If  
Mode: DIRECTOR BRAIN MVP PREPARATION  
Current technical target: VISUAL PACING PREVIEW TO PRODUCTION RENDER BRIDGE  
Depends on:
- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md
- FLOWMIND_CURRENT_WORK_ANCHOR.md
- FLOWMIND_CURRENT_TO_TARGET_INTEGRATION_MAP.md
- FLOWMIND_FILE_EDIT_PROTOCOL.md

---

## 1. Purpose

This file records the concrete implementation decision after inspecting the current executor surface, active project artifacts, and visual pacing preview renderer.

It defines how Director Brain MVP should be integrated into the existing codebase without creating a second runtime contour.

This file is not a new architecture.

It is a focused implementation decision.

---

## 2. Mandatory file edit rule

All future modifications to this file must follow:

- FLOWMIND_FILE_EDIT_PROTOCOL.md

Mandatory rule:

Full file replacement only.

Forbidden:

- partial edits
- heredoc
- patch-style edits
- append-only changes
- unclear section edits

---

## 3. Confirmed current execution surface

The active production path already has these executor responsibilities:

| Area | Current executor | Current artifact |
|---|---|---|
| Scenes | engine/executors/scenes_executor.py | scenes/scenes.json |
| Assembly | engine/executors/assembly_executor.py | assembly/assembly_plan.json |
| Visual pacing | engine/executors/visual_pacing_executor.py | visual_pacing/visual_pacing_plan.json |
| Final render | engine/executors/final_render_executor.py | final_render/final_video.mp4 + final_render/final_render_report.json |
| Asset resolving | engine/executors/asset_resolver.py | assets/resolved_assets.json |
| Audio render | engine/executors/audio_renderer.py | audio/audio_render.json |
| Visual pacing preview | tools/render_visual_pacing_preview.py | final_render/final_video_visual_pacing_preview.mp4 + final_render/visual_pacing_preview_report.json |

Current runner / dispatcher must not be rewritten for Director Brain MVP.

---

## 4. Confirmed active project runtime state

Active project:

- projects/P2026_TEST_001

Confirmed current production render:

- projects/P2026_TEST_001/final_render/final_video.mp4

Confirmed preview render:

- projects/P2026_TEST_001/final_render/final_video_visual_pacing_preview.mp4

PROJECT_STATE.json already contains paths for:

- scenes_path
- assembly_plan_path
- visual_pacing_plan_path
- final_video_path
- final_render_report_path
- resolved_assets_path
- audio_render_path
- audio_loudness_report_path

Upload remains closed:

- approval_status: PENDING
- approved_for_upload: false
- qa_passed: false

---

## 5. Confirmed runtime finding

Production final render currently renders scene-level output:

- 9 scene-level rendered segments
- final_video.mp4
- final_render_report.json
- renderer: final_render_executor

Visual pacing preview already renders beat-level output:

- 84 beat-level rendered segments
- final_video_visual_pacing_preview.mp4
- visual_pacing_preview_report.json
- executor: render_visual_pacing_preview
- render_mode: visual_pacing_preview_no_drawtext

This is the key discovery.

The system already has a beat-level render proof-of-concept.

The problem is that this beat-level renderer is still preview-only and does not replace or update production final render.

---

## 6. Key technical finding

Final production render is currently driven by:

- assembly_plan.json
- resolved_assets.json
- audio_render.json
- audio_loudness_report.json

There is no confirmed evidence that final_render_executor.py directly consumes:

- visual_pacing_plan.json
- shot_list.json
- director_plan.json

Visual pacing preview is driven by:

- visual_pacing_plan.json

It reads beats, validates beat timing, renders each beat, trims audio by beat timing, applies motion profiles, concatenates beat segments, and writes a preview report.

---

## 7. Main risk

The main integration risk is renderer non-consumption.

Meaning:

Director Brain may create useful planning artifacts, but production final_video.mp4 may remain unchanged if final render does not consume them.

This would be fake progress.

The current evidence confirms this risk:

- visual_pacing_plan.json has 84 beats
- production final render still renders 9 scene segments
- preview render proves beat-level output is possible
- production render does not yet use that beat-level path

---

## 8. Updated integration decision

Do not start with a full Director Engine rewrite.

Do not add a new DIRECTOR phase.

Do not create a new module runtime contour.

Do not create 12 module folders.

Do not rewrite runner or dispatcher.

Do not rewrite final_render_executor.py from scratch.

Next implementation target:

Visual Pacing Preview -> Production Render Bridge

Goal:

Turn the already-proven beat-level preview path into a production-safe render path, or safely integrate its logic into the existing final render flow.

---

## 9. Preferred MVP path

Current proven preview path:

visual_pacing_plan.json
-> tools/render_visual_pacing_preview.py
-> 84 beat segments
-> final_video_visual_pacing_preview.mp4
-> visual_pacing_preview_report.json

Current production path:

assembly_plan.json
-> final_render_executor.py
-> 9 scene segments
-> final_video.mp4
-> final_render_report.json

Target bridge path:

visual_pacing_plan.json
-> production-safe beat-level render
-> final_video.mp4 or explicitly approved production output path
-> final_render_report.json or compatible production report
-> PROJECT_STATE artifact update only when contract is safe

---

## 10. What preview renderer already proves

tools/render_visual_pacing_preview.py already proves:

- visual_pacing_plan.json can drive beat-level render
- beat_count can be greater than scene_count
- beat-level timing can be validated
- source_visual_path can be validated
- source_audio_path can be validated
- motion_profile can affect video filter
- visual_action can affect video filter
- scene audio can be trimmed per beat
- beat segments can be rendered as separate mp4 files
- beat segments can be concatenated into one mp4 file
- preview report can record rendered beat count and segment details

This is useful.

---

## 11. What preview renderer does not yet prove

tools/render_visual_pacing_preview.py does not yet prove production readiness.

Current limitations:

- it is a tool, not a production executor
- it has a default hardcoded plan path for P2026_TEST_001
- it writes preview output, not production output
- it does not update PROJECT_STATE
- it does not replace final_video.mp4
- it does not approve upload
- it disables text overlay
- it writes render_mode: visual_pacing_preview_no_drawtext
- it warns that preview artifact does not replace production final_video.mp4

Therefore it cannot be treated as production output yet.

---

## 12. Practical implementation principle

Use the preview renderer as evidence and as implementation material, not as direct production truth.

The safest first strategy is:

1. preserve current dispatcher / runner
2. preserve upload gate
3. preserve PROJECT_STATE safety
4. extract or adapt beat-level render logic carefully
5. create a production-safe bridge with explicit report and validation
6. prove output quality through manual review

Do not bypass production contracts.

Do not silently replace final_video.mp4 without a safe report and state contract.

---

## 13. Required proof for bridge acceptance

Visual Pacing -> Production Render Bridge is accepted only if:

1. it consumes visual_pacing_plan.json or an equivalent validated beat-level artifact
2. it renders beat-level or shot-aware output
3. it produces a valid mp4 with audio and video streams
4. it preserves duration within allowed drift
5. it produces a production-safe report
6. it does not open upload
7. it does not mark READY_FOR_UPLOAD
8. it does not create a second runtime contour
9. it is validated by preflight or a specific runtime check
10. manual review confirms the output is less PowerPoint-like than baseline

---

## 14. What must be inspected next

Before code changes, inspect exact shared logic opportunities between:

- tools/render_visual_pacing_preview.py
- engine/executors/final_render_executor.py

Need to identify whether the safest path is:

Option A:

Promote preview renderer logic into a production executor path.

Option B:

Extract shared beat rendering helpers and reuse them from final_render_executor.py.

Option C:

Create a dedicated production bridge tool first, then integrate only after proof.

Default recommendation:

Option C first.

Reason:

It avoids destabilizing current final_render_executor.py before proof.

---

## 15. Immediate next technical step

Inspect shared render logic and choose the minimal bridge approach.

Do not code until the exact bridge surface is defined.

Do not modify final_render_executor.py before choosing the bridge strategy.

Do not modify scenes_executor.py before proving the visual pacing bridge cannot solve the current slideshow problem.

---

## 16. Stop rules

Stop if next action:

- adds a DIRECTOR phase
- creates a new runtime contour
- rewrites dispatcher
- rewrites runner
- silently replaces final_video.mp4 without report contract
- changes upload/readiness logic
- marks READY_FOR_UPLOAD
- activates legacy module_runner or engine/modules
- modifies any file without full replacement content
- uses heredoc
- uses partial edits
- treats preview output as production output without validation
- creates planning JSON without downstream consumer

---

## 17. Final decision

Director Brain MVP integration starts with the proven visual pacing runtime path.

The first render-impact implementation target is:

Visual Pacing Preview -> Production Render Bridge

The first proof is not a new document.

The first proof is a production-safe beat-level render that visibly reduces PowerPoint/slideshow feeling without opening upload or creating a second runtime contour.

End.
