# FIX_001_COMMAND_SURFACE_DESIGN

Status: DESIGN DRAFT
Target backlog item: FIX-001
Mode: SYSTEM MAP MODE

## Purpose

Define the minimal active command surface for FlowMind.

The goal is to remove manual executor drift without creating a second active runtime contour.

## Problem

FlowMind currently has:

- canonical dispatcher for phase transitions
- executor files that produce artifacts
- guarded PROJECT_STATE updates
- legacy module_runner.py that must not be used

But there is no single active command surface that maps:

PROJECT_STATE.phase -> allowed executor

## Non-goals

This design does not add:

- Telegram
- YouTube upload
- Pexels/Pixabay
- visual quality tuning
- auto-approval
- auto-upload
- strategic thinking inside runner

## Forbidden paths

The active command surface must not call:

- engine/module_runner.py
- engine/modules/*
- legacy s1_strategy.py
- legacy s2_script.py

## Minimal active command

Target command shape:

python tools/flowmind_run_phase.py --state projects/<PROJECT_ID>/PROJECT_STATE.json

The command must:

1. load PROJECT_STATE.json through canonical validation
2. read current phase
3. resolve the allowed executor for that phase
4. execute only that executor
5. fail closed if phase has no executor
6. fail closed if executor returns non-zero
7. not transition phase automatically in v1
8. not approve upload
9. not upload
10. not write state directly

## Phase to executor map v1

SCRIPT -> engine/executors/script_executor.py
SCENES -> engine/executors/scenes_executor.py
ASSETS -> engine/executors/assets_executor.py
ASSEMBLY -> engine/executors/assembly_executor.py
AUDIO -> engine/executors/audio_executor.py
QA -> no single executor in v1 without explicit subcommand

Special QA-compatible executors must stay explicit:

- asset_resolver
- audio_renderer
- final_render_executor
- qa_executor
- visual_pacing_executor

## Why QA is special

Current project reached QA through multiple QA-compatible evidence generators.

Running all QA-compatible executors blindly is unsafe.

Therefore v1 command surface should not auto-run all QA tools.

## Required safety rules

The runner must:

- require explicit --state
- reject missing state file
- reject invalid PROJECT_STATE
- reject HALT unless explicit recovery command exists later
- reject READY_FOR_UPLOAD and UPLOADED in v1
- reject legacy modules
- print exact executor command before running
- return executor exit code
- avoid direct PROJECT_STATE writes

## Success criteria

FIX-001 is ready for implementation only when this design is accepted.

Implementation is complete only when:

- new runner exists
- runner has tests or smoke checks
- legacy module_runner remains unused
- preflight passes
- FLOWMIND_FIX_BACKLOG.md is updated
- FLOWMIND_MODULE_STATUS.md is updated

End.
