# FLOWMIND AUDIT FINDINGS V1

Status: ACTIVE AUDIT RECORD
Project: FlowMind / Imagine What If
Mode: SYSTEM AUDIT MODE
Authority: NONE

Purpose:

Persistent evidence-based record of material findings discovered during the FlowMind system audit.

This file is not:

- operational authority
- target architecture
- runtime proof by itself
- implementation authorization

SYSTEM AUDIT MODE rule:

- confirmed findings are recorded immediately
- YELLOW and ORANGE findings do not authorize implementation
- RED may pause audit when continuing would be unsafe or invalid
- implementation priority is selected only after audit exit conditions are satisfied

---

## 1. Classification model

KEEP

= useful as-is; no material modernization requirement found.

ADAPT

= useful responsibility remains, but implementation requires modification.

REPLACE

= responsibility remains, but current implementation should be replaced.

REMOVE

= obsolete, duplicated, harmful, or unnecessary.

UNKNOWN

= insufficient implementation evidence for a safe disposition decision.

Severity:

GREEN

= healthy.

YELLOW

= material but lower-impact issue.

ORANGE

= confirmed significant architecture, control, reliability, validation, automation, correctness, or quality issue.

RED

= critical blocker requiring audit pause.

---

# 2. Findings

## AUDIT-001 — Unsafe HALT resume policy

Component:

engine/canonical_dispatcher.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

resume_from_halt() accepts any target contained in RESUMABLE_PHASES rather than deriving one permitted destination from verified prior state.

The resume path does not use the normal sequential ALLOWED_PHASE_TRANSITIONS model.

No inspected lower-level validation in:

- engine/state_validator.py
- engine/state_store.py

prevents a structurally valid resume such as:

HALT -> READY_FOR_UPLOAD

Risk:

Normal sequential production and release gates can be bypassed during HALT resume.

Required outcome:

- explicit canonical resume policy
- verified resume destination
- rejection of arbitrary targets
- QA/release gate preservation
- fail-closed invalid targets
- regression coverage

Resolution:

OPEN

---

## AUDIT-002 — Dispatcher validation misses unsafe HALT resume

Component:

tools/run_dispatcher_checks.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

run_resume_test() treats:

HALT -> AUDIO

as expected success.

It does not verify:

- prior phase
- permitted resume destination
- arbitrary-target rejection
- HALT -> READY_FOR_UPLOAD rejection
- release-gate preservation

Therefore DISPATCHER_CHECKS_ALL_OK can occur while AUDIT-001 remains present.

Required outcome:

Add negative HALT-resume regression coverage after AUDIT-001 is corrected.

Resolution:

OPEN

---

## AUDIT-003 — Dispatcher validation Python mismatch

Component:

tools/check_dispatcher.sh

Classification:

ADAPT

Severity:

YELLOW

Status:

CONFIRMED — OPEN

Evidence:

tools/dispatcher.sh resolves Python through:

- .venv/bin/python
- python3 fallback
- explicit failure

tools/check_dispatcher.sh invokes:

python

directly.

Risk:

Validation and runtime can execute under different Python environments.

Required outcome:

Runtime and validation must use the same interpreter-resolution policy.

Resolution:

OPEN

---

## AUDIT-004 — Hard-coded niche intelligence inside script, scene and asset planning

Components:

- engine/executors/script_executor.py
- engine/executors/scenes_executor.py
- engine/executors/assets_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The current SCRIPT, SCENES and ASSETS contour contains historical electricity / invisible-cost niche intelligence and fixed creative assumptions.

script_executor.py:

build_script() contains a predominantly hard-coded electricity-bill narration.

The function accepts:

- topic
- working_title
- hook
- niche
- audience
- content_language
- target_duration_sec

but most of the actual story, explanation, examples, structure and payoff are fixed in source code.

The supplied niche parameter does not drive generation of the narrative.

Manifest values such as:

- topic
- title
- hook
- audience

are interpolated into an otherwise pre-authored niche-specific script.

scenes_executor.py and assets_executor.py similarly contain historical niche-specific creative assumptions.

Current deterministic executors therefore combine execution with creative decisions including:

- script content
- story structure
- scene segmentation
- asset-type selection
- visual intent
- on-screen text
- production notes
- niche-specific asset queries

Risk:

Changing niche, topic class or creative direction requires runtime-code changes rather than Brain / Editorial / Director decisions.

This prevents the current contour from functioning as a general media-production system.

Positive evidence:

script_executor.py correctly uses:

- load_state()
- save_state_with_disk_guard()
- SCRIPT phase guard
- atomic artifact writes
- explicit error handling

These control/persistence patterns should be preserved.

Required outcome:

Brain / Editorial intelligence
-> canonical narration
-> evidence-backed Script QA
-> Director / scene / shot intent
-> asset requirements
-> capability contracts
-> provider execution
-> normalized artifacts
-> deterministic validation

Creative content must not be embedded as fixed niche prose inside deterministic runtime executors.

Resolution:

OPEN

---

## AUDIT-005 — Scene-level asset, assembly and render contract blocks shot-aware production

Components:

- engine/executors/assets_executor.py
- engine/executors/assembly_executor.py
- engine/executors/final_render_executor.py

Supporting runtime evidence:

- projects/P2026_TEST_001/assets/assets.json
- projects/P2026_TEST_001/assets/resolved_assets.json
- projects/P2026_TEST_001/final_render/final_render_report.json

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Current effective contract is:

scene
-> one asset
-> one assembly item
-> one rendered scene segment

The inspected project confirms:

9 scenes
-> 9 planned assets
-> 9 resolved assets
-> 9 rendered scene segments

Assembly rejects more than one asset for the same scene_id.

Final rendering uses one visual asset for each scene.

Risk:

Canonical production cannot naturally represent:

- multiple shots per scene
- multiple visual assets per scene
- semantic visual changes inside long narration
- shot-specific timing
- shot-specific provider outputs

Required outcome:

scene
-> 1..N shots
-> 1..N asset requirements
-> resolved assets
-> timing / motion
-> normalized production timeline
-> renderer

Resolution:

OPEN

---

## AUDIT-006 — Visual Pacing is post-render and disconnected from canonical rendering

Components:

- engine/executors/visual_pacing_executor.py
- engine/executors/final_render_executor.py

Positive donor:

tools/render_visual_pacing_preview.py

Supporting runtime evidence:

projects/P2026_TEST_001/visual_pacing/visual_pacing_plan.json

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

visual_pacing_executor.py requires an already successful final render and existing final video.

final_render_executor.py does not consume visual_pacing_plan.

Therefore visual pacing cannot influence the canonical render that is required as its own prerequisite.

Runtime artifact confirms:

- audio_master_clock = true
- beat_count = 84
- scene_count = 9
- target beat duration = 5.0 sec
- min beat duration = 3.0 sec
- max beat duration = 6.5 sec
- total duration = 390.505 sec
- duration delta = 0
- status = VISUAL_PACING_PLAN_OK

The artifact contains useful beat-level fields including:

- beat timing
- display_text
- motion_profile
- visual_action
- render_instruction

However beats inside a scene repeatedly reuse the same scene asset.

Variation is primarily created through:

- zoom
- pan
- crop
- static/chart focus
- text/no-text alternation

The plan records:

source_phase = QA

and consumes:

source_final_render_report_path

confirming that pacing is currently produced after canonical final rendering.

Positive evidence:

tools/render_visual_pacing_preview.py already provides usable beat-level FFmpeg rendering behavior.

Risk:

Useful beat-level capability exists, but too late in the production contour and without sufficient Director-driven shot/asset variation.

Required outcome:

Brain / Director
-> shot/pacing decisions
-> resolved assets
-> normalized shot/beat plan
-> canonical renderer
-> QA

Reuse preview-rendering donor behavior where appropriate.

Do not create a second production contour.

Runtime-confirmed preservation requirements:

- preserve audio-master-clock beat timing
- preserve existing beat-level render instructions as donor capability
- preserve useful display_text / motion_profile / visual_action structure
- move pacing decisions before canonical rendering
- allow Director-driven asset and shot changes inside a scene
- do not treat repeated zoom/pan/crop on one asset as sufficient visual variety
- motion must follow semantic intent and asset type rather than a fixed mechanical sequence
- preserve deterministic beat timing and duration validation

Resolution:

OPEN

---

## AUDIT-007 — QA executor contains a circular release gate and cannot produce QA PASS

Component:

engine/executors/qa_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

QA upload readiness depends on:

qa_passed = true
and approved_for_upload = true

while QA itself should establish qa_passed.

Implementation explicitly persists:

qa_passed = false

and hard-codes BLOCKED behavior.

Runtime confirmation:

projects/P2026_TEST_001/qa/qa_report.json

contains eleven production checks with PASS status.

Its only BLOCKED check is:

upload_readiness

The report then produces:

qa_passed = false
verdict = BLOCKED
approved_for_upload = false

Risk:

Normal QA -> READY_FOR_UPLOAD flow cannot be completed by the QA executor.

Required outcome:

QA:
-> PASS / FAIL
-> persist qa_passed

Release approval must remain separate.

Resolution:

OPEN

---

## AUDIT-008 — Asset Resolver is local-only and can resolve weak semantic matches

Component:

engine/executors/asset_resolver.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Current resolver mode:

local_existing_only

Candidate scoring can become positive from a compatible file extension even without meaningful semantic correspondence.

choose_candidate() accepts:

score > 0

Risk:

- no autonomous provider resolution in this resolver
- semantically irrelevant local media may be marked ready

Required outcome:

Provider-neutral asset resolution plus meaningful request correspondence validation.

Local fallback and licensing behavior should remain.

Resolution:

OPEN

---

## AUDIT-009 — Audio narration can bypass the QA-approved script text

Component:

engine/executors/audio_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

audio_executor.py requires script_qa.verdict = PASS.

However TTS planning uses:

assembly_plan.timeline[].voiceover_text

The QA-approved script text is not compared for textual identity.

Only total word count is cross-checked.

Equal word count does not prove equal narration.

Risk:

Narration reaching TTS may differ from narration that received Script QA PASS.

Required outcome:

TTS narration must be demonstrably derived from QA-approved canonical narration.

Possible mechanisms:

- deterministic segmentation
- normalized-text equality
- source hash
- per-segment hashes

Resolution:

OPEN

---

## AUDIT-010 — Audio Renderer reuses existing TTS files without validating render identity

Component:

engine/executors/audio_renderer.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

If the expected MP3 already exists and has non-zero size, the renderer reuses it.

Reuse does not validate:

- narration content
- source identity
- voice
- model
- synthesis settings
- audio-plan identity

Runtime evidence confirms:

AUDIO_SEGMENT_001
reused_existing_file = true

Risk:

Stale audio can silently survive narration or provider configuration changes.

Required outcome:

Reuse only after deterministic render fingerprint equality.

File existence alone must never authorize reuse.

Resolution:

OPEN

---

## AUDIT-011 — Audio Renderer marks duration validated without validating actual duration

Component:

engine/executors/audio_renderer.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Segment duration_validated is set true after successful duration probing.

Project-level:

duration_validated = all_segments_rendered

No actual comparison between total_duration_sec and target_duration_sec occurs.

Runtime evidence:

target_duration_sec = 480

total_duration_sec = 390.505

duration_validated = true

Risk:

Materially short or long narration can become production-ready.

Required outcome:

Actual measured duration must be compared against explicit production tolerance.

Resolution:

OPEN

---

## AUDIT-012 — Loudness threshold violations do not fail loudness validation

Component:

tools/audio_loudness_report.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The tool performs real FFmpeg loudnorm measurement.

Configured limits include:

- target integrated loudness = -16 LUFS
- max integrated deviation = 1 LU
- max true peak = -0.5 dBTP
- max LRA = 8 LU

Threshold violations are classified as:

WARN

Final report logic is:

verdict = PASS if fail_count == 0 else FAIL

loudness_validated = fail_count == 0

warn_count is ignored.

Therefore:

PASS = 7
WARN = 2
FAIL = 0

still produces:

verdict = PASS
loudness_validated = true

Current runtime artifact has:

9 PASS
0 WARN
0 FAIL

so the inspected artifact itself is within thresholds.

Risk:

Future threshold violations can pass the production loudness gate.

Required outcome:

Production acceptance thresholds must actually block loudness validation when exceeded.

Resolution:

OPEN

---

## AUDIT-013 — Loudness report is not bound to the exact audio render it validates

Component:

tools/apply_audio_loudness_report.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The loudness applicator intends to verify:

- audio_render.project_id == report.project_id
- report.verdict = PASS
- report.loudness_validated = true
- report.fail_count = 0
- report.segment_count == audio_render.segment_count
- report.source_audio_render_path corresponds to the supplied audio render
- report file exists

AUDIT-018 separately proves that the current source fails while attempting the source-path comparison because audio_render_path is not in validate_loudness_report() scope.

Even after that runtime defect is corrected, path equality alone does not prove that the report was generated from the current bytes or current contents of the audio artifacts.

There is no validation of:

- audio-render fingerprint
- per-segment audio fingerprint
- per-segment file identity
- modification/content identity

The report contains source_audio_renderer_version, but the applicator does not compare it against current audio_render.renderer_version.

Risk:

Once the immediate AUDIT-018 defect is fixed, changed or regenerated audio could still inherit loudness approval measured against older audio.

Required outcome:

Loudness evidence must be bound to the exact audio artifact set it measured.

Persist and validate deterministic audio/render fingerprints.

Path equality alone must not establish provenance.

Resolution:

OPEN

---

## AUDIT-014 — Loudness applicator bypasses canonical state validation and lacks state-project binding

Component:

tools/apply_audio_loudness_report.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

PROJECT_STATE is read using the tool's generic JSON reader.

The tool does not use:

- engine.state_validator.load_state
- engine.state_store.save_state_with_disk_guard

After mutation it directly writes PROJECT_STATE with:

write_json_atomic(state_path, state)

Project identity is validated only between:

audio_render.project_id
and
audio_loudness_report.project_id

It does not verify:

PROJECT_STATE.project_id == audio_render.project_id

Therefore a caller can theoretically provide:

Project A PROJECT_STATE

with:

Project B audio_render
Project B loudness report

and register Project B artifacts into Project A state.

Risk:

- cross-project artifact contamination
- canonical state mutation outside validated persistence
- another canonical-state writer outside the intended state layer

No evidence proves this occurred in the inspected project.

Required outcome:

PROJECT_STATE.project_id
=
audio_render.project_id
=
audio_loudness_report.project_id

State must be loaded and persisted through the approved validated state layer.

Resolution:

OPEN

---

## AUDIT-015 — Runtime phase model and production orchestration diverge from canonical control semantics

Components:

- engine/canonical_dispatcher.py
- current production executor contour

Supporting runtime evidence:

projects/P2026_TEST_001/PROJECT_STATE.json

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The persisted runtime phase history for P2026_TEST_001 is:

TOPIC
-> SCRIPT
-> SCENES
-> ASSETS
-> ASSEMBLY
-> AUDIO
-> QA

The project entered QA at:

2026-05-18T21:00:08Z

The current persisted phase remains:

QA

However the same state already registers production artifacts including:

- audio_render_path
- audio_loudness_report_path
- final_render_report_path
- final_video_path
- visual_pacing_plan_path
- qa_report_path

There are no later phase transitions recorded after entry into QA.

Previously audited implementation also confirms that several production operations are intentionally executed while the project phase is QA.

The real runtime phase history also contains:

AUDIO

while the previously verified canonical control specification does not define AUDIO as one of its canonical production phases.

Therefore two control concepts are currently mixed:

1. phase as a canonical project lifecycle state;
2. QA as a broad execution container for additional production work.

Risk:

PROJECT_STATE.phase no longer reliably communicates where the project actually is in the production lifecycle.

This weakens:

- orchestration clarity
- recovery semantics
- HALT/resume correctness
- transition guards
- operator observability
- deterministic automation
- future scheduling

This finding is distinct from AUDIT-007.

AUDIT-007 concerns the circular QA/release decision.

AUDIT-015 concerns phase semantics and execution ordering.

Required outcome:

Define one coherent lifecycle contract.

For every real production operation, establish whether it is:

- a canonical lifecycle phase;
- or an internal sub-step of a canonical phase.

If AUDIO is intended to remain a canonical phase, all canonical control layers must define it consistently.

If AUDIO is internal, it must not create contradictory lifecycle state.

QA must represent an actual quality-evaluation stage.

Resolution:

OPEN

---

## AUDIT-016 — QA validates pipeline readiness, not final output quality

Component:

engine/executors/qa_executor.py

Supporting runtime evidence:

projects/P2026_TEST_001/qa/qa_report.json

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The inspected QA report contains twelve checks.

Eleven are marked PASS:

- Script QA passed
- Scenes artifact valid
- Resolved assets artifact valid
- Assets resolved
- Asset licenses cleared
- Assembly plan valid
- Assembly render ready
- Audio plan valid
- Audio render artifact valid
- Audio ready
- Final video exists

The only BLOCKED check is:

upload_readiness

For the actual final video, the QA report checks only:

final_video_exists

with detail:

final video file exists

The report does not provide evidence of QA checks for:

- actual final-video duration against target duration
- audio/video synchronization
- actual audio duration independent of upstream flags
- frozen or black frames
- visual pacing quality
- shot variety
- narration/visual correspondence
- readable overlays/cards
- final content quality
- semantic correctness of final visuals
- retention risk
- final-render report verdict

The artifact summary also does not include:

final_render_report_path

or:

visual_pacing_plan_path

as QA evidence inputs.

Cross-evidence from AUDIT-011 is material.

The same project has:

target_duration_sec = 480

and:

audio total_duration_sec = 390.505

while upstream audio nevertheless reports:

duration_validated = true
audio_ready = true

The QA report then accepts:

audio_ready = PASS

without independently detecting the duration problem.

Risk:

A pipeline can be structurally complete and still produce weak, mistimed, visually poor, semantically wrong, or otherwise unusable final video while current QA reports all production checks as PASS.

Required outcome:

QA must independently evaluate the actual final output.

Minimum production QA contract should cover relevant deterministic checks such as:

- final render report validity
- actual output duration
- audio/video synchronization
- media readability and technical integrity
- required artifact provenance

Quality-sensitive checks should also evaluate the produced media against Director / content intent where technically and economically justified.

Upstream readiness booleans may be inputs.

They must not substitute for final-output validation.

Release approval must remain separate from QA PASS.

Resolution:

OPEN

---

## AUDIT-017 — Script QA PASS is not evidence-backed enough for downstream trust

Component:

Script QA gate / runtime QA contract

Implementation path:

UNVERIFIED

Supporting runtime evidence:

projects/P2026_TEST_001/script/script_qa.json

Classification:

UNKNOWN

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The inspected Script QA artifact reports:

score = 100

verdict = PASS

warnings = []

failure_reasons = []

All seven scored checks receive maximum points.

However several check details do not expose evidence from the script that demonstrates the claimed quality property.

Examples:

hook_alignment:

15 / 15 points

detail:

working_title=Your Power Bill Is Quietly Changing

The detail exposes the title but does not show how the script hook was compared with it.

topic_match:

15 / 15 points

detail:

topic=Why your electricity bill rises even when usage looks normal

The detail exposes the topic but does not show script evidence establishing topical coverage.

structure:

15 / 15 points

detail:

requires coherent multi-part narration

This describes the requirement rather than evidence that the script satisfies it.

practical_payoff:

15 / 15 points

detail:

audience=Global English

Audience metadata is not evidence of practical payoff.

voiceover_usability:

15 / 15 points

detail:

requires spoken-narration-friendly script text

Again the detail describes a requirement rather than the evaluated evidence.

safety_no_fake_facts:

10 / 10 points

detail:

blocks unsupported precise claims and fake citation patterns

The artifact does not list:

- factual claims detected
- unsupported claims detected
- citation patterns inspected
- evidence used for the PASS

duration_fit is more measurable:

word_count = 1000
allowed_range = 928-1392
estimated_minutes = 6.9

but even this is a coarse script-length check rather than direct runtime duration proof.

Additional implementation evidence:

engine/executors/script_executor.py was inspected.

It creates:

- script.txt
- script_meta.json

It does not create:

script_qa.json

Therefore script_executor.py is not the Script QA producer.

Important evidence boundary:

This finding does NOT yet prove that the actual Script QA producer performs no deeper text analysis internally.

The exact producer implementation has not yet been verified.

The confirmed defect is narrower:

the persisted QA artifact does not provide sufficient content-derived evidence to audit or reproduce why a script received 100/100 and PASS.

Downstream executors already use:

script_qa.verdict = PASS

as a production gate.

Risk:

A downstream component cannot distinguish between:

- a genuinely evaluated high-quality script
- a metadata-driven PASS
- a shallow heuristic PASS
- an opaque internal evaluation whose reasoning was not persisted

This weakens:

- auditability
- reproducibility
- regression diagnosis
- script-quality gating
- future automated optimization
- confidence in downstream production decisions

Required outcome:

Script QA must persist evidence derived from the actual script for each scored quality dimension.

At minimum, where relevant:

- hook evidence and position
- topic coverage evidence
- structural evidence
- practical payoff evidence
- voiceover-readability evidence
- factual-claim extraction
- unsupported-claim / citation-risk evidence
- explicit warnings and failure reasons
- measurable scoring inputs

Qualitative AI judgment may be used when justified, but the artifact should persist structured rubric results and sufficient rationale/evidence to audit the PASS.

A 100/100 result must not be justified only by restating manifest metadata or the rule being checked.

Before assigning a permanent implementation disposition:

identify and inspect the actual current Script QA producer.

Resolution:

OPEN

---

## AUDIT-018 — Loudness applicator contains an uncaught undefined-variable runtime failure

Component:

tools/apply_audio_loudness_report.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

validate_loudness_report() is defined with:

audio_render
loudness_report
loudness_report_path

as its inputs.

Inside that function the implementation executes:

expected_source = str(audio_render_path)

However:

audio_render_path

is not:

- a parameter of validate_loudness_report()
- a local variable in validate_loudness_report()
- a verified module-global value

audio_render_path exists as a local parameter of the separate caller:

apply_loudness_report(
    state_path,
    audio_render_path,
    loudness_report_path,
)

Python lexical scope does not expose caller-local variables inside another top-level function.

apply_loudness_report() calls:

validate_loudness_report(
    audio_render,
    loudness_report,
    loudness_report_path,
)

without passing audio_render_path.

Therefore, after the earlier validation checks succeed and execution reaches:

expected_source = str(audio_render_path)

the current source raises:

NameError

main() catches only:

- ApplyAudioLoudnessReportError
- OSError

NameError is not included.

Therefore the failure escapes the intended controlled failure path as an uncaught exception.

Risk:

The current loudness-application component cannot reliably complete its normal validation/apply path.

The tool may crash after valid inputs reach the source-path validation stage.

This also means historical runtime artifacts that record successful loudness application cannot by themselves prove that this exact current source version produced them successfully.

Do not infer which prior source version or process produced those artifacts without additional evidence.

This finding is distinct from:

AUDIT-013

which concerns insufficient provenance binding even after path validation works.

AUDIT-014

which concerns unsafe canonical-state application and project binding.

Required outcome:

Pass audio_render_path explicitly into validate_loudness_report().

The validator contract must make every required input explicit.

Example intended relationship:

apply_loudness_report(...)
-> validate_loudness_report(
     audio_render,
     loudness_report,
     audio_render_path,
     loudness_report_path
   )

The corrected implementation must:

- eliminate undefined-variable access
- preserve fail-closed validation
- surface invalid input as a controlled domain error
- include regression coverage for the normal successful path
- include regression coverage for source-path mismatch
- avoid an uncaught NameError

Production implementation remains frozen during SYSTEM AUDIT MODE.

Resolution:

OPEN

---

# 3. Audited classifications

engine/canonical_dispatcher.py
= ADAPT

tools/dispatcher_cli.py
= KEEP

tools/dispatcher.sh
= KEEP

engine/state_validator.py
= KEEP

engine/state_store.py
= KEEP

tools/run_dispatcher_checks.py
= ADAPT

tools/check_dispatcher.sh
= ADAPT

Makefile
= KEEP

engine/executors/script_executor.py
= ADAPT

engine/executors/scenes_executor.py
= ADAPT

engine/executors/assets_executor.py
= ADAPT

engine/executors/asset_resolver.py
= ADAPT

engine/executors/assembly_executor.py
= ADAPT

engine/executors/audio_executor.py
= ADAPT

engine/executors/audio_renderer.py
= ADAPT

tools/audio_loudness_report.py
= ADAPT

tools/apply_audio_loudness_report.py
= ADAPT

engine/executors/final_render_executor.py
= ADAPT

engine/executors/visual_pacing_executor.py
= ADAPT

tools/render_visual_pacing_preview.py
= KEEP

engine/executors/qa_executor.py
= ADAPT

Script QA producer implementation
= UNKNOWN

---

# 4. Supporting runtime evidence inspected

## projects/P2026_TEST_001/assets/assets.json

Observed:

- 9 scenes
- 9 planned assets
- one-asset-per-scene planning
- provider_status = planned
- local_path = null
- source_url = null
- license_status = pending

## projects/P2026_TEST_001/assets/resolved_assets.json

Observed:

- 9 scenes
- 9 resolved assets
- one resolved asset per scene
- provider_mode = local_existing_only
- source_provider = manual
- licenses cleared
- no blockers

## projects/P2026_TEST_001/audio/audio_plan.json

Observed:

- 9 planned audio segments
- estimated word count = 1000
- estimated duration = 413 sec
- target duration = 480 sec
- estimate inside configured ±20% planning tolerance
- audio_ready = false

## projects/P2026_TEST_001/audio/audio_render.json

Observed:

- renderer = audio_renderer v1.1.1
- provider = ElevenLabs
- model = eleven_multilingual_v2
- 9/9 segments rendered
- failed_segment_count = 0
- total_duration_sec = 390.505
- target_duration_sec = 480
- duration_validated = true
- loudness_validated = true
- audio_ready = true
- blockers = []
- AUDIO_SEGMENT_001 reused existing MP3

## projects/P2026_TEST_001/audio/audio_loudness_report.json

Observed:

- segment_count = 9
- pass_count = 9
- warn_count = 0
- fail_count = 0
- verdict = PASS
- loudness_validated = true
- target integrated loudness = -16 LUFS
- max integrated deviation = 1 LU
- max LRA = 8 LU
- max true peak = -0.5 dBTP
- all inspected measurements satisfy configured thresholds

## projects/P2026_TEST_001/PROJECT_STATE.json

Observed:

- current phase = QA
- halted = false
- qa_passed = false
- approval_status = PENDING
- approved_for_upload = false
- phase history:
  TOPIC -> SCRIPT -> SCENES -> ASSETS -> ASSEMBLY -> AUDIO -> QA
- no phase transitions are recorded after QA
- current artifacts include audio render, loudness report, final render, final video, QA report and visual pacing plan
- state remains in QA while these production artifacts are registered

## projects/P2026_TEST_001/qa/qa_report.json

Observed:

- executor = qa_executor v1.0.4
- source_phase = QA
- 11 production checks PASS
- only upload_readiness is BLOCKED
- verdict = BLOCKED
- qa_passed = false
- approved_for_upload = false
- readiness_score = 88
- final output validation consists of final_video_exists
- audio_ready is accepted as PASS from upstream state
- no final-render report or visual-pacing artifact appears in artifact_summary

## projects/P2026_TEST_001/final_render/final_render_report.json

Observed:

- renderer = final_render_executor v1.0.0
- scene_count = 9
- rendered_scene_count = 9
- failed_scene_count = 0
- expected_duration_sec = 390.505
- final_duration_sec = 390.207
- duration_delta_sec = -0.298
- final video exists
- verdict = PASS
- status = FINAL_RENDER_OK
- blockers = []
- warnings = []
- segment-level audio/video deltas are small
- renderer successfully follows the supplied audio master duration
- report does not reconcile that local expected duration against manifest target_duration_sec = 480

## projects/P2026_TEST_001/visual_pacing/visual_pacing_plan.json

Observed:

- executor = visual_pacing_executor v1.0.1
- source_phase = QA
- audio_master_clock = true
- scene_count = 9
- beat_count = 84
- target beat duration = 5.0 sec
- min beat duration = 3.0 sec
- max beat duration = 6.5 sec
- source audio duration = 390.505 sec
- total duration = 390.505 sec
- duration delta = 0
- status = VISUAL_PACING_PLAN_OK
- blockers = []
- warnings = []
- beat-level display text and motion instructions exist
- beats inside a scene generally reuse the same scene visual asset
- visual variation is primarily motion/crop/text treatment
- plan depends on an already existing final render report

## projects/P2026_TEST_001/script/script_qa.json

Observed:

- qa_gate = script_qa
- qa_version = 1.0.0
- source_phase = SCRIPT
- word_count = 1000
- estimated_duration_minutes = 6.9
- score = 100
- verdict = PASS
- warnings = []
- failure_reasons = []
- all seven scored checks receive maximum points
- multiple check details restate metadata or requirements rather than persisted script-derived evidence
- exact Script QA producer implementation has not yet been verified

These artifacts are runtime evidence.

They are not operational authority.

---

# 5. Modernization backlog

## M-001 — HALT resume safety

Source:

AUDIT-001

Required outcome:

HALT resume cannot bypass canonical production or release rules.

---

## M-002 — HALT resume regression coverage

Source:

AUDIT-002

Dependency:

M-001

Required outcome:

Unsafe HALT resume targets must be rejected by validation.

---

## M-003 — Dispatcher validation runtime consistency

Source:

AUDIT-003

Required outcome:

Runtime and validation use the same Python interpreter-resolution policy.

---

## M-004 — Brain-driven script, scene and asset requirement planning

Source:

AUDIT-004

Required outcome:

Creative niche intelligence moves out of deterministic runtime executors.

Preserve deterministic execution and canonical state handling.

Move actual creative responsibility to the appropriate Brain / Editorial / Director contracts.

The production contour must support changing:

- niche
- topic
- story
- angle
- script
- visual direction

without editing Python source code.

---

## M-005 — Shot-aware asset, assembly and render contract

Source:

AUDIT-005

Dependency:

M-004

Required outcome:

scene
-> 1..N shots
-> 1..N assets
-> production timeline
-> renderer

---

## M-006 — Pre-render Director / Visual Pacing integration

Source:

AUDIT-006

Dependencies:

- M-004
- M-005

Required outcome:

Visual pacing decisions exist before rendering and are consumed by the canonical renderer.

Runtime-confirmed preservation requirements:

- preserve audio-master-clock beat timing
- preserve deterministic beat duration validation
- preserve useful beat-level render instructions
- preserve display_text / motion_profile / visual_action as donor structures
- allow semantic Director-driven shot and asset changes inside a scene
- do not rely on repetitive pan/zoom/crop as the primary source of visual variety
- select motion based on asset type, semantic purpose and content role
- integrate the useful donor behavior into the one canonical production contour

---

## M-007 — QA and release-gate separation

Source:

AUDIT-007

Required outcome:

QA independently produces QA PASS/FAIL.

Release approval remains separate.

---

## M-008 — Provider-capable and semantically safe asset resolution

Source:

AUDIT-008

Dependencies:

- M-004
- M-005

Required outcome:

Provider-neutral resolution with meaningful semantic correspondence and preserved licensing/local fallback.

---

## M-009 — QA-approved narration integrity

Source:

AUDIT-009

Required outcome:

TTS narration is provably derived from QA-approved narration.

---

## M-010 — Safe TTS render reuse

Source:

AUDIT-010

Dependency:

M-009

Required outcome:

Audio reuse requires deterministic render identity.

---

## M-011 — Real rendered-audio duration validation

Source:

AUDIT-011

Required outcome:

Actual rendered duration must satisfy explicit production tolerance.

---

## M-012 — Enforced loudness acceptance gate

Source:

AUDIT-012

Required outcome:

Production loudness threshold violations must actually block loudness validation.

---

## M-013 — Loudness provenance binding

Source:

AUDIT-013

Dependencies:

- M-010
- M-012
- M-018

Required outcome:

A loudness report may be applied only to the exact rendered audio artifact set it measured.

Persist and verify render/audio fingerprints.

---

## M-014 — Canonical state-safe loudness application

Source:

AUDIT-014

Required outcome:

Loudness application must:

- verify state/audio/report project identity
- load canonical state through approved validator
- persist canonical state through approved state-store guard
- avoid an independent canonical-state writer

---

## M-015 — Canonical production lifecycle and phase reconciliation

Source:

AUDIT-015

Related findings:

- AUDIT-001
- AUDIT-007
- AUDIT-014

Required outcome:

Define one coherent runtime lifecycle where:

- canonical phases are explicitly defined
- dispatcher and specification agree on the phase set
- AUDIO is either a real canonical phase or an internal capability, not both
- production work required for QA has a deterministic place before the QA gate
- PROJECT_STATE.phase has one unambiguous operational meaning
- phase_history reflects meaningful lifecycle progression
- HALT/resume and transition guards use the same lifecycle contract

Do not solve this by creating a second orchestrator or parallel phase model.

---

## M-016 — Final-output QA contract

Source:

AUDIT-016

Related findings:

- AUDIT-006
- AUDIT-007
- AUDIT-011

Required outcome:

QA must evaluate the actual produced media rather than only pipeline readiness.

Minimum deterministic final-output QA should verify:

- final render report validity
- actual final duration
- audio/video synchronization
- technical media integrity
- required artifact provenance

Quality-sensitive checks should evaluate final output against Director / content intent where appropriate.

Upstream PASS/readiness fields may support QA.

They must not replace independent final-output validation.

Release approval remains separate.

---

## M-017 — Evidence-backed Script QA

Source:

AUDIT-017

Related findings:

- AUDIT-009
- AUDIT-016

Required outcome:

Script QA must persist auditable script-derived evidence for every scored criterion.

The contract should support:

- evidence-backed hook evaluation
- topic coverage
- structure quality
- practical payoff
- voiceover usability
- factual-claim and citation-risk review
- explicit warnings
- explicit failure reasons
- reproducible scoring inputs

Qualitative model judgment may be used when useful, but a PASS must include enough structured evidence to understand why it passed.

Do not treat manifest metadata itself as proof of script quality.

First identify and inspect the current Script QA producer before selecting its implementation disposition.

---

## M-018 — Loudness applicator runtime-path fix

Source:

AUDIT-018

Related findings:

- AUDIT-013
- AUDIT-014

Required outcome:

Make the loudness validator contract explicit and executable.

audio_render_path must be passed explicitly into the validator.

The corrected path must:

- avoid undefined-variable access
- preserve source-path validation
- fail through controlled domain errors
- include successful-path regression coverage
- include source-path mismatch regression coverage
- preserve fail-closed behavior

Do not treat this narrow fix as sufficient resolution for:

- loudness provenance binding
- canonical state safety

Those remain separately tracked by M-013 and M-014.

---

# 6. Modernization sequencing note

No implementation priority is authorized by this audit file.

Priority will be selected after sufficient audit evidence exists.

Current connected groups:

Control plane and orchestration:

- M-001
- M-002
- M-003
- M-014
- M-015

Creative / Editorial / Director / production quality:

- M-004
- M-005
- M-006

Asset autonomy:

- M-008

Script / QA / narration integrity:

- M-007
- M-009
- M-016
- M-017

Audio correctness:

- M-010
- M-011
- M-012
- M-013
- M-018

Do not implement all groups simultaneously.

The final modernization plan must select the smallest high-impact change set after audit exit conditions are satisfied.

---

# 7. Current audit summary

Files materially audited:

21

Supporting runtime artifacts materially inspected:

10

Material findings:

18

Confirmed findings:

18

Confirmed RED blockers:

0

Confirmed ORANGE findings:

17

Confirmed YELLOW findings:

1

KEEP:

6

ADAPT:

15

REPLACE:

0

REMOVE:

0

UNKNOWN:

1

Current confirmed KEEP components:

- tools/dispatcher_cli.py
- tools/dispatcher.sh
- engine/state_validator.py
- engine/state_store.py
- Makefile
- tools/render_visual_pacing_preview.py

Current confirmed ADAPT components:

- engine/canonical_dispatcher.py
- tools/run_dispatcher_checks.py
- tools/check_dispatcher.sh
- engine/executors/script_executor.py
- engine/executors/scenes_executor.py
- engine/executors/assets_executor.py
- engine/executors/asset_resolver.py
- engine/executors/assembly_executor.py
- engine/executors/audio_executor.py
- engine/executors/audio_renderer.py
- tools/audio_loudness_report.py
- tools/apply_audio_loudness_report.py
- engine/executors/final_render_executor.py
- engine/executors/visual_pacing_executor.py
- engine/executors/qa_executor.py

Current UNKNOWN components:

- Script QA producer implementation

Current direction:

Continue system audit.

No production implementation is authorized by this file.

End.