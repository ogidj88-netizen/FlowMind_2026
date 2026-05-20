# FLOWMIND_FIX_BACKLOG

Status: ACTIVE FIX BACKLOG
Mode: SYSTEM MAP MODE

## Purpose

Track known FlowMind gaps found during audit and repair.

Do not fix items immediately unless the active map says this is the current step.

## Rules

- One backlog item must have one clear problem.
- Do not mix active runtime, frozen legacy, and unverified files.
- Do not implement from this file directly.
- Use this file to choose future work after inventory is complete.
- Do not delete resolved or invalid items; change their status and keep evidence.

## Status values

- OPEN
- IMPLEMENTED V1 / VERIFYING
- DONE
- INVALID / REPLACED
- DEFERRED
- ARCHIVED

## Open / active items

### FIX-001: Missing single active command surface

Status: IMPLEMENTED V1 / VERIFYING
Priority: HIGH
Area: nervous system / execution control

Problem:
There was no single active command surface that maps phase -> executor.

Current reality:
- tools/flowmind_run_phase.py exists
- runner requires explicit --state
- runner reads PROJECT_STATE through canonical load_state
- runner maps SCRIPT, SCENES, ASSETS, ASSEMBLY, AUDIO to active executors
- runner refuses QA, READY_FOR_UPLOAD, UPLOADED, ARCHIVED, and HALT
- runner does not auto-transition phase
- runner does not approve upload
- runner does not call legacy module_runner.py
- runner does not call engine/modules/*

Evidence:
- SCRIPT dry-run maps to engine/executors/script_executor.py
- READY_FOR_UPLOAD dry-run fails closed with exit code 2
- preflight passes after adding tools/flowmind_run_phase.py

Remaining:
- add focused smoke tests later
- decide QA-compatible command surface separately
- keep legacy runner frozen

Do not expand yet:
No QA auto-run, no upload, no Telegram, no provider integration.

### FIX-002: Legacy module runner still exists

Status: OPEN
Priority: HIGH
Area: active vs legacy separation

Problem:
engine/module_runner.py routes phases to engine/modules/*.

Current reality:
- engine/module_runner.py maps TOPIC and SCRIPT to engine/modules/*
- registry says engine/module_runner.py must not be active phase runner
- registry says engine/modules/* must not be executed as active runtime

Risk:
It can create a second active contour.

Evidence:
- engine/module_runner.py
- engine/modules/s1_strategy.py
- engine/modules/s2_script.py
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md warnings

Do not fix yet:
Keep frozen until cleanup phase.

### FIX-003: Upload / approval surface missing

Status: OPEN
Priority: MEDIUM
Area: human review / upload gate

Problem:
QA blocks upload correctly, but there is no real human review command surface yet.

Current reality:
- phase is QA
- qa_passed=false
- approved_for_upload=false
- approval_status=PENDING
- QA verdict is BLOCKED by upload_readiness

Risk:
System can render video but cannot complete safe review/upload workflow.

Evidence:
- PROJECT_STATE.json
- qa_report.json
- QA_EXECUTOR_CONTRACT_V1.md

Do not fix yet:
Telegram / YouTube upload are forbidden in current SYSTEM MAP MODE.

### FIX-004: Visual pacing is prototype only

Status: OPEN
Priority: MEDIUM
Area: video quality / renderer

Problem:
Visual pacing technically works but blind motion can make informational cards worse.

Current reality:
- visual_pacing_plan.json exists
- preview video exists
- preview is not production output

Risk:
Adding visual motion blindly can reduce video quality.

Evidence:
- visual pacing preview proof
- user review: video became worse on info-card motion

Do not fix yet:
Video-quality tuning is forbidden until module inventory is complete.

### FIX-005: script_meta is not self-contained

Status: OPEN
Priority: MEDIUM
Area: script executor / artifact contract

Problem:
script_executor creates script.txt and script_meta.json, but script_meta.json does not include script_path or explicit status.

Risk:
Downstream modules may need to depend on PROJECT_STATE or script_qa to locate the script.

Evidence:
- engine/executors/script_executor.py writes script_path to PROJECT_STATE artifacts
- projects/P2026_TEST_001/script/script_meta.json summary showed script_path=None
- projects/P2026_TEST_001/script/script_meta.json summary showed status=None

Do not fix yet:
This belongs to module hardening after inventory is complete.

### FIX-006: script_qa artifact lacks explicit status and blockers

Status: OPEN
Priority: MEDIUM
Area: script QA / gate artifact contract

Problem:
script_qa writes verdict and warnings, but the artifact does not expose explicit status or blockers.

Risk:
Downstream modules may need to infer gate state from missing fields.

Evidence:
- engine/executors/script_qa.py returns status SCRIPT_QA_OK
- projects/P2026_TEST_001/script/script_qa.json summary showed status=None
- projects/P2026_TEST_001/script/script_qa.json summary showed blockers=None

Do not fix yet:
This belongs to module hardening after inventory is complete.

### FIX-007: scenes artifact lacks explicit status and consistent source paths

Status: OPEN
Priority: MEDIUM
Area: scenes executor / director artifact contract

Problem:
scenes_executor creates scenes.json, but the artifact does not expose explicit status, verdict, blockers, or consistent script source path fields.

Risk:
Downstream modules may need to depend on PROJECT_STATE or inconsistent field names.

Evidence:
- engine/executors/scenes_executor.py writes source_script_path and source_script_qa_path
- projects/P2026_TEST_001/scenes/scenes.json summary showed script_path=None
- projects/P2026_TEST_001/scenes/scenes.json summary showed script_meta_path=None
- projects/P2026_TEST_001/scenes/scenes.json summary showed script_qa_path=None
- projects/P2026_TEST_001/scenes/scenes.json summary showed status=None, verdict=None, blockers=None

Do not fix yet:
This belongs to module hardening after inventory is complete.

### FIX-008: assets artifact lacks explicit status and consistent source fields

Status: OPEN
Priority: MEDIUM
Area: assets executor / asset artifact contract

Problem:
assets_executor creates assets.json, but the artifact does not expose explicit status, verdict, blockers, or consistent scenes source path fields.

Risk:
Downstream modules may need to infer asset readiness from missing fields or inconsistent source field names.

Evidence:
- engine/executors/assets_executor.py writes source_scenes_path
- projects/P2026_TEST_001/assets/assets.json summary showed scenes_path=None
- projects/P2026_TEST_001/assets/assets.json summary showed status=None, verdict=None, blockers=None

Do not fix yet:
This belongs to module hardening after inventory is complete.

### FIX-009: asset_resolver zero-assets finding was invalid

Status: INVALID / REPLACED
Priority: LOW
Area: audit accuracy / artifact schema naming

Original problem:
The audit summary claimed asset_resolver produced resolved_assets.json with asset_count=0 and blockers=[].

Corrected reality:
- resolved_assets.json uses the key assets, not resolved_assets
- resolved.asset_count=9
- resolved.assets_len=9
- resolved_count=9
- blocked_count=0
- blockers=[]
- first_provider_status=resolved

Real issue:
The audit summary checked r.get("resolved_assets", []) even though the artifact schema uses assets.

Risk:
False audit findings can cause unnecessary code changes.

Evidence:
- projects/P2026_TEST_001/assets/resolved_assets.json has asset_count=9
- projects/P2026_TEST_001/assets/resolved_assets.json has assets_len=9
- projects/P2026_TEST_001/assets/resolved_assets.json has resolved_count=9
- projects/P2026_TEST_001/assets/resolved_assets.json has blockers=[] because no assets are blocked

Replacement:
No asset_resolver code fix is recommended for this finding.

### FIX-010: legacy s2_script has direct PROJECT_STATE write path

Status: OPEN
Priority: HIGH
Area: legacy containment / state safety

Problem:
engine/modules/s2_script.py can directly write PROJECT_STATE.json using json.dump.

Risk:
If legacy module_runner or engine/modules/s2_script.py is accidentally executed, it can bypass canonical state_store guards.

Evidence:
- engine/modules/s2_script.py contains direct PROJECT_STATE.json write path
- engine/module_runner.py can route SCRIPT to engine/modules/s2_script.py

Do not fix yet:
Keep legacy frozen until cleanup phase.

### FIX-011: hardcoded P2026_TEST_001 defaults exist in tools and executor defaults

Status: IMPLEMENTED V1 / PARTIAL
Priority: MEDIUM
Area: project isolation / multi-project safety

Problem:
Several tools and previously one executor default referenced projects/P2026_TEST_001 directly.

Risk:
Future runs may accidentally operate on the test project instead of an explicit project state path.

Fixed in V1:
- engine/executors/final_render_executor.py no longer has DEFAULT_STATE_PATH for P2026_TEST_001
- final_render_executor.py now requires explicit --state
- running final_render_executor.py without --state exits with argparse error code 2

Remaining:
- apply_* tools still reference P2026_TEST_001
- audio_loudness_report.py still references P2026_TEST_001
- render_visual_pacing_preview.py still references P2026_TEST_001
- elevenlabs_probe_short.py still writes under P2026_TEST_001
- docs still use P2026_TEST_001 as examples/evidence

Evidence:
- commit f83a0da fix: require explicit state for final render executor
- grep in final_render_executor.py shows --state and required=True only
- DEFAULT_STATE_PATH is no longer present in final_render_executor.py
- P2026_TEST_001 is no longer present in final_render_executor.py
- preflight passed after the change

Do not expand yet:
Helper tools cleanup is a separate future scope.

## Current next action

Do not code FIX-009.

Next safe repair target should be chosen from real open items, not invalidated audit findings.

End.
