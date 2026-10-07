FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP Project: FlowMind / Imagine What If
Updated: 2026-10-07 Mode: AUTHORITY SIMPLIFICATION / GOVERNANCE
COMPACTION

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

3. Current Governance Transaction

Current transaction:

AUTHORITY SIMPLIFICATION / GOVERNANCE COMPACTION

Purpose:

-   make FLOWMIND_CORE_RULES.md the single owner of permanent operating
    and execution discipline
-   make FLOWMIND_ACTIVE_MAP.md the single current-state/recovery
    checkpoint
-   remove duplicated active governance ownership
-   make new-chat recovery small and deterministic
-   preserve specialized reference authorities without rereading them by
    default

Runtime implementation is FROZEN during this transaction.

Production completion remains:

98%

Do not increase production completion above 98% until the production
target’s remaining runtime exit conditions and validated commit are
complete.

Verified governance work in this transaction:

-   FLOWMIND_CORE_RULES.md created and validated
-   logical-action execution rule added to FLOWMIND_CORE_RULES.md
-   large replacement content is delivered as .txt by default
-   000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md compacted to a
    transitional compatibility pointer and validated
-   docs/FLOWMIND_WORK_PROTOCOL_V1.md compacted to a transitional
    reference / compatibility document and validated
-   FLOWMIND_ACTIVE_MAP.md compacted into the single operational/recovery
    checkpoint and validated
-   FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md reconciled to the simplified
    authority model and validated
-   targeted active-authority dependency/reference scan completed
-   CANONICAL_DISPATCHER_SPEC.md old governance dependency migrated to
    FLOWMIND_CORE_RULES.md and validated
-   final cross-file authority validation completed with PASS
-   Git status inspected; production/runtime modifications and runtime
    evidence remain intentionally outside the governance commit

Governance transaction status:

IN PROGRESS / READY FOR DURABLE PUBLICATION

4. Frozen Production Target

Production target:

PRODUCTION EXECUTION ORDER REPAIR

Production target status:

IN PROGRESS / FROZEN FOR GOVERNANCE COMPACTION

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

9. Governance Exit Conditions

AUTHORITY SIMPLIFICATION / GOVERNANCE COMPACTION completes when:

1.  FLOWMIND_CORE_RULES.md is the single active owner of permanent
    operating/execution discipline.
2.  FLOWMIND_ACTIVE_MAP.md is the single current operational/recovery
    checkpoint.
3.  000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md no longer owns duplicate
    rules.
4.  docs/FLOWMIND_WORK_PROTOCOL_V1.md no longer owns duplicate rules.
5.  FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md routes authority to the
    simplified model.
6.  No other active authority document materially restores the retired
    duplicate ownership.
7.  Cross-file authority validation passes.
8.  The governance block is committed and pushed.
9.  Required Project Sources are synchronized.
10. A recovery check confirms that a new chat can continue from CORE +
    ACTIVE MAP without reconstructing project history.

No V3.3 is authorized.

No production architecture rewrite is authorized.

10. Current Allowed Work

Until governance compaction closes, allowed work is limited to:

-   governance authority simplification
-   current-state compaction
-   authority routing correction
-   targeted cross-file authority validation
-   Git commit/push of the validated governance block
-   required Project Sources synchronization
-   recovery verification

Production runtime execution remains frozen.

Do not mix production fixes into this governance block.

11. Current Next Logical Action

Current next logical action:

Publish the validated governance simplification block durably without
mixing production/runtime WIP.

Required sequence:

1.  stage only the intended governance files:
    - FLOWMIND_CORE_RULES.md
    - 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
    - docs/FLOWMIND_WORK_PROTOCOL_V1.md
    - FLOWMIND_ACTIVE_MAP.md
    - FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
    - CANONICAL_DISPATCHER_SPEC.md
2.  verify the staged file set exactly
3.  run staged diff validation
4.  commit the governance block
5.  push the current branch
6.  verify the pushed commit and remaining unstaged production/runtime WIP
7.  replace/synchronize every affected Project Source with the committed
    versions
8.  verify Project Source contents
9.  perform a compact new-chat recovery verification using CORE + ACTIVE MAP

Do not stage:

-   engine runtime modifications
-   tool runtime modifications
-   control replay directories
-   historical runtime evidence directories
-   unrelated files

Production runtime remains FROZEN until governance publication and
recovery verification complete.

Governance publication is NOT complete until the affected Project Sources
are synchronized and verified.

End.
