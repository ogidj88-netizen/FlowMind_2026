# CHAT_START_BLOCK_FLOWMIND_CURRENT

Status: ACTIVE CHAT START BLOCK
Project: FlowMind / Imagine What If
Mode: SYSTEM MAP MODE

## Current repo state

Branch:
cashflow-mode

Latest confirmed commit:
b4acdfb docs: update module status after approval bypass fix

Recent critical commits:
- b4acdfb docs: update module status after approval bypass fix
- 065f198 docs: record dispatcher approval bypass fix
- ebef6cd fix: block dispatcher transition approval bypass
- f899a55 docs: sync fix backlog after runner qa checkpoint
- e882728 docs: update module status after runner qa checkpoint
- 411f83c fix: allow active runner qa dry-run mapping
- 40a6abf fix: align script executor with retention qa

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
- FLOWMIND_ACTIVE_MAP.md
- FLOWMIND_FIX_BACKLOG.md
- FLOWMIND_MODULE_STATUS.md
- FLOWMIND_MODULE_INVENTORY.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
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

FIX-003 partial:
dispatcher transition approval bypass is FIXED.

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

Important:
Human review / approval protocol is still missing.

## Current open risks

Most important open risks:
- FIX-002: legacy module_runner still exists
- FIX-003: approval bypass fixed, but human review / approval protocol still missing
- FIX-006: script_qa artifact lacks explicit status and blockers in existing active artifact until regenerated
- FIX-007: scenes artifact lacks explicit status and consistent source paths
- FIX-008: assets artifact lacks explicit status and consistent source fields
- FIX-009: asset_resolver can produce weak resolved asset output without strong enough blockers
- FIX-010: legacy s2_script has direct PROJECT_STATE write path
- FIX-011: hardcoded P2026_TEST_001 defaults exist in helper tools

## Current next action

Continue SYSTEM LOGIC AUDIT.

Next safe target:
Design, but do not implement yet, the minimal human review / approval protocol for FIX-003.

The protocol must define:
- what a human reviews
- what evidence must exist before mark-qa-passed
- what command may mark QA as passed
- what command may transition to READY_FOR_UPLOAD
- what is still forbidden
- no upload implementation yet

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
