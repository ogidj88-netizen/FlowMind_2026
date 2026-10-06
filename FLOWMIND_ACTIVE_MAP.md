# FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP
Project: FlowMind / Imagine What If
Updated: 2026-10-05
Mode: PRODUCTION EXECUTION ORDER IMPLEMENTATION MODE

## 1. Purpose

This file is the single current operational authority for FlowMind.

It defines only:

-   current mode
-   current objective
-   current step
-   current allowed work
-   current forbidden work
-   current exit condition
-   current next action

It does NOT define:

-   permanent operating discipline
-   high-level product intent
-   detailed target architecture
-   authority classification
-   control-plane semantics
-   runtime truth
-   historical architecture
-   completed authority-migration history

Those belong to their canonical owners.

------------------------------------------------------------------------

## 2. Current Authority Routing

Permanent operating discipline:
`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Product intent: `FLOWMIND_WORKING_TARGET.md`

Detailed-target identity and classification:
`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Current trusted detailed target: `CURRENT_TRUSTED_DETAILED_TARGET`

Resolved by the Registry as: `FLOWMIND_TARGET_ARCHITECTURE_V3_2.md`

Execution discipline / MAP CHECK / anti-loop:
`docs/FLOWMIND_WORK_PROTOCOL_V1.md`

Control-plane semantics: `CANONICAL_DISPATCHER_SPEC.md`

Current operational authority: `FLOWMIND_ACTIVE_MAP.md`

Runtime truth: verified current repo and runtime evidence

Historical guard:
`docs/FLOWMIND_MAP_GUARD_V1.md`
classification:
FROZEN LEGACY

Historical target:
`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`
classification:
FROZEN LEGACY

------------------------------------------------------------------------

## 3. Current Verified State

Authority System V2 publication is complete.

The V3.2 architecture promotion is complete.

The following remain closed and must not be reopened without new
material evidence:

-   V3.2 architecture review
-   cross-module ownership review
-   contradiction review
-   duplication review
-   internal architecture validation
-   deferred-scope review
-   authority reconciliation
-   authority migration
-   authority publication
-   Project Sources synchronization for the completed authority block

Completed checks remain completed.

A new chat does not reset them.

A historical file remaining in Git does not reset them.

A Project Source filename suffix does not reset them.

Governance work is not the current blocker.

Production reentry gap identification is complete.

Exactly one highest-value implementation target is selected and
authorized:

`PRODUCTION EXECUTION ORDER REPAIR`

Verified runtime evidence established the following implementation gap:

-   the current runtime introduced `AUDIO` as a canonical phase
-   the canonical control contract does not define `AUDIO` as a
    canonical phase
-   canonical audio is required as downstream timing truth
-   exact timed visual execution must derive from actual canonical audio
-   current visual pacing is positioned after final render and depends
    on already-resolved media
-   current asset planning/resolution occurs before
    canonical-audio-driven exact timing
-   current final render is guarded under `QA` even though it creates
    the final video
-   current QA consumes the final video and therefore must remain
    downstream of final render
-   the existing asset resolver/provider layer is reusable and is not
    the current blocker

This is the selected blocker because it prevents a correct real
end-to-end production contour.

The separate QA verdict defect is verified but is NOT part of the
current implementation target.

Durable implementation recovery boundary:

-   selected target status: `IN PROGRESS`
-   last verified implementation boundary:
    `engine/executors/audio_executor.py` v1.2.0
-   verification evidence:
    `AUDIO_EXECUTOR_SCENES_MIGRATION=PASS`, exit=0
-   verified file SHA-256:
    `d7535ac57d4cabfcf9a5cf58768cc04d3fc0c2f53040eb9d15e76423b59307e6`
-   verified result: audio planning is an internal `SCENES` substep; the
    canonical `AUDIO` phase dependency is removed from this executor;
    segment count remains dynamic; the downstream `audio_plan` contract
    is preserved; the executor does not advance canonical phase
-   material NOT DONE state:
    `engine/executors/audio_renderer.py` has NOT been modified for this
    target
-   next unresolved implementation action:
    inspect a fresh current-repo copy of
    `engine/executors/audio_renderer.py` and decide its required boundary
    repair
-   runtime freeze: `YES` while the selected production-order contour is
    cross-file incomplete

This recovery boundary is durable handoff state.

A new chat must recover from this boundary through the active Work
Protocol RECOVERY CHECK and must not restart from `audio_executor.py`.

------------------------------------------------------------------------

## 4. Current Mode

Current mode:

PRODUCTION EXECUTION ORDER IMPLEMENTATION MODE

Purpose:

Repair the verified production execution-order gap using the existing
active contour.

This mode authorizes exactly one implementation target:

`PRODUCTION EXECUTION ORDER REPAIR`

This is not authorization for broad refactoring.

The implementation must preserve:

-   one canonical dispatcher
-   one canonical project state
-   one active production contour
-   existing reusable provider/resolver capabilities
-   explicit artifact contracts
-   evidence-driven validation
-   one-file-at-a-time execution

Intermediate runtime execution is frozen while a changed file is
temporarily incompatible with not-yet-updated files inside this selected
contour.

Do not claim the contour operational until the required cross-file
dependencies are coherent and validated.

------------------------------------------------------------------------

## 5. Current Objective

Current objective:

Restore the production execution order so that the active runtime
follows the trusted production dependency chain without creating a new
canonical phase or a second orchestration contour.

Required canonical lifecycle remains:

TOPIC -\> SCRIPT -\> SCENES -\> ASSETS -\> ASSEMBLY -\> QA -\>
READY_FOR_UPLOAD -\> UPLOADED -\> ARCHIVED

with HALT as the controlled stop state.

`AUDIO` is not a canonical lifecycle phase.

Required production dependency order inside the canonical lifecycle:

SCRIPT -\> Visual Intent / Pass 1 -\> Canonical Audio -\> actual audio
timing -\> Pass 2 / timed execution -\> Media Requirements -\> Media
Resolution -\> Assembly / deterministic final render -\> QA of the
completed final artifact

Operational ownership target:

SCENES -\> Visual Intent / Pass 1 -\> canonical audio
planning/rendering/validation -\> Pass 2 exact timed execution

ASSETS -\> media requirements derived from the timed execution contract
-\> media resolution -\> rights evidence required by the active resolver
contract

ASSEMBLY -\> assembly/readiness -\> deterministic final render -\> final
render readiness

QA -\> evaluate the already-created final artifact

The dispatcher remains the only canonical phase-transition authority.

Internal executors must not silently advance canonical phase.

------------------------------------------------------------------------

## 6. Current Step

Current step:

IMPLEMENT `PRODUCTION EXECUTION ORDER REPAIR`

Target status:

IN PROGRESS

Execution rule:

ONE FILE -\> VERIFY -\> RECORD RESULT -\> NEXT FILE

Last verified implementation substep:

`engine/executors/audio_executor.py`

Result:

PASS

Evidence:

`AUDIO_EXECUTOR_SCENES_MIGRATION=PASS`, exit=0

Current unresolved implementation substep:

`engine/executors/audio_renderer.py`

Material NOT DONE state:

`engine/executors/audio_renderer.py` has not been modified for this
target.

Before modifying this file, use a fresh copy directly from the current
repo.

Required decision question:

Can the existing audio renderer be fully adapted into an internal
`SCENES` substep so that it consumes the dynamic `audio_plan`, renders
the actual planned segment set without a manually configured production
segment-count limit, preserves the downstream `audio_render` contract,
and does not advance canonical phase?

Required result if modification is justified by the fresh file:

-   audio rendering remains an internal `SCENES` production substep
-   it does not require a canonical `AUDIO` phase
-   the render set derives from the actual `audio_plan` segment set
-   production does not depend on `FLOWMIND_AUDIO_RENDER_LIMIT` as a
    scene/segment-count control
-   existing idempotent reuse of valid rendered audio is preserved where
    supported by the verified implementation
-   the downstream `audio_render` artifact contract is preserved
-   the executor does not advance canonical phase

After replacement, if modification is required:

-   syntax must pass
-   phase/input/output contract must pass targeted verification
-   absence of manual production segment-count control must pass targeted
    verification
-   no production runtime chain is executed until the currently edited
    dependency boundary is safe to test

Then proceed to the next file inside the same selected implementation
target based on verified dependency order.

The Active Map does not need to be rewritten between ordinary substeps.
However, before a required new-chat handoff or when chat/context
degradation makes continuation unsafe, create a context recovery
checkpoint according to the active Work Protocol so the last verified
boundary and next unresolved action are durable.

------------------------------------------------------------------------

## 7. Authorized Implementation Contour

The selected target may modify only files directly required to repair
the verified production-order gap.

In-scope runtime components include, when their verified contract
requires modification:

-   `engine/executors/audio_executor.py`
-   `engine/executors/audio_renderer.py`
-   `engine/executors/visual_pacing_executor.py`
-   `engine/executors/assets_executor.py`
-   `engine/executors/assembly_executor.py`
-   `engine/executors/final_render_executor.py`
-   `tools/audio_loudness_report.py`
-   `tools/apply_audio_loudness_report.py`
-   `tools/apply_assembly_readiness.py`
-   `tools/apply_final_render_readiness.py`
-   `tools/flowmind_run_phase.py`
-   `engine/canonical_dispatcher.py`
-   targeted active tests/checks that directly encode the superseded
    `AUDIO` lifecycle or the repaired production-order contract

A file being listed here does not mean it must be changed.

Use:

KEEP MODIFY REMOVE

based on verified current implementation evidence.

Do not modify a component merely because it is in the authorized
contour.

No new production module is authorized unless current evidence proves
the existing contour cannot satisfy the required contract.

------------------------------------------------------------------------

## 8. Current Component Classification

Current evidence supports:

KEEP:

-   existing canonical state mechanism
-   existing dispatcher as the single canonical transition authority
-   existing asset resolver capability
-   existing Pexels provider capability
-   existing deterministic visual provider capability
-   existing audio rendering capability
-   existing loudness validation capability
-   existing final render capability
-   existing QA capability as the downstream consumer of the final
    artifact

MODIFY:

-   audio executor phase/ownership boundary
-   audio renderer phase/ownership boundary
-   visual pacing dependency boundary and timing ownership
-   assets executor upstream contract
-   assembly/final-render execution boundary where required
-   readiness tools whose phase guards encode the old ordering
-   active phase runner orchestration
-   canonical dispatcher runtime implementation that currently contains
    the non-canonical `AUDIO` phase
-   targeted tests/checks that encode the old runtime ordering

REMOVE:

-   `AUDIO` as a canonical runtime phase
-   required production dependence on a manually configured
    scene/segment render count
-   post-final-render ownership of exact visual timing

DEFER:

-   QA hardcoded final verdict defect
-   editorial/script quality tuning
-   provider migration
-   capability benchmarking
-   delivery/upload hardening
-   performance optimization unrelated to this blocker

------------------------------------------------------------------------

## 9. Allowed Actions Now

Allowed:

-   modify only the selected production-order contour
-   work one specific file at a time
-   require a fresh current-repo copy before modifying an existing file
-   perform full-file replacement only
-   run targeted syntax checks after each replacement
-   run the smallest contract check needed to validate the current
    substep
-   inspect an immediately dependent file only when required to avoid an
    unsafe edit
-   preserve already-verified provider/API preflight PASS unless recheck
    conditions are triggered
-   keep runtime execution frozen across temporarily incomplete
    cross-file implementation states
-   run a bounded integration validation after the required dependencies
    become coherent
-   run a clean control replay after the production-order contour is
    coherent
-   commit after the selected implementation block is validated
-   create a bounded context recovery checkpoint before block completion
    only when the active Work Protocol exception is triggered

Default execution:

ONE STEP -\> EVIDENCE -\> VERIFY -\> NEXT STEP

When files are modified:

ONE STEP = ONE SPECIFIC FILE

No batch file editing.

------------------------------------------------------------------------

## 10. Forbidden Actions Now

Do not:

-   reopen authority reconciliation
-   reopen V3.2 architecture review
-   recreate V3.2
-   create V3.3
-   reactivate V3.1
-   reactivate MAP_GUARD
-   modify unrelated governance files
-   create a second dispatcher
-   create a second production contour
-   add `AUDIO` or any other new canonical phase
-   preserve `AUDIO` as canonical lifecycle authority for convenience
-   create a second canonical state
-   add hard-coded scene counts
-   add hard-coded segment counts
-   require `FLOWMIND_AUDIO_RENDER_LIMIT` as a production
    scene/segment-count control
-   derive exact shot timing from estimated scene duration when actual
    canonical audio exists
-   resolve final media before the timed execution/media-requirement
    contract is ready
-   run final render as a QA-owned creative/production operation
-   make QA create the artifact it is supposed to evaluate
-   modify providers merely to solve orchestration
-   start provider migration
-   start capability benchmarking
-   tune script quality or creative quality inside this implementation
    target
-   fix the separate QA hardcoded verdict defect inside this target
-   add infrastructure for future scale
-   activate legacy code without audit
-   use placeholders or stubs in production
-   claim runtime success without runtime evidence
-   run full E2E while the production-order contour is knowingly
    cross-file incomplete

------------------------------------------------------------------------

## 11. Implementation Invariants

The implementation must preserve all of the following:

1.  Canonical lifecycle authority remains owned by the dispatcher.

2.  `AUDIO` is an internal production capability, not a canonical phase.

3.  Pass 1 visual intent exists before canonical audio exact timing is
    required.

4.  Actual canonical audio exists before exact timed Pass 2 execution
    planning.

5.  Exact timing derives from actual canonical audio.

6.  Media requirements are downstream of the timed execution contract.

7.  Media resolution is downstream of media requirements.

8.  Final render consumes ready production artifacts and occurs before
    QA.

9.  QA consumes the completed final artifact.

10. Scene/segment counts are derived from actual project artifacts, not
    manual production constants.

11. Provider/API secrets remain outside code.

12. Existing reusable provider/resolver capability is preserved unless
    runtime evidence proves a specific incompatibility.

13. No executor silently changes canonical phase.

14. Errors are explicit and logged/returned; no empty exception
    handling.

15. Repeated execution must not silently create conflicting canonical
    state.

------------------------------------------------------------------------

## 12. Validation Strategy

Per-file validation:

-   syntax
-   direct phase/input/output contract
-   absence of forbidden hard-coded production counts where relevant
-   no unauthorized canonical phase mutation

Cross-file validation is deferred until the dependencies required for
the repaired contour are coherent.

Then validate:

SCENES -\> canonical audio -\> timed execution -\> ASSETS -\> resolved
media -\> ASSEMBLY -\> final video -\> QA boundary

The first successful integration target is:

a real final video artifact reaches QA through the corrected canonical
lifecycle.

A QA PASS is not required to close this target if the already-verified
separate QA verdict defect is the only remaining blocker.

If that happens:

-   record the production-order target as PASS
-   select the QA verdict defect as the next separate implementation
    target
-   do not mix both fixes into one block

External API preflight follows the active Work Protocol.

Previously verified provider checks remain valid unless their
configuration, account, scope, prior result, or runtime evidence
materially changes.

------------------------------------------------------------------------

## 13. Exit Condition

PRODUCTION EXECUTION ORDER IMPLEMENTATION MODE completes when all of the
following are true:

1.  `AUDIO` is no longer a canonical runtime phase.

2.  canonical audio is produced as an internal production substep before
    exact timed execution.

3.  exact timed execution is produced before media resolution.

4.  media resolution produces the required resolved/licensed media for
    assembly.

5.  final render occurs inside the production/assembly side of the QA
    boundary.

6.  QA receives an already-created final video.

7.  active runner orchestration matches the repaired contour.

8.  dispatcher runtime implementation matches the canonical lifecycle
    contract.

9.  targeted old-order tests/checks are updated or retired based on
    verified active ownership.

10. one clean control replay provides runtime evidence through the QA
    boundary.

11. no second active contour or second canonical state exists.

12. the validated implementation block is committed.

The separate QA verdict defect may remain as the next blocker if it is
the only reason the control replay cannot produce QA PASS.

------------------------------------------------------------------------

## 14. Current Next Action

Current next action:

Continue the selected implementation target from the last verified
boundary with exactly one unresolved runtime file:

`engine/executors/audio_renderer.py`

Current status of that file for this target:

NOT DONE

Before editing:

use a fresh copy directly from the current repo.

Required decision question:

Can the existing audio renderer be fully adapted into an internal
`SCENES` substep so that the render set derives from the actual
`audio_plan`, production does not depend on a manually configured
scene/segment render count, the downstream `audio_render` contract is
preserved, and no canonical phase is advanced?

Do not restart `audio_executor.py` without new material evidence.

Do not edit any other runtime file on this step.

Before a new chat is used for implementation, the context recovery
checkpoint containing the verified `audio_executor.py` boundary and this
Active Map handoff must be committed, pushed, synchronized to Project
Sources where required by the Work Protocol, and recovery-verified.

End.
