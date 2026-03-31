# READ-ONLY COMPATIBILITY BRIDGE

Status: LOCKED-DRAFT
Branch: cashflow-mode

## Purpose

This document defines the allowed and forbidden boundaries for the future read-only compatibility bridge between:

- legacy runtime layer
- canonical dispatcher layer

This is a planning/control document.
It does not authorize direct implementation without a dedicated migration step.

## Core principle

The bridge must be read-only from the perspective of legacy runtime.

Canonical state must remain protected.

PROJECT_STATE.json must not be mutated by legacy runtime code.

## Source of truth rule

For migration v1:

- PROJECT_STATE.json is the only target runtime state model
- ExecutionManifest.json is not allowed to become a second active state authority
- legacy runtime may consume derived/read-only information only

## What legacy runtime is allowed to read

Legacy-side read access may include only the following categories:

1. Project identity
- project_id

2. Canonical phase snapshot
- current canonical phase
- phase_history as read-only information
- halted status as read-only information

3. Canonical manifest metadata
- manifest_id
- manifest_version
- mode
- niche
- audience
- content_language
- primary_platform
- topic
- working_title
- hook
- target_duration_sec
- render_profile
- stock_policy
- created_at
- locked

4. Canonical runtime flags
- approval_status
- qa_passed
- approved_for_upload

5. Canonical artifact metadata
- artifact paths
- final_video_path if present
- other future artifact references as read-only metadata only

## What legacy runtime is forbidden to write

Legacy runtime must never write directly to:

- PROJECT_STATE.json
- manifest.manifest_hash
- manifest.manifest_version
- manifest.locked
- phase
- phase_history
- halted
- halt_reason
- resume_hint
- approval_status
- qa_passed
- approved_for_upload
- artifacts
- any future canonical state control field

## What legacy runtime is forbidden to decide

Legacy runtime must not become the authority for:

- canonical phase transitions
- canonical halt/resume decisions
- canonical qa_passed decision
- canonical approve-upload decision
- canonical upload state
- canonical archive state
- canonical manifest mutation

## Allowed bridge output shape

The bridge may expose a derived compatibility view such as:

- legacy-readable summary object
- canonical phase snapshot translated for analysis only
- compatibility metadata for dashboards or diagnostics
- read-only adapter payload

The bridge must not expose a writable compatibility contract that can be pushed back into canonical state.

## Forbidden bridge designs

The following are forbidden:

1. Bidirectional sync
2. Dual write between ExecutionManifest.json and PROJECT_STATE.json
3. Legacy-triggered mutation of canonical state
4. Silent phase translation with persistence
5. “Temporary” convenience writes into canonical state from legacy code
6. Any bridge that makes legacy runtime an equal state authority

## Operational rule

If legacy runtime needs canonical information, it must receive it through:

- read-only adapter output
- derived snapshot
- compatibility payload

It must not receive write privileges.

## Minimal safe bridge idea

The minimal safe bridge for migration v1 is:

- input: PROJECT_STATE.json
- processing: read + derive compatibility snapshot
- output: read-only legacy-facing representation

No reverse path.

## Exit condition for M3

M3 can be considered prepared only when:

1. read-only boundary is explicitly documented
2. forbidden write paths are explicitly documented
3. source-of-truth rule is explicit
4. no implementation contradicts this policy

## Current decision

For migration v1:

- read-only compatibility is allowed in principle
- write-back from legacy runtime is forbidden
- canonical dispatcher remains the only valid control authority for canonical state
