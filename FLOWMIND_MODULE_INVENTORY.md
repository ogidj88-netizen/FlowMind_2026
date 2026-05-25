# FLOWMIND_MODULE_INVENTORY

Status: ACTIVE MODULE INVENTORY TABLE
Mode: SYSTEM MAP MODE
Created from runtime grep/audit evidence.

## Purpose

This file maps the active FlowMind module contour.

It records:

- module name
- executor file
- allowed phase
- input artifacts
- output artifacts
- downstream consumer
- runtime proof
- status
- readiness percentage
- next action

This file does not implement module changes.

## Scope rule

This inventory covers active executor-level modules found under:

- engine/executors/
- tools/flowmind_run_phase.py
- projects/P2026_TEST_001/PROJECT_STATE.json artifacts

It does not promote frozen legacy, donor files, archive files, or unverified tooling.

## Current control facts

Active project:

- project_id: P2026_TEST_001
- phase: QA
- qa_passed: false
- approved_for_upload: false
- approval_status: PENDING
- qa_verdict: BLOCKED
- blocker: upload_readiness

Current command surface:

- tools/flowmind_run_phase.py

Runner v1 maps:

- SCRIPT -> engine/executors/script_executor.py
- SCENES -> engine/executors/scenes_executor.py
- ASSETS -> engine/executors/assets_executor.py
- ASSEMBLY -> engine/executors/assembly_executor.py
- AUDIO -> engine/executors/audio_executor.py

Runner v1 refuses:

- QA
- READY_FOR_UPLOAD
- UPLOADED
- ARCHIVED
- HALT

Dispatcher guards verified:

- QA -> READY_FOR_UPLOAD refuses when qa_passed=false
- READY_FOR_UPLOAD -> UPLOADED refuses when approved_for_upload=false

## Active artifact graph

Current PROJECT_STATE artifacts:

- script_path: projects/P2026_TEST_001/script/script.txt
- script_meta_path: projects/P2026_TEST_001/script/script_meta.json
- script_qa_path: projects/P2026_TEST_001/script/script_qa.json
- scenes_path: projects/P2026_TEST_001/scenes/scenes.json
- assets_path: projects/P2026_TEST_001/assets/assets.json
- resolved_assets_path: projects/P2026_TEST_001/assets/resolved_assets.json
- assembly_plan_path: projects/P2026_TEST_001/assembly/assembly_plan.json
- audio_plan_path: projects/P2026_TEST_001/audio/audio_plan.json
- audio_render_path: projects/P2026_TEST_001/audio/audio_render.json
- audio_loudness_report_path: projects/P2026_TEST_001/audio/audio_loudness_report.json
- final_video_path: projects/P2026_TEST_001/final_render/final_video.mp4
- final_render_report_path: projects/P2026_TEST_001/final_render/final_render_report.json
- visual_pacing_plan_path: projects/P2026_TEST_001/visual_pacing/visual_pacing_plan.json
- qa_report_path: projects/P2026_TEST_001/qa/qa_report.json

## Module inventory table

| # | Module | Executor file | Allowed phase | Input artifacts | Output artifacts | Downstream consumer | Runtime proof | Status | Readiness | Next action |
|---:|---|---|---|---|---|---|---|---|---:|---|
| 0 | Foundation / State control | engine/canonical_dispatcher.py, engine/state_validator.py, engine/state_store.py, tools/dispatcher.sh | control layer | PROJECT_STATE.json | guarded state transitions | all phases | QA/upload guards verified; invalid transitions fail closed | TRUSTED | 96% | Keep as control authority; no redesign now |
| 1 | Active phase runner | tools/flowmind_run_phase.py | SCRIPT, SCENES, ASSETS, ASSEMBLY, AUDIO | PROJECT_STATE.json phase | executor command | active executors | phase map verified; refuses unsupported phases | TRUSTED | 94% | Do not expand runner v1 yet |
| 2 | Script | engine/executors/script_executor.py | SCRIPT | PROJECT_STATE manifest | script_path, script_meta_path | script_qa, scenes, audio | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 88% | Later harden script quality and meta contract after inventory |
| 3 | Script QA | engine/executors/script_qa.py | SCRIPT | script_path, script_meta_path | script_qa_path | scenes, assets, assembly, QA | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 84% | Later add explicit status/blockers if still needed |
| 4 | Scenes / Director | engine/executors/scenes_executor.py | SCENES | script_path, script_meta_path, script_qa_path | scenes_path | assets, assembly, visual pacing, QA | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 84% | Later harden source fields/status/verdict/blockers |
| 5 | Assets planning | engine/executors/assets_executor.py | ASSETS | scenes_path, script_qa_path | assets_path | asset_resolver, assembly, QA | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 82% | Later harden asset readiness schema |
| 6 | Asset resolver | engine/executors/asset_resolver.py | QA | assets_path, scenes_path | resolved_assets_path | final_render, visual_pacing, QA | phase guard verified; artifact writes verified | RISKY / NEEDS HARDENING | 72% | Later harden blockers/readiness behavior |
| 7 | Assembly | engine/executors/assembly_executor.py | ASSEMBLY | script_qa_path, scenes_path, assets_path | assembly_plan_path | audio, final_render, visual_pacing, QA | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 85% | Later validate timing/audio-master-clock logic |
| 8 | Audio plan | engine/executors/audio_executor.py | AUDIO | script_path, script_meta_path, script_qa_path, assembly_plan_path | audio_plan_path | audio_renderer, QA | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 86% | Later improve voice/pacing quality |
| 9 | Audio renderer | engine/executors/audio_renderer.py | QA | audio_plan_path | audio_render_path | final_render, visual_pacing, QA | phase guard verified; artifact writes verified | TRUSTED CANDIDATE | 84% | Later confirm provider/runtime cost and loudness path |
| 10 | Final render | engine/executors/final_render_executor.py | implementation-level executor, runner v1 does not map it | assembly_plan_path, resolved_assets_path, audio_render_path, audio_loudness_report_path | final_video_path, final_render_report_path | QA, visual_pacing preview | artifact reads/writes verified; explicit --state required | TRUSTED CANDIDATE | 82% | Do not tune renderer until inventory is complete |
| 11 | Visual pacing | engine/executors/visual_pacing_executor.py | implementation-level executor, runner v1 does not map it | final_video_path, assembly_plan_path, resolved_assets_path, audio_render_path, scenes_path, final_render_report_path | visual_pacing_plan_path | preview/review only | artifact reads/writes verified; quality risk known | PROTOTYPE / RISKY | 60% | Do not tune yet; revisit in VIDEO QUALITY MODE |
| 12 | QA / Readiness | engine/executors/qa_executor.py | QA | script_path, script_meta_path, script_qa_path, scenes_path, assets_path, resolved_assets_path, assembly_plan_path, audio_plan_path, audio_render_path, optional final_video_path | qa_report_path | dispatcher upload gate, design-only human review protocol | phase guard verified; artifact summary consistency verified; human review protocol documented | TRUSTED CANDIDATE | 88% | Later implement approval evidence artifact only after explicit review |
| 13 | Human Review / Upload | docs/HUMAN_REVIEW_APPROVAL_PROTOCOL_V1.md | design-only protocol, not active upload runtime | qa_report_path, final_video_path, qa_passed=false, approved_for_upload=false, approval_status=PENDING | READY_FOR_UPLOAD handoff rules only; UPLOADED remains closed | YouTube/upload later | protocol documented; dispatcher still blocks upload without approval | DESIGN-ONLY / UPLOAD CLOSED | 25% | Do not implement upload; later add approval evidence artifact after review |

## Main findings

The skeleton exists.

The active artifact graph is coherent enough for audit continuation.

The dispatcher/control layer correctly blocks unsafe upload transitions.

The runner v1 is intentionally minimal and does not run QA/upload/final upload phases.

The main remaining operational gap is an approval evidence artifact and upload command surface. Human review rules are documented as design-only; upload remains closed.

The main quality risks remain inside module hardening, not the control skeleton.

## Forbidden next actions

Do not:

- tune video quality
- change renderer behavior
- add Telegram integration
- add YouTube upload automation
- add Pexels/Pixabay integration
- open upload gate
- execute engine/modules/*
- activate engine/module_runner.py
- start module hardening before inventory is committed

## Current next action

Validate the synchronized status docs.

Then run preflight before committing this SYSTEM LOGIC AUDIT checkpoint.

End.
