# HUMAN_REVIEW_APPROVAL_PROTOCOL_V1

Status: DESIGN ONLY
Mode: SYSTEM MAP MODE
Scope: FIX-003 human review / approval protocol

## Purpose

Define the minimal human review protocol before FlowMind may mark QA as passed.

This document does not implement upload.

This document does not approve any current project.

This document does not move any project to READY_FOR_UPLOAD.

## Current state

Active project:

P2026_TEST_001

Current phase:

QA

Current gate state:

- qa_passed=false
- approved_for_upload=false
- approval_status=PENDING
- qa_verdict=BLOCKED
- blocker=upload_readiness

## Existing dispatcher facts

The dispatcher already enforces:

- mark-qa-passed can only set qa_passed=true while phase=QA
- transition QA -> READY_FOR_UPLOAD is blocked unless qa_passed=true
- approve-upload can only set approved_for_upload=true while phase=READY_FOR_UPLOAD
- transition READY_FOR_UPLOAD -> UPLOADED is blocked unless approved_for_upload=true

The previous generic transition approval bypass is fixed.

Generic transition must not accept:

- --qa-passed
- --approved-for-upload
- --approval-status

## Human review objective

Human review answers one question:

Is the current generated video package safe and coherent enough to move from QA to READY_FOR_UPLOAD?

This is not final publishing approval.

This is not YouTube upload approval.

This is only approval to enter the READY_FOR_UPLOAD phase.

## Required artifacts before review

Human review may start only if PROJECT_STATE contains all required artifact paths:

- script_path
- script_meta_path
- script_qa_path
- scenes_path
- assets_path
- resolved_assets_path
- audio_plan_path
- audio_render_path
- audio_loudness_report_path
- assembly_plan_path
- visual_pacing_plan_path
- final_video_path
- final_render_report_path
- qa_report_path

If any required artifact path is missing, human review must stop.

## Required review checks

The human reviewer must check:

1. PROJECT_STATE is in phase QA.
2. qa_report exists.
3. final_video_path exists.
4. final video file exists on disk.
5. final render report exists.
6. audio render report exists.
7. audio loudness report exists.
8. resolved assets report exists.
9. license json files exist for selected manual assets.
10. script QA report exists.
11. qa_report does not show critical runtime blockers except upload_readiness.
12. video is playable locally.
13. audio is understandable.
14. video is not empty, broken, black-only, or obviously corrupt.
15. video does not contain production placeholders, stubs, fake output, or DO_NOT_PUBLISH markers.
16. output is acceptable only as system-flow candidate, not final YouTube-quality proof.

## Allowed approval command

If all required review checks pass, the human may run:

./tools/dispatcher.sh --state projects/P2026_TEST_001/PROJECT_STATE.json mark-qa-passed

After that, the human may run:

./tools/dispatcher.sh --state projects/P2026_TEST_001/PROJECT_STATE.json transition --to READY_FOR_UPLOAD

## Not allowed

Human review must not:

- approve upload
- upload to YouTube
- run approve-upload
- transition READY_FOR_UPLOAD -> UPLOADED
- bypass dispatcher
- edit PROJECT_STATE manually
- set qa_passed through generic transition
- set approved_for_upload through generic transition
- use engine/module_runner.py
- execute engine/modules/*
- use old MASTER_PROMPTS_v2_FULL.txt as active authority
- use IronCore v3.5 as active runtime
- treat system-flow candidate quality as final content quality

## Required evidence after review

After mark-qa-passed, verify:

- phase remains QA
- qa_passed=true
- approved_for_upload=false
- approval_status remains PENDING or equivalent non-upload state

After transition to READY_FOR_UPLOAD, verify:

- phase=READY_FOR_UPLOAD
- qa_passed=true
- approved_for_upload=false
- approval_status is not APPROVED for upload

## Exit condition

This protocol is accepted when:

- it is committed as design documentation
- no code is changed
- upload remains closed
- active PROJECT_STATE is not mutated during protocol design
- next implementation step is explicitly approved later

End.
