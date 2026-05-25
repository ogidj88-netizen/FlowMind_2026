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
- IMPLEMENTED V1 / PARTIAL
- DONE
- INVALID / REPLACED
- DEFERRED
- ARCHIVED

## Open / active items

### FIX-001: Missing single active command surface

Status: DONE
Priority: HIGH
Area: nervous system / execution control

Problem:
There was no single active command surface that maps phase -> executor.

Current reality:
- tools/flowmind_run_phase.py exists
- runner requires explicit --state
- runner reads PROJECT_STATE through canonical load_state
- runner maps SCRIPT, SCENES, ASSETS, ASSEMBLY, AUDIO, and QA to active executors
- runner supports QA dry-run
- runner refuses READY_FOR_UPLOAD, UPLOADED, ARCHIVED, and HALT
- runner does not auto-transition phase
- runner does not approve upload
- runner does not upload to YouTube
- runner does not call legacy module_runner.py
- runner does not call engine/modules/*

Evidence:
- SCRIPT dry-run maps to engine/executors/script_executor.py
- QA dry-run maps to engine/executors/qa_executor.py
- READY_FOR_UPLOAD transition still fails closed through dispatcher when qa_passed=false
- dispatcher blocks QA -> READY_FOR_UPLOAD while qa_passed=false
- real PROJECT_STATE stayed unchanged during failed upload gate check
- commit e212793 add active phase runner and freeze legacy runner
- commit 411f83c allow active runner QA dry-run mapping
- commit e882728 updates module status after runner QA checkpoint
- preflight passed after runner changes

Closed scope:
Command surface v1.1 is verified for active execution mapping and QA dry-run mapping.

Not included in this fix:
- approval command surface
- upload command surface
- QA auto-run
- Telegram integration
- YouTube upload

Do not expand here:
Upload / approval belongs to FIX-003.

### FIX-002: Legacy module runner still exists

Status: CONTROLLED / TOMBSTONED
Priority: MEDIUM
Area: active vs legacy separation

Problem:
engine/module_runner.py still exists, but it is no longer an active phase router.

Current reality:
- engine/module_runner.py is a fail-closed tombstone
- engine/module_runner.py prints FLOWMIND_LEGACY_RUNNER_DISABLED
- engine/module_runner.py exits with SystemExit(2)
- active runner does not import engine/module_runner.py
- active runner does not call engine/module_runner.py
- active runner maps phases only to engine/executors/*
- active runner blocks engine/module_runner.py and engine/modules/* through forbidden executor fragments
- registry says engine/module_runner.py must not be active phase runner
- registry says engine/modules/* must not be executed as active runtime

Risk:
Residual legacy files still exist and can confuse operators or future edits, but the active command surface does not route through them.

Evidence:
- engine/module_runner.py fail-closed tombstone
- FLOWMIND_LEGACY_RUNNER_DISABLED message
- SystemExit(2) in engine/module_runner.py
- tools/flowmind_run_phase.py forbids engine/module_runner.py and engine/modules/*
- tools/flowmind_run_phase.py maps active phases only to engine/executors/*
- grep import/call check found no active module_runner import or call outside the forbidden fragment list

Do not fix yet:
Keep tombstoned legacy files frozen until a dedicated cleanup phase.

### FIX-003: Upload / approval surface missing

Status: IMPLEMENTED V1 / PARTIAL
Priority: HIGH
Area: human review / upload gate

Problem:
QA blocks upload correctly, but the approval path was incomplete and unsafe.

Confirmed old risk:
The generic dispatcher transition command allowed approval gate flags to be passed directly.

This created a bypass where:

- transition --to READY_FOR_UPLOAD --qa-passed true

could move a QA state to READY_FOR_UPLOAD without first using the explicit mark-qa-passed command.

Fixed in V1:
- tools/dispatcher_cli.py no longer exposes --qa-passed on generic transition
- tools/dispatcher_cli.py no longer exposes --approved-for-upload on generic transition
- tools/dispatcher_cli.py no longer exposes --approval-status on generic transition
- approval mutations now remain available only through explicit commands:
  - mark-qa-passed
  - approve-upload

Current reality:
- phase is QA
- qa_passed=false
- approved_for_upload=false
- approval_status=PENDING
- QA verdict is BLOCKED by upload_readiness
- dispatcher blocks QA -> READY_FOR_UPLOAD while qa_passed=false
- dispatcher blocks READY_FOR_UPLOAD -> UPLOADED while approved_for_upload=false
- runner supports QA dry-run but does not approve upload
- generic transition approval bypass is blocked by argparse
- failed bypass test leaves tmp state in QA
- active PROJECT_STATE was not mutated during bypass testing

Risk remaining:
Human review / approval protocol is now documented, but it is design-only.
It does not move any project to READY_FOR_UPLOAD.
It does not approve upload.
It does not prove implementation of an approval evidence artifact or upload command surface.

Evidence:
- PROJECT_STATE.json
- qa_report.json
- QA_EXECUTOR_CONTRACT_V1.md
- docs/HUMAN_REVIEW_APPROVAL_PROTOCOL_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md lists docs/HUMAN_REVIEW_APPROVAL_PROTOCOL_V1.md as TRUSTED design-only protocol
- dispatcher failed closed on QA -> READY_FOR_UPLOAD while qa_passed=false
- runner dry-run resolves QA without mutating PROJECT_STATE
- runtime bypass test on /tmp confirmed the old bypass
- commit ebef6cd fix: block dispatcher transition approval bypass
- commit 759eb44 docs: add human review approval protocol
- after ebef6cd, --qa-passed on transition fails with argparse error
- after ebef6cd, tmp state remained phase=QA, qa_passed=false, approved_for_upload=false, approval_status=PENDING
- preflight passed after dispatcher_cli.py change

Fixed in documentation:
- human review checklist
- review command protocol
- READY_FOR_UPLOAD handoff rules
- explicit forbidden actions before upload implementation

Not fixed yet:
- approval evidence artifact
- upload command surface
- YouTube upload

Do not fix yet:
Telegram / YouTube upload are forbidden in current SYSTEM MAP MODE.

Next possible audit target:
Synchronize module status and inventory docs with the design-only human review / approval protocol.

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
Video-quality tuning is forbidden during SYSTEM MAP MODE.

### FIX-005: script_meta is not self-contained

Status: IMPLEMENTED V1 / PARTIAL
Priority: MEDIUM
Area: script executor / artifact contract

Problem:
script_executor created script.txt and script_meta.json, but previous script_meta.json did not include script_path or explicit status.

Current reality:
- script_executor.py now writes script_path
- script_executor.py now writes script_meta_path
- script_executor.py now writes status
- updated SCRIPT chain passed isolated /tmp runtime test
- existing active artifact under projects/P2026_TEST_001 may remain old until regenerated

Risk:
Existing active artifacts may still reflect older schema until SCRIPT is regenerated for the active project.

Evidence:
- commit bdd4bf7 fix: make script meta artifact self-contained
- commit 40a6abf fix: align script executor with retention qa
- isolated /tmp SCRIPT chain passed after executor update

Remaining:
- regenerate active project artifacts only when system phase discipline allows it
- do not mutate active QA project just to refresh historical artifacts

Do not expand yet:
This is not the current system-control blocker.

### FIX-006: script_qa artifact lacks explicit status and blockers

Status: OPEN
Priority: MEDIUM
Area: script QA / gate artifact contract

Problem:
script_qa writes verdict and warnings, but the artifact does not expose explicit status or blockers.

Current reality:
- engine/executors/script_qa.py returns status SCRIPT_QA_OK
- script_qa.json contains verdict, score, checks, failure_reasons, warnings
- existing artifact may not expose explicit status or blockers as top-level fields

Risk:
Downstream modules may need to infer gate state from missing fields.

Evidence:
- engine/executors/script_qa.py returns status SCRIPT_QA_OK
- projects/P2026_TEST_001/script/script_qa.json summary showed status=None
- projects/P2026_TEST_001/script/script_qa.json summary showed blockers=None

Do not fix yet:
This belongs to module hardening after system-control audit.

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
This belongs to module hardening after system-control audit.

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
This belongs to module hardening after system-control audit.

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
- active runner does not call engine/module_runner.py
- active runner does not call engine/modules/*

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

Continue SYSTEM LOGIC AUDIT.

Next safe target:
Synchronize FLOWMIND_MODULE_STATUS.md and FLOWMIND_MODULE_INVENTORY.md with docs/HUMAN_REVIEW_APPROVAL_PROTOCOL_V1.md.

Do not code upload.

Do not open YouTube integration.

Do not auto-approve QA.

Do not move any project to READY_FOR_UPLOAD.

End.
