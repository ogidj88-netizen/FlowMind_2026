FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP Project: FlowMind / Imagine What If
Updated: 2026-10-10 Mode: SYSTEM AUDIT — RUNTIME EVIDENCE (READ-ONLY)

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

4A. Current Audit Checkpoint (2026-10-09)

The approved SYSTEM AUDIT methodology is now the current workstream.
Recovery verification is completed; the immediate phase is RUNTIME EVIDENCE, not code remediation.
R2 editorial issues are historical evidence only. R3 success or failure
is UNKNOWN without direct current runtime evidence. No technical or
editorial production-readiness PASS is claimed.

The historical production-order repair material below is retained for
traceability and may still contain open exit conditions. Its former
NEXT ACTION is superseded by Section 11.

4. Historical Production Target (superseded operational focus)

Production target:

PRODUCTION EXECUTION ORDER REPAIR

Historical production target status at 2026-10-07 checkpoint:

IN PROGRESS / NOT CLOSED; deferred pending system audit baseline

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

7. Historical Clean Replay State (unverified; not current next action)

At the 2026-10-07 checkpoint a clean control replay remained required
to close the production-order target. This is historical NOT DONE, not
the current next action.

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

8. Historical Production Exit Conditions (not superseded as proof)

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

Current active target: SYSTEM AUDIT — RUNTIME EVIDENCE (READ-ONLY).

Recovery checkpoint (verified 2026-10-09): branch wip-transfer-20261006,
GitHub HEAD fab8ce1e550314dfa95c02f10d1c526daf42f19b;
GitHub-first new-chat recovery PASS. Historical recovery NOT DONE claims
below are superseded, not fresh work items. No production changes authorized.

Verified repository publication checkpoint (branch wip-transfer-20261006):

- Audit methodology and Registry publication: f890056.
- GitHub-first recovery rule in FLOWMIND_CORE_RULES.md: c096486.
- Reconciled Active Map publication: e7aa508.
- Audit Framework header corrected to PUBLISHED IN REPOSITORY: a612e4d.
- Registry Section 5.1 corrected to PUBLISHED IN REPOSITORY: 80acbbf.
- Framework is an approved reference methodology, NOT a seventh canonical authority.
- Older publication-pending statements are historical and superseded.
- The current GitHub branch HEAD must be fetched directly at recovery time;
  historical commit IDs in this Map are evidence anchors, not a HEAD pointer.

Project Sources cleanup confirmed by the user:

- Stale FLOWMIND_ACTIVE_MAP.md Project Source copy removed.
- Stale FLOWMIND_AUDIT_FRAMEWORK_V1.md Project Source copy removed.
- Stale FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md Project Source copy removed.
- GitHub remains the durable master; do not reintroduce stale copies.

Audit method approved:

- system-wide runtime and contract audit, not fixture-specific R2 fixes
- independent Hard Gates; MQS-100, FDS-100 and VQS-100 only with evidence
- UNKNOWN remains UNKNOWN; no fabricated PASS, FAIL or scores
- Future Impact Gate for Long/Shorts, variable scenes, Director and scale
- sequence: Runtime Evidence -> Impact Triage -> Contract & Module Audit ->
  Targeted Quality Hardening -> Downstream Regression ->
  Integrated Validation -> Production Readiness
- no speculative tooling, second dispatcher or extra current-state owner

Material NOT DONE (current):

- reconcile R2 final-render PASS with canonical state still in ASSEMBLY;
  verify final-render readiness and dispatcher/QA handoff using evidence
- establish current runtime baseline and actual module inventory without
  re-running completed work or modifying historical replay artifacts
- inspect R3 identity only if material: its PROJECT_STATE.json identifies R2
  and references R2 artifacts; R3 is NOT independently validated
- verify whether Claude/Gemini/Grok audit findings exist and were accepted
  into the Audit Registry; no external-AI audit PASS is established
- integrated runner replay through QA, QA verdict repair, downstream
  regression and validated implementation commit remain NOT DONE

Governance/recovery exit conditions:

1. Framework is published as reference methodology only.
2. Active Map owns one current target and one next logical action.
3. No duplicate active authority or recovery owner is introduced.
4. Publication changes are in GitHub without unrelated runtime artifacts.
5. Material stale publication claims are reconciled or marked historical.
6. A fresh new chat fetches GitHub HEAD and this Map without inferring
   local runtime PASS or a clean working tree.

Repository publication is verified for the listed governance changes.
Fresh new-chat recovery passed at the verified 2026-10-09 checkpoint.
Production code changes remain paused during read-only runtime evidence audit.

11. Current Next Logical Action

Read-only inspect R2 final-render readiness evidence and canonical phase
transition prerequisites. R2 final_render_report.json (2026-10-09) records
FINAL_RENDER_OK / PASS, 13/13 scenes, 53 visual segments, 236.726 seconds,
-0.071 seconds duration delta, zero failed scenes, blockers and warnings,
with final_video.mp4 present (55,298,076 bytes).

R2 PROJECT_STATE.json (updated 2026-10-09T14:01:18Z) references the
final render report and video but remains phase ASSEMBLY, qa_passed=false,
approval_status=PENDING and approved_for_upload=false. Therefore render
PASS is NOT integrated QA PASS or production readiness.

R3 PROJECT_STATE.json identifies R2 and points to R2 artifacts; do not
assume independent R3 replay success or manually patch historical state.

Do not rerender, execute production, mutate replay folders or change
canonical phases merely to manufacture PASS. Use existing evidence first.

Operational convenience: for large JSON/text files use Finder reveal
(open -R path) and upload the file instead of pasting full terminal output.
This is not a new governance authority.

End.
