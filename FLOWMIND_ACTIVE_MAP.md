FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP Project: FlowMind / Imagine What If
Updated: 2026-10-07 Mode: PRODUCTION EXECUTION ORDER REPAIR

1. Purpose

This file is the single current operational and recovery checkpoint for
FlowMind.

It answers only:

-   what target is active
-   what is currently paused or allowed
-   what has been verified
-   what materially remains NOT DONE
-   what is deferred
-   what exit conditions remain
-   what the next logical action is
-   what durable evidence anchors recovery

Permanent operating/execution rules belong to:

FLOWMIND_CORE_RULES.md

This file does not duplicate those rules.

2. Authority Routing

Permanent operating/execution rules: FLOWMIND_CORE_RULES.md

Current operational/recovery state: FLOWMIND_ACTIVE_MAP.md

Product intent: FLOWMIND_WORKING_TARGET.md

Authority classification and reference routing:
FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Detailed architecture: CURRENT_TRUSTED_DETAILED_TARGET as resolved by
the Registry

Control-plane semantics: CANONICAL_DISPATCHER_SPEC.md

Runtime truth: verified current repo and runtime evidence

Compatibility during the current governance migration:

-   000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md -> transitional pointer
    to FLOWMIND_CORE_RULES.md
-   docs/FLOWMIND_WORK_PROTOCOL_V1.md -> transitional reference /
    compatibility document

Historical authorities remain historical unless the Registry explicitly
classifies otherwise.

3. Governance Closure State

Governance transaction:

AUTHORITY SIMPLIFICATION / GOVERNANCE COMPACTION

Status:

COMPLETED / PUBLISHED / RECOVERY VERIFIED

Purpose achieved:

- FLOWMIND_CORE_RULES.md is the single owner of permanent operating and
  execution discipline
- FLOWMIND_ACTIVE_MAP.md is the single current-state/recovery checkpoint
- duplicate active governance ownership has been removed
- new-chat recovery is compact and deterministic
- specialized reference authorities remain available without being reread
  by default

Verified governance closure evidence:

- FLOWMIND_CORE_RULES.md created and validated
- logical-action execution rule added to FLOWMIND_CORE_RULES.md
- large replacement content is delivered as .txt by default
- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md compacted to a transitional
  compatibility pointer and validated
- docs/FLOWMIND_WORK_PROTOCOL_V1.md compacted to a transitional reference /
  compatibility document and validated
- FLOWMIND_ACTIVE_MAP.md compacted into the single operational/recovery
  checkpoint and validated
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md reconciled to the simplified
  authority model and validated
- targeted active-authority dependency/reference scan completed
- CANONICAL_DISPATCHER_SPEC.md old governance dependency migrated to
  FLOWMIND_CORE_RULES.md and validated
- final cross-file authority validation completed with PASS
- governance publication commit ee94ae1 created and pushed successfully
- required affected Project Sources synchronized 6/6
- compact new-chat recovery verification completed successfully using
  FLOWMIND_CORE_RULES.md + FLOWMIND_ACTIVE_MAP.md without reconstructing
  project history or promoting legacy authority

Governance compaction is closed.

Production runtime is no longer frozen by governance.

Production completion remains:

98%

Do not increase production completion above 98% until the production
target's remaining runtime exit conditions and validated implementation
commit are complete.

4. Active Production Target

Production target:

PRODUCTION EXECUTION ORDER REPAIR

Production target status:

IN PROGRESS / ACTIVE

Do not reopen completed production boundaries merely because governance
is being compacted.

Required canonical lifecycle:

TOPIC -> SCRIPT -> SCENES -> ASSETS -> ASSEMBLY -> QA ->
READY_FOR_UPLOAD -> UPLOADED -> ARCHIVED

HALT remains the controlled stop state.

AUDIO is not a canonical lifecycle phase.

Required production dependency order:

SCRIPT -> Visual Intent / Pass 1 -> Canonical Audio -> actual audio
timing -> Pass 2 / timed execution -> Media Requirements -> Media
Resolution -> Assembly / deterministic final render -> QA of the
completed final artifact

The dispatcher remains the only canonical phase-transition authority.

5. Verified Production Boundaries

The following implementation boundaries are already verified and must
not be reopened without material new evidence.

Audio executor

engine/executors/audio_executor.py

Verified:

-   audio planning is an internal SCENES substep
-   no canonical AUDIO phase
-   dynamic segment count
-   downstream audio_plan preserved
-   no canonical phase advance

Evidence:

AUDIO_EXECUTOR_SCENES_MIGRATION=PASS

Audio renderer

Verified:

-   internal SCENES substep
-   no FLOWMIND_AUDIO_RENDER_LIMIT production dependency
-   dynamic audio_plan rendering
-   valid rendered files can be reused idempotently
-   actual duration obtained through ffprobe
-   phase remains SCENES
-   actual duration is written
-   duration_validated=True
-   audio_path preserved
-   loudness validation remains a required downstream audio-readiness
    step

Runtime evidence included 9 segments and 390.505 seconds for the control
artifact.

These counts are evidence, not production constants.

Scenes executor / Visual Intent Pass 1

engine/executors/scenes_executor.py

Verified repaired boundary:

-   runtime PASS
-   OpenAI call per scene
-   topic-agnostic visual units
-   no hard-coded current topic
-   no canonical phase transition
-   dynamic visual-unit output

Evidence:

SCENES_PASS1_RUNTIME=PASS

Historical runtime evidence included 9 scenes and 31 visual units.

These counts are evidence, not production constants.

Visual pacing / Pass 2

engine/executors/visual_pacing_executor.py

Verified repaired boundary:

-   maps ordered proportional visual units onto actual audio-timed beats
-   preserves actual timing
-   preserves order
-   supports dynamic counts
-   no canonical phase transition
-   exact timing ownership remains downstream of actual canonical audio

Assets

engine/executors/assets_executor.py

Verified repaired/runtime boundary:

-   timed beats produce asset requirements dynamically
-   resolved media is produced through the existing active resolver path
-   asset IDs are dynamic
-   no hard-coded runtime asset count

Historical runtime evidence included 84 timed beats, 84 assets, and 84
resolved media items.

These counts are evidence, not production constants.

Do not invent a second resolver/orchestrator unless new runtime evidence
proves an actual gap.

Canonical dispatcher

engine/canonical_dispatcher.py

Verified repaired lifecycle boundary:

-   AUDIO removed as a canonical phase
-   relevant lifecycle includes SCRIPT, SCENES, ASSETS, ASSEMBLY, QA
-   SCENES -> ASSETS guard requires scenes_path, audio_render_path, and
    visual_pacing_plan_path
-   QA -> READY requires qa_passed=True
-   READY -> UPLOADED requires approved_for_upload=True
-   dispatcher remains API-only

Do not treat canonical_dispatcher.py as a CLI.

Assembly executor

engine/executors/assembly_executor.py

Verified static and runtime boundary:

-   consumes timed media
-   groups beat assets into scene timeline
-   each scene has audio once
-   visual segments follow timed beat media
-   before final render, render_ready=False is intentional

Evidence:

ASSEMBLY_TIMED_MEDIA_RUNTIME=PASS

Historical runtime evidence included 9 scenes, 84 beats, 84 visual
segments, and expected duration 390.505 seconds.

These counts are evidence, not production constants.

Assembly readiness

tools/apply_assembly_readiness.py

Verified KEEP.

It dynamically validates:

-   project/assets relationships
-   resolution/license readiness
-   audio readiness
-   loudness validation
-   duration validation
-   blockers
-   timeline/scene relationships

Before final render it intentionally leaves:

render_ready=False

with final render still required.

Final render

engine/executors/final_render_executor.py

Historical render mechanics are runtime-proven under the old ownership
boundary.

Corrected current boundary:

ASSEMBLY side only, before QA.

Current corrected implementation has static PASS for the repaired
ASSEMBLY guard.

Do NOT claim corrected integrated runtime PASS yet.

Historical mechanics evidence:

FINAL_RENDER_TIMED_VISUALS_RUNTIME=PASS

Corrected boundary evidence:

FINAL_RENDER_ASSEMBLY_BOUNDARY_STATIC=PASS

Final render readiness

tools/apply_final_render_readiness.py

Verified corrected static boundary:

-   validates final video and final render report
-   requires final render verdict PASS
-   validates non-zero artifact/duration
-   validates failed_scene_count=0
-   validates blockers empty
-   synchronizes assembly readiness
-   sets render_ready=True after successful final render
-   does not change canonical phase

Evidence:

FINAL_RENDER_READINESS_ASSEMBLY_STATIC=PASS

Corrected integrated runtime proof is still NOT DONE.

Active phase runner

tools/flowmind_run_phase.py

Verified repaired static contour:

SCRIPT: script_executor

SCENES: scenes_executor audio_executor audio_renderer
audio_loudness_report apply_audio_loudness_report visual_pacing_executor

ASSETS: assets_executor

ASSEMBLY: assembly_executor apply_assembly_readiness
final_render_executor apply_final_render_readiness

QA: qa_executor

Verified:

-   no canonical AUDIO phase
-   state phase AUDIO fails closed
-   runner does not transition canonical phase
-   each substep must leave canonical phase unchanged

Evidence:

FLOWMIND_RUN_PHASE_REPAIRED_CONTOUR_STATIC=PASS

Full repaired runner runtime PASS remains NOT DONE until clean control
replay.

6. Known Deferred Defect

QA verdict defect is VERIFIED but DEFERRED from the production-order
target.

Current known behavior in qa_executor:

-   QA consumes an existing final artifact
-   final verdict logic is still defective
-   upload-readiness logic is circular
-   final verdict is hardcoded BLOCKED / qa_passed=False /
    approved=False

Do not fix this inside PRODUCTION EXECUTION ORDER REPAIR.

The production-order target may close if the clean replay reaches QA
through the corrected lifecycle and the only remaining failure is this
already-known QA verdict defect.

Then the QA defect becomes the next separate target.

7. Clean Replay State

A clean control replay is still required to close the production-order
target.

Its purpose is not to re-prove every module independently.

It must provide integrated runtime evidence of:

SCENES -> Pass 1 -> canonical audio -> actual audio timing -> timed Pass
2 -> ASSETS -> resolved media -> ASSEMBLY -> final render -> final
readiness -> dispatcher transition to QA -> QA receives the
already-created final video

Known historical candidates and experiments must not be mutated to
manufacture PASS.

Previously rejected/blocked replay evidence remains historical evidence.

Do not:

-   manually change script_qa FAIL to PASS
-   patch historical fixtures to make them green
-   resume donor/bootstrap archaeology by inertia
-   restart completed module audits without new material evidence

New replay directories observed in the working tree before governance
compaction:

-   projects/FM_CONTROL_REPLAY_20261006/
-   projects/FM_CONTROL_REPLAY_20261006_01/
-   projects/FM_CONTROL_REPLAY_20261006_R1/
-   projects/FM_CONTROL_REPLAY_20261006_R2/

Their final success/failure status is UNVERIFIED in this Active Map.

They must not be deleted or classified without direct inspection when
production work resumes.

8. Production Exit Conditions

PRODUCTION EXECUTION ORDER REPAIR completes when:

1.  AUDIO is no longer a canonical runtime phase.
2.  Canonical audio is internal before exact timing.
3.  Exact timed execution exists before media resolution.
4.  Media resolution produces required resolved/licensed media.
5.  Final render is on the ASSEMBLY/production side of the QA boundary.
6.  QA receives an already-created final video.
7.  Active runner matches the repaired contour.
8.  Dispatcher matches the canonical lifecycle.
9.  Targeted old-order tests/checks are updated or retired where
    required.
10. One clean control replay provides runtime evidence through the QA
    boundary.
11. No second active contour or canonical state exists.
12. The validated implementation block is committed.

Current interpretation:

-   implementation repairs are substantially complete
-   corrected final-render/readiness integrated runtime proof is still
    pending
-   full repaired runner runtime proof is still pending
-   clean control replay through QA boundary is still pending
-   validated production implementation commit is still pending

Do not raise production completion above 98% before these closure
conditions are satisfied.

9. Governance Closure

AUTHORITY SIMPLIFICATION / GOVERNANCE COMPACTION is COMPLETE.

Verified closure conditions:

1. FLOWMIND_CORE_RULES.md is the single active owner of permanent
   operating/execution discipline.
2. FLOWMIND_ACTIVE_MAP.md is the single current operational/recovery
   checkpoint.
3. 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md no longer owns duplicate
   rules.
4. docs/FLOWMIND_WORK_PROTOCOL_V1.md no longer owns duplicate rules.
5. FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md routes authority to the simplified
   model.
6. No other active authority document materially restores the retired
   duplicate ownership.
7. Cross-file authority validation passed.
8. Governance publication commit ee94ae1 was committed and pushed.
9. Required affected Project Sources were synchronized 6/6.
10. New-chat recovery verification passed using CORE + ACTIVE MAP without
    reconstructing project history.

No V3.3 is authorized.

No production architecture rewrite is authorized.

10. Current Allowed Work

Governance compaction is closed.

Production runtime work for the active target is UNFROZEN.

Allowed work is limited to the current production target and the smallest
evidence required to satisfy its remaining exit conditions.

Do not:

- reopen completed production boundaries without material new evidence
- rerun governance compaction
- reconstruct project history
- resume donor/bootstrap archaeology by inertia
- mutate historical failed replay evidence to manufacture PASS
- fix the known deferred QA verdict defect inside PRODUCTION EXECUTION
  ORDER REPAIR
- introduce a second dispatcher, canonical state, resolver, or production
  contour
- mix unrelated architecture/provider migration work into the current target

11. Current Next Logical Action

Current next logical action:

Perform ONE CLEAN CONTROL REPLAY through the QA boundary using the repaired
production contour.

Purpose:

Provide the remaining integrated runtime evidence for PRODUCTION EXECUTION
ORDER REPAIR without re-proving already verified modules independently.

The replay must demonstrate, in order:

SCENES -> Visual Intent / Pass 1 -> canonical audio -> actual audio timing
-> loudness readiness -> timed Pass 2 -> ASSETS -> resolved/licensed media
-> ASSEMBLY -> deterministic final render -> final render readiness ->
dispatcher transition to QA -> QA receives the already-created final video

Execution constraints:

- start from a valid clean control input/state
- use the repaired active runner and canonical dispatcher
- do not manually change script_qa FAIL to PASS
- do not patch historical fixtures to make them green
- do not resume donor/bootstrap archaeology by inertia
- do not restart completed module audits without material new evidence
- preserve historical failed/blocked replay evidence
- inspect existing replay directories only when needed to avoid misclassifying
  or overwriting evidence
- final render may take time; do not kill a healthy render merely because it
  is long-running
- if the replay reaches QA with an already-created final video and the only
  remaining failure is the known deferred QA verdict defect, treat that
  defect according to Section 6 rather than repairing it inside this target

Closure after replay still requires the validated production implementation
block to be committed.

End.
