# MIGRATION ROADMAP V1

Status: LOCKED-DRAFT
Branch: cashflow-mode

## Purpose

This file is the single operational roadmap for migration from the legacy runtime layer to the new canonical dispatcher layer.

This roadmap is for planning and controlled execution only.

It is not permission for ad-hoc runtime rewiring.

## Current architecture reality

There are currently two separate systems in the repository.

Legacy runtime layer:
- main.py
- dispatcher/engine.py
- ExecutionManifest.json
- legacy phase model

New canonical dispatcher layer:
- engine/canonical_dispatcher.py
- tools/dispatcher_cli.py
- tools/dispatcher.sh
- tools/check_dispatcher.sh
- PROJECT_STATE.json
- canonical phase model

## Current verified truth

Verified:
- the new canonical dispatcher works
- canonical PROJECT_STATE bootstrap works
- canonical transitions work
- halt/resume works
- QA and upload guards work
- reproducibility was verified on multiple canonical project states

Also verified:
- main.py is a legacy launcher
- dispatcher/engine.py is a frozen legacy artifact
- dispatcher/engine_v16.py is not a trusted canonical dispatcher
- legacy runtime and canonical dispatcher must not be mixed directly

## Final migration principle

Migration must happen through controlled staged replacement.

Direct runtime switching is forbidden.

Incremental patching of legacy runtime is forbidden.

Dual-write between ExecutionManifest.json and PROJECT_STATE.json is forbidden.

## Single source of truth target

Final target:
- PROJECT_STATE.json becomes the only runtime state source of truth

Legacy artifacts:
- ExecutionManifest.json becomes compatibility-only or archived

## Migration phases

### M0 — Freeze legacy runtime
Goal:
Stop accidental architectural drift.

Rule:
- do not refactor main.py
- do not refactor dispatcher/engine.py
- do not wire canonical dispatcher into legacy runtime
- do not treat legacy files as canonical control surface

Exit condition:
- legacy runtime is documented as frozen
- canonical dispatcher is documented as standalone

### M1 — Phase mapping
Goal:
Define the current best mapping between legacy and canonical phases.

Current state:
- mapping exists
- mapping is still draft-level in unresolved zones

Important:
- no automated translation is allowed yet

Exit condition:
- mapping document exists and reflects audited evidence

### M2 — State model decision
Goal:
Lock the future runtime state model.

Decision:
- PROJECT_STATE.json is the future runtime state source of truth
- ExecutionManifest.json is not the long-term control state

Exit condition:
- this decision is explicitly documented and not contradicted elsewhere

### M3 — Read-only compatibility bridge
Goal:
Allow legacy-side understanding of canonical state without canonical-state corruption.

Rule:
- read-only compatibility is allowed
- legacy runtime must not directly mutate PROJECT_STATE.json
- no bidirectional sync

Exit condition:
- a compatibility concept exists
- no dual-write exists

### M4 — Canonical bootstrap for all new projects
Goal:
All new projects start only through canonical PROJECT_STATE bootstrap.

Rule:
- all new project state creation must use canonical template + bootstrap flow
- legacy project creation path is no longer used for new work

Exit condition:
- new projects are born only in canonical form

### M5 — Canonical manual operator surface
Goal:
Manual human control moves fully to canonical dispatcher.

Rule:
- show / transition / halt / resume / mark-qa-passed / approve-upload
  must be done through tools/dispatcher.sh

Exit condition:
- operators do not use main.py for new dispatcher control

### M6 — New runtime launcher
Goal:
Create a future canonical runtime launcher without mutating legacy runtime internals.

Rule:
- do not evolve dispatcher/engine.py into the new launcher
- build a separate canonical launcher path
- the new launcher must operate only through PROJECT_STATE.json

Exit condition:
- a new launcher exists
- it reproduces canonical lifecycle behavior
- it does not depend on legacy dispatcher internals

### M7 — Legacy decommission
Goal:
Move legacy runtime from active control surface to archived compatibility status.

Rule:
- legacy runtime is no longer primary
- canonical runtime becomes the only active control plane

Exit condition:
- no production control flow depends on main.py or dispatcher/engine.py

## Biggest migration risks

### Risk 1 — Dual source of truth
If ExecutionManifest.json and PROJECT_STATE.json both behave like active runtime state, the system will drift.

Mitigation:
- PROJECT_STATE.json must become the only active target
- no bidirectional sync

### Risk 2 — False phase equivalence
If legacy phases are treated as exact 1:1 canonical matches, migration will become fake-stable and then break.

Mitigation:
- keep confidence labels
- do not automate translation where mapping is not verified

### Risk 3 — Incremental legacy patching
Small convenience patches to main.py or dispatcher/engine.py will create a hybrid system that is harder to kill later.

Mitigation:
- no convenience bridge logic in legacy runtime

### Risk 4 — Operator confusion
If humans use both main.py and tools/dispatcher.sh interchangeably, migration will fail operationally even if code looks correct.

Mitigation:
- manual control surface must be canonical-only for new work

### Risk 5 — Fake upload equivalence
If legacy final QA is mistaken for uploaded state, migration semantics will be wrong at the finish line.

Mitigation:
- treat UPLOADED as canonical-only until proven otherwise

## Current phase mapping truth summary

Strong:
- CREATED -> TOPIC
- S2_DONE -> SCRIPT
- S5_DONE -> ASSETS
- S8_DONE -> ASSEMBLY
- S10_DONE -> QA

Weak or partial:
- S1_DONE -> TOPIC
- S6_DONE -> ASSEMBLY
- S7_DONE -> ASSEMBLY
- S9_DONE -> READY_FOR_UPLOAD

Canonical-only for now:
- SCENES
- HALT
- UPLOADED
- ARCHIVED

## What we are NOT doing now

We are not:
- rewriting main.py
- replacing dispatcher/engine.py
- auto-translating legacy phases
- merging ExecutionManifest.json and PROJECT_STATE.json
- building a dual-runtime bridge with write access

## Immediate next execution target

The next practical migration block is:

M3 preparation:
define the read-only compatibility bridge boundary

This means:
- decide what legacy runtime is allowed to read from canonical state
- decide what legacy runtime is forbidden to write
- describe adapter scope before any implementation

## Final decision

Migration is approved only as staged replacement.

The repository is not ready for direct runtime cutover.

Canonical dispatcher is already valid.

Legacy runtime is not yet retired.
