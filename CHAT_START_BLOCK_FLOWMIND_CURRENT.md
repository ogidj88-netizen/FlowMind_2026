# CHAT_START_BLOCK_FLOWMIND_CURRENT

Status: ACTIVE CHAT START BLOCK
Project: FlowMind / Imagine What If
Mode: SYSTEM MAP MODE

## Current repo state

Branch:
cashflow-mode

Latest confirmed commit:
ce17001 docs: sync human review protocol status

Recent critical commits:
- ce17001 docs: sync human review protocol status
- 759eb44 docs: add human review approval protocol
- 42248c4 docs: add active project source override
- 7660c40 docs: add current chat start block
- b4acdfb docs: update module status after approval bypass fix
- 065f198 docs: record dispatcher approval bypass fix
- ebef6cd fix: block dispatcher transition approval bypass

Repo status at last checkpoint:
clean

## Active mode

SYSTEM MAP MODE.

Do not polish individual module quality yet.
Do not tune video quality yet.
Do not expand upload surface yet.
Do not start YouTube integration.

Current objective:
stabilize system control, state safety, and active contour before module-quality hardening.

## Active contour

Trusted active contour:
- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
- CHAT_START_BLOCK_FLOWMIND_CURRENT.md
- FLOWMIND_ACTIVE_MAP.md
- FLOWMIND_FIX_BACKLOG.md
- FLOWMIND_MODULE_STATUS.md
- FLOWMIND_MODULE_INVENTORY.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- docs/HUMAN_REVIEW_APPROVAL_PROTOCOL_V1.md
- engine/state_validator.py
- engine/state_store.py
- engine/canonical_dispatcher.py
- engine/executors/*
- tools/flowmind_run_phase.py
- tools/dispatcher.sh
- tools/dispatcher_cli.py
- projects/P2026_TEST_001/* active artifacts

Frozen / not active:
- engine/module_runner.py
- engine/modules/*
- old migration docs
- old FM_* projects
- old IronCore / horror rules

Rule:
Do not mix active runtime, frozen legacy, and archive material.

## Current project state

Active test project:
P2026_TEST_001

Current phase:
QA

Current gate state:
- qa_passed=false
- approved_for_upload=false
- approval_status=PENDING
- qa_verdict=BLOCKED
- blocker=upload_readiness

Do not move to READY_FOR_UPLOAD yet.
Do not approve upload yet.
Do not upload to YouTube.

## Command surface status

Command surface:
VERIFIED V1.2

Active runner:
tools/flowmind_run_phase.py

Runner supports:
- SCRIPT
- SCENES
- ASSETS
- ASSEMBLY
- AUDIO
- QA

Runner refuses:
- READY_FOR_UPLOAD
- UPLOADED
- ARCHIVED
- HALT

Runner does not:
- auto-transition phase
- approve upload
- upload to YouTube
- call engine/module_runner.py
- call engine/modules/*

Dispatcher CLI:
tools/dispatcher_cli.py

Dispatcher CLI allows approval mutations only through explicit commands:
- mark-qa-passed
- approve-upload

Dispatcher CLI generic transition no longer exposes:
- --qa-passed
- --approved-for-upload
- --approval-status

## Closed system fixes

FIX-001:
single active command surface is DONE.

FIX-003:
dispatcher transition approval bypass is FIXED.

Human review / approval protocol is DOCUMENTED AS DESIGN-ONLY.

Old bypass:
transition --to READY_FOR_UPLOAD --qa-passed true

Result before fix:
could move tmp QA state to READY_FOR_UPLOAD.

Result after fix:
--qa-passed on transition fails with argparse error.
Tmp state remains:
- phase=QA
- qa_passed=false
- approved_for_upload=false
- approval_status=PENDING

Protocol status:
- docs/HUMAN_REVIEW_APPROVAL_PROTOCOL_V1.md exists
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md lists it as TRUSTED design-only protocol
- FLOWMIND_FIX_BACKLOG.md is synced
- FLOWMIND_MODULE_STATUS.md is synced
- FLOWMIND_MODULE_INVENTORY.md is synced
- protocol does not move state
- protocol does not approve upload
- protocol does not implement YouTube upload

## Current open risks

Most important open risks:
- FIX-002: legacy module_runner still exists
- FIX-003 remaining: approval evidence artifact is not implemented; upload command surface is not implemented; upload remains closed
- FIX-006: script_qa artifact lacks explicit status and blockers in existing active artifact until regenerated
- FIX-007: scenes artifact lacks explicit status and consistent source paths
- FIX-008: assets artifact lacks explicit status and consistent source fields
- FIX-009: asset_resolver can produce weak resolved asset output without strong enough blockers
- FIX-010: legacy s2_script has direct PROJECT_STATE write path
- FIX-011: hardcoded P2026_TEST_001 defaults exist in helper tools

## Current next action

Continue SYSTEM LOGIC AUDIT.

Next safe target:
Read-only inspect stale upload / approval wording in trusted executor contracts before any runtime implementation.

Primary files to inspect:
- docs/QA_EXECUTOR_CONTRACT_V1.md
- docs/FINAL_RENDER_EXECUTOR_CONTRACT_V1.md
- docs/VISUAL_PACING_LAYER_CONTRACT_V1.md
- docs/AUDIO_RENDERER_CONTRACT_V1.md

Goal:
Identify wording that could imply executors, renderers, or visual pacing may set approved_for_upload=true or transition to upload states.

Do not edit these contracts until the stale wording is inspected and classified.

## Forbidden now

- video-quality tuning
- renderer changes
- Telegram integration
- YouTube upload
- Pexels/Pixabay integration
- activating engine/module_runner.py
- executing engine/modules/*
- moving to READY_FOR_UPLOAD
- approving upload
- adding upload automation
- polishing individual module quality beyond system-flow candidate level

## Workflow rule

Work one step at a time.

Do not proceed without user confirmation:
виконано

Do not commit after every small edit.
Commit only at the end of a logical checkpoint.

Files must be changed only by full replacement.
No heredoc.
No partial edits.
No production placeholders or stubs.

End.
