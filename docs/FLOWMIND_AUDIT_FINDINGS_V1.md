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

= insufficient evidence.

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

## AUDIT-004 — Hard-coded niche intelligence inside scene and asset planning

Components:

- engine/executors/scenes_executor.py
- engine/executors/assets_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

SCENES and ASSETS contain historical electricity / invisible-cost niche intelligence and fixed creative assumptions.

Runtime executors currently combine deterministic execution with creative decisions including:

- scene segmentation
- asset-type selection
- visual intent
- on-screen text
- production notes
- niche-specific asset queries

Risk:

Changing niche or creative direction requires runtime-code changes rather than Brain / Director decisions.

Required outcome:

Brain / Director
-> semantic scene / shot intent
-> asset requirements
-> capability contract
-> provider / resolver
-> normalized artifacts
-> deterministic validation

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

Assembly rejects more than one asset for the same scene_id.

Final rendering uses one visual asset for each scene.

Risk:

Canonical production cannot naturally represent:

- multiple shots per scene
- multiple visual assets per scene
- semantic visual changes inside long narration
- shot-specific timing
- shot-specific provider output

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

Positive evidence:

tools/render_visual_pacing_preview.py already provides usable beat-level FFmpeg rendering behavior.

Required outcome:

Brain / Director
-> shot/pacing decisions
-> resolved assets
-> normalized shot/beat plan
-> canonical renderer
-> QA

Reuse preview-rendering donor behavior where appropriate.

Do not create a second production contour.

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

validate_loudness_report() verifies:

- audio_render.project_id == report.project_id
- report.verdict = PASS
- report.loudness_validated = true
- report.fail_count = 0
- report.segment_count == audio_render.segment_count
- report.source_audio_render_path == supplied audio_render path
- report file exists

However it does not verify that the report was produced from the current content of that audio render.

There is no comparison of:

- audio_render content hash
- audio-render fingerprint
- per-segment file fingerprint
- per-segment segment_id mapping
- per-segment audio_path mapping
- per-segment measured duration
- MP3 modification/content identity

The report contains source_audio_renderer_version, but apply_audio_loudness_report.py does not compare it against the current audio_render.renderer_version.

Therefore the same path:

projects/<project>/audio/audio_render.json

may point to changed content while an older loudness report still refers to the identical path string.

If project_id and segment_count remain unchanged, that old PASS report can satisfy the current validation checks.

Risk:

Changed or regenerated audio can inherit loudness approval measured against previous audio.

This can create:

- stale QA evidence
- false loudness_validated = true
- false audio_ready = true
- production artifacts accepted without measurement of their current bytes

This risk is especially relevant because AUDIT-010 already proves audio artifacts can be reused without robust render identity.

Preserve:

- explicit report artifact
- project-id validation
- source-path recording
- fail-closed non-PASS handling
- segment-count validation

Required outcome:

Loudness evidence must be bound to the exact audio artifact set it measured.

Suitable contract:

audio render fingerprint
+
per-segment audio fingerprint
+
measurement report
-> apply only when fingerprints still match

At minimum validation must prove that the current rendered audio bytes and segment identities are the same artifacts that were measured.

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

The tool reads PROJECT_STATE through its own generic JSON reader:

state = read_json_file(state_path)

It does not use the canonical state loading/validation path used by audited executors.

After modifying state.artifacts and updated_at, it directly persists canonical PROJECT_STATE through:

write_json_atomic(state_path, state)

It does not use:

- engine.state_validator.load_state
- engine.state_store.save_state_with_disk_guard

The tool also validates project identity only between:

audio_render.project_id
and
audio_loudness_report.project_id

It does not verify:

PROJECT_STATE.project_id == audio_render.project_id

or:

PROJECT_STATE.project_id == audio_loudness_report.project_id

Therefore a CLI invocation can theoretically provide:

PROJECT_STATE from Project A

with:

audio_render from Project B
audio_loudness_report from Project B

and the report pair can pass their mutual project-id check.

The tool can then register Project B audio artifact paths into Project A state.

Risk:

- cross-project artifact contamination
- canonical state mutation outside the verified state-store guard
- invalid state persistence without canonical validation
- additional canonical-state writer outside the intended state layer

No current evidence proves this contamination has already occurred in P2026_TEST_001.

The defect is confirmed from the accepted input contract and persistence path.

Preserve:

- atomic file persistence
- explicit artifact registration
- fail-closed error handling
- explicit loudness application operation

Required outcome:

Before mutation:

PROJECT_STATE.project_id
=
audio_render.project_id
=
audio_loudness_report.project_id

Canonical state must be loaded and persisted through the approved validated state layer.

The tool must not create an independent state persistence path.

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

## M-004 — Brain-driven scene and asset requirement planning

Source:

AUDIT-004

Required outcome:

Creative niche intelligence moves out of deterministic runtime executors.

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

Required outcome:

A loudness report may be applied only to the exact rendered audio artifact set it measured.

Persist and verify render/audio fingerprints.

Stale report reuse must fail closed.

---

## M-014 — Canonical state-safe loudness application

Source:

AUDIT-014

Required outcome:

Loudness application must:

- verify state/audio/report project identity
- load canonical state through the approved validator
- persist canonical state through the approved state-store guard
- avoid introducing an independent canonical-state writer

---

# 6. Modernization sequencing note

No implementation priority is authorized by this audit file.

Priority will be selected after sufficient audit evidence exists.

Current connected groups:

Control plane:

- M-001
- M-002
- M-003
- M-014

Creative / Director / production quality:

- M-004
- M-005
- M-006

Asset autonomy:

- M-008

QA / narration integrity:

- M-007
- M-009

Audio correctness:

- M-010
- M-011
- M-012
- M-013

Do not implement all groups simultaneously.

The final modernization plan must select the smallest high-impact change set after audit exit conditions are satisfied.

---

# 7. Current audit summary

Files materially audited:

20

Supporting runtime artifacts materially inspected:

5

Material findings:

14

Confirmed findings:

14

Confirmed RED blockers:

0

Confirmed ORANGE findings:

13

Confirmed YELLOW findings:

1

KEEP:

6

ADAPT:

14

REPLACE:

0

REMOVE:

0

UNKNOWN:

0

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

Current direction:

Continue system audit.

No production implementation is authorized by this file.

End.