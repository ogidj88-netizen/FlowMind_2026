# FLOWMIND AUDIT FINDINGS V1

Status: ACTIVE AUDIT RECORD
Project: FlowMind / Imagine What If
Mode: SYSTEM AUDIT MODE
Authority: NONE

Purpose:

Persistent record of material findings discovered during system audit.

This file is not:

- operational authority
- target architecture
- runtime proof
- implementation authorization

---

## 1. Classification

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

= confirmed significant architecture, control, reliability, validation, automation, or quality issue.

RED

= critical blocker requiring audit pause.

SYSTEM AUDIT MODE rule:

YELLOW and ORANGE findings are recorded but not implemented by default.

RED may pause the audit.

---

## 2. Findings

### AUDIT-001 — Unsafe HALT resume policy

Component:

engine/canonical_dispatcher.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

resume_from_halt() accepts any target contained in RESUMABLE_PHASES rather than deriving one permitted resume destination from verified prior state.

The resume path directly mutates state after HALT-specific checks but does not use the normal sequential ALLOWED_PHASE_TRANSITIONS model.

No inspected lower-level validation in:

- engine/state_validator.py
- engine/state_store.py

prevents a structurally valid resume such as:

HALT -> READY_FOR_UPLOAD

Risk:

Normal sequential production and release gates can be bypassed during HALT resume.

Preserve:

- narrow dispatcher responsibility
- explicit HALT state
- state history
- validation before persistence
- fail-closed errors

Required outcome:

- explicit canonical resume policy
- verified resume destination derived from safe state/history
- rejection of arbitrary resume targets
- QA/release gate preservation
- fail-closed invalid target behavior
- regression coverage

Resolution:

OPEN

---

### AUDIT-002 — Dispatcher validation misses unsafe resume

Component:

tools/run_dispatcher_checks.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

run_resume_test() treats direct:

HALT -> AUDIO

resume as expected success but does not test:

- verified prior phase
- permitted resume destination
- invalid arbitrary resume targets
- HALT -> READY_FOR_UPLOAD
- release-gate bypass

Therefore:

DISPATCHER_CHECKS_ALL_OK

can occur while AUDIT-001 remains present.

Risk:

Validation can report healthy dispatcher behavior while an unsafe resume path remains possible.

Preserve:

- deterministic dispatcher smoke checks
- forward transition checks
- rollback/failure checks
- explicit validation output

Required outcome:

Add negative resume regression coverage after AUDIT-001 is corrected.

Resolution:

OPEN

---

### AUDIT-003 — Dispatcher validation Python mismatch

Component:

tools/check_dispatcher.sh

Classification:

ADAPT

Severity:

YELLOW

Status:

CONFIRMED — OPEN

Evidence:

tools/dispatcher.sh resolves runtime Python through:

- .venv/bin/python
- python3 fallback
- explicit failure when neither exists

tools/check_dispatcher.sh invokes:

python

directly.

Risk:

Validation and runtime may execute under different Python environments.

No current evidence proves that this mismatch has already caused a production failure.

Required outcome:

Use the same interpreter-resolution policy for runtime and validation.

Resolution:

OPEN

---

### AUDIT-004 — Hard-coded niche intelligence inside scene and asset planning

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

SCENES creative logic contains historical niche-specific concepts including:

- refrigerator
- water heater
- dryer
- freezer
- pool pump
- bill
- kilowatt
- fixed charges
- utility bills
- home energy
- hidden costs

SCENES also combines responsibilities for:

- scene segmentation
- asset-type selection
- visual intent
- on-screen text
- production notes

with fixed assumptions including:

- 145 WPM
- 6–18 scenes
- English-only execution

ASSETS planning continues the niche coupling.

build_asset_query() contains hard-coded queries including:

- utility bill cost breakdown usage rate fixed charges
- checklist compare electricity bill usage rate fixed charges
- home appliances electricity usage refrigerator water heater
- household energy costs simple home finance

This means reusable FlowMind runtime logic contains creative intelligence specific to one historical electricity / invisible-cost content example.

Risk:

Changing niche or creative direction requires code-level behavior changes instead of Brain / Director decisions.

The current executor chain mixes deterministic execution responsibilities with productive intelligence.

Preserve:

- SCENES phase guard
- ASSETS phase guard
- Script QA dependency
- structured artifacts
- required-field validation
- forbidden-marker validation
- deterministic persistence
- canonical state registration
- surfaced failures

Required outcome:

FlowMind Brain / Director

-> semantic scene / shot intent

-> asset requirements

-> capability contract

-> selected provider / resolver

-> normalized artifacts

-> deterministic validation and persistence

Creative query generation must come from content context or Director decisions rather than historical niche constants embedded in runtime code.

Resolution:

OPEN

---

### AUDIT-005 — Scene-level asset, assembly and render contract blocks shot-aware production

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

The limitation begins during asset planning.

assets_executor.py builds:

one asset entry for each scene

through the effective contract:

scene
-> one asset_id
-> one asset_type
-> one asset_query
-> duration of the scene

The current runtime artifact confirms:

9 scenes
-> 9 planned assets

The resolved-assets artifact confirms:

9 scenes
-> 9 resolved assets

Assembly continues the same structure.

build_asset_index() rejects more than one asset for the same scene_id.

Assembly represents:

scene
-> one asset
-> one timeline item

validate_timeline() requires:

timeline length == scene count

Final rendering continues the same contract.

final_render_executor.py builds one render job per timeline scene using:

- one scene_id
- one asset_id
- one visual asset
- one audio segment

For image assets the same image is held for the scene duration.

For video assets the same visual asset may be looped for the scene duration.

Scene MP4 files are then concatenated into the canonical final video.

Risk:

The canonical production contract cannot naturally represent:

- multiple shots inside one scene
- multiple visual assets inside one scene
- shot-specific timing
- shot-specific provider outputs
- semantic visual changes inside long narration scenes

This structurally creates slideshow / PowerPoint-style output even when downstream pacing logic exists.

Preserve:

- planning-only separation in assets/assembly
- structured asset metadata
- deterministic validation
- resolved asset references
- timeline ordering
- duration validation
- FFmpeg/FFprobe technical checks
- canonical state registration
- final render report

Required outcome:

scene

-> shot / beat requirements

-> one or more asset requirements

-> resolved assets

-> shot timing + motion + visual role

-> normalized production timeline

-> final renderer

The target contract must support:

1 scene -> 1..N shots -> 1..N assets

where creative intent requires it.

Resolution:

OPEN

---

### AUDIT-006 — Visual Pacing is post-render and disconnected from canonical production render

Components:

- engine/executors/visual_pacing_executor.py
- engine/executors/final_render_executor.py

Positive donor component:

tools/render_visual_pacing_preview.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

visual_pacing_executor.py requires:

PROJECT_STATE.phase = QA

and also requires:

final_render_report.verdict = PASS

plus an already existing:

PROJECT_STATE.artifacts.final_video_path

Therefore visual_pacing_plan.json is generated only after a canonical final render already exists and has passed its render report.

final_render_executor.py does not consume:

- visual_pacing_plan
- beats
- visual_action
- motion_profile
- display_text

The canonical renderer therefore remains scene-level.

The pacing plan cannot influence the final video that was required as its own precondition.

Beat structure is also limited by the upstream one-asset-per-scene contract.

Each beat inside the same scene reuses the same:

- asset_id
- source_visual_path
- source_audio_path

Variation is generated mainly through:

- crop
- pan
- zoom
- display-text decisions

Visual actions are largely produced by deterministic sequencing rather than semantic Director decisions.

Fixed pacing policy includes:

- target beat duration = 5.0 sec
- minimum beat duration = 3.0 sec
- maximum beat duration = 6.5 sec

validate_beats() also requires:

beat_count > scene_count

which can reject valid material where one natural beat per scene is appropriate.

Positive evidence:

tools/render_visual_pacing_preview.py proves that usable beat-level rendering logic already exists.

The preview renderer:

- consumes visual_pacing_plan.json
- validates beat timing
- renders individual beat segments
- applies motion_profile
- applies visual_action
- trims/synchronizes audio for beat segments
- validates duration drift
- concatenates beat segments
- creates a preview report

It correctly remains isolated from canonical production state.

It explicitly does not:

- replace production final_video.mp4
- update PROJECT_STATE
- approve upload

Risk:

FlowMind already contains useful beat-level rendering capability, but it exists outside the canonical production path.

Building a second renderer from scratch would waste existing verified functionality.

Preserve:

- audio master clock
- beat timing contract
- duration consistency validation
- source file verification
- structured visual_pacing_plan
- existing preview beat rendering logic
- motion/action FFmpeg implementation
- explicit preview isolation
- fail-closed validation

Required future outcome:

FlowMind Brain / Director

-> shot and pacing decisions

-> provider execution / resolved assets

-> normalized shot/beat production plan

-> canonical renderer consumes that plan

-> QA evaluates rendered output

The existing preview renderer should be treated as a donor implementation for the future production render bridge rather than as a second production contour.

Deterministic motion heuristics may remain as fallback behavior but must not replace Director decisions.

Resolution:

OPEN

---

### AUDIT-007 — QA executor contains a circular release gate and cannot produce QA PASS

Component:

engine/executors/qa_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

QA first evaluates production checks.

It then computes upload_ready using:

all existing checks PASS

and:

state.qa_passed is True

and:

state.approved_for_upload is True

The upload_readiness check is then appended to the QA checks.

However the canonical control model separates:

QA PASS

from:

release / upload approval

QA is expected to establish whether quality passed.

Release approval belongs after successful QA.

The implementation then explicitly sets:

verdict = "BLOCKED"

qa_passed = False

approved_for_upload = False

regardless of the preceding technical checks.

When PROJECT_STATE is persisted, the executor explicitly writes:

candidate_state["qa_passed"] = False

The returned result also reports:

qa_passed = False

Risk:

The QA executor cannot itself produce the state required for the normal:

QA -> READY_FOR_UPLOAD

transition.

The release condition depends on values that QA itself cannot legitimately possess beforehand.

This creates a circular gate:

QA requires prior QA/release approval

while QA is supposed to generate the QA result needed before release approval.

Required outcome:

QA executor:

-> evaluate output
-> PASS or FAIL
-> persist verified qa_passed result

Dispatcher:

-> enforce QA -> READY_FOR_UPLOAD using qa_passed

Release / human approval:

-> produce approved_for_upload separately

Dispatcher:

-> enforce READY_FOR_UPLOAD -> UPLOADED

QA must not require upload approval in order to decide whether QA itself passed.

verdict must be derived from actual QA checks rather than hard-coded BLOCKED.

Resolution:

OPEN

---

### AUDIT-008 — Asset Resolver is local-only and can resolve weak semantic matches

Component:

engine/executors/asset_resolver.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Current resolver mode is hard-coded:

PROVIDER_MODE = "local_existing_only"

Approved media sources are limited to:

- assets_library
- projects/<project_id>/manual_assets

The resolver supports only:

stock_first_no_repeat

and rejects other stock policies.

No provider adapter or external execution path exists in this resolver.

This means autonomous asset acquisition is not currently implemented here.

The local fallback and licensing behavior are useful, but candidate selection also has a match-quality weakness.

score_candidate() awards points for:

- asset_id filename match
- scene_id filename match
- asset_type filename match
- query-token filename overlap
- compatible file extension

A compatible file extension alone can provide a positive score.

For example:

a stock_video candidate receives points merely for being:

.mp4
.mov
.mkv

even if its filename has no semantic overlap with the asset query.

Image asset types receive the same type-only extension bonus.

choose_candidate() accepts any candidate with:

score > 0

and selects the highest score.

There is no minimum semantic-match threshold.

Therefore a licensed but semantically unrelated media file can be selected and marked:

provider_status = resolved

license_status = cleared

resolution_status = ready

provided it wins the local score.

Risk:

Two separate limitations exist:

1. autonomous/provider-based asset resolution is absent from the current resolver;
2. local fallback resolution can incorrectly classify a weak type-only match as production-ready.

This can create visually irrelevant output while the technical state reports successful asset resolution.

Positive evidence worth preserving:

- local fallback capability
- approved search directories
- no-repeat used_paths behavior
- deterministic candidate ranking
- explicit blocked assets
- license sidecar requirement
- source_provider recording
- license_note recording
- blocker reporting
- resolved/blocked counts
- forbidden-marker validation
- canonical artifact registration
- fail-closed validation

Required outcome:

Asset Requirement Planner

-> provider-neutral capability request

-> selected provider adapter or approved local fallback

-> candidate quality validation

-> license validation

-> normalized resolved asset

Local fallback should remain supported.

Provider adapters should remain replaceable.

Candidate acceptance must require meaningful correspondence to the requested asset, not merely a compatible extension.

Suitable approaches may include:

- explicit asset/scene binding
- provider-returned request IDs
- metadata matching
- semantic similarity threshold
- deterministic minimum score requiring semantic evidence

The exact implementation should be selected during modernization planning.

Resolution:

OPEN

---

## 3. Audited classifications

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

engine/executors/final_render_executor.py

= ADAPT

engine/executors/visual_pacing_executor.py

= ADAPT

tools/render_visual_pacing_preview.py

= KEEP

engine/executors/qa_executor.py

= ADAPT

---

## 4. Supporting runtime evidence inspected

projects/P2026_TEST_001/assets/assets.json

Observed:

- 9 planned assets
- 9 scenes
- effective one-asset-per-scene planning model
- provider_status = planned
- local_path = null
- source_url = null
- license_status = pending

projects/P2026_TEST_001/assets/resolved_assets.json

Observed:

- 9 resolved assets
- 9 scenes
- one resolved asset per scene in the current project
- provider_mode = local_existing_only
- source_provider = manual
- licenses cleared through local evidence
- no blockers in the inspected artifact

These artifacts are runtime evidence.

They are not operational authority.

---

## 5. Modernization backlog

### M-001 — HALT resume safety

Source:

AUDIT-001

Required outcome:

HALT resume cannot bypass canonical production or release transition rules.

---

### M-002 — HALT resume regression coverage

Source:

AUDIT-002

Dependency:

M-001

Required outcome:

Dispatcher validation rejects unsafe or arbitrary HALT resume targets.

---

### M-003 — Dispatcher validation runtime consistency

Source:

AUDIT-003

Required outcome:

Dispatcher runtime and validation use the same Python interpreter-resolution policy.

---

### M-004 — Brain-driven scene and asset requirement planning

Source:

AUDIT-004

Required outcome:

Niche-specific creative intelligence moves out of deterministic runtime executors.

Scene / asset requirements are produced from current content intent rather than hard-coded historical topic logic.

---

### M-005 — Shot-aware asset, assembly and render contract

Source:

AUDIT-005

Dependency:

M-004

Required outcome:

Canonical production supports:

scene
-> 1..N shots
-> 1..N asset requirements
-> resolved assets
-> timing / motion
-> production timeline
-> renderer

without forcing one asset and one render item per scene.

---

### M-006 — Pre-render Director / Visual Pacing integration

Source:

AUDIT-006

Dependencies:

M-004
M-005

Required outcome:

Visual pacing / shot decisions exist before canonical final rendering and are consumed by the production renderer.

Reuse proven beat-rendering behavior from:

tools/render_visual_pacing_preview.py

where appropriate.

Do not create a second production contour.

---

### M-007 — QA and release-gate separation

Source:

AUDIT-007

Required outcome:

QA derives and persists its own PASS / FAIL result.

Upload approval remains a separate release decision after QA.

qa_passed must not depend on approved_for_upload.

---

### M-008 — Provider-capable and semantically safe asset resolution

Source:

AUDIT-008

Dependencies:

M-004
M-005

Required outcome:

Preserve local fallback and license validation while introducing a provider-neutral resolution contract.

Resolved assets must satisfy meaningful request correspondence before being marked ready.

Type-only / extension-only candidate matches must not be sufficient for production acceptance.

---

## 6. Modernization sequencing note

No implementation priority is authorized by this audit file.

Priority will be selected after sufficient system audit evidence exists.

Current evidence suggests several connected modernization groups:

Control plane:

- M-001
- M-002
- M-003

Creative / Director / production quality:

- M-004
- M-005
- M-006

Asset autonomy and correctness:

- M-008

QA / release correctness:

- M-007

Do not implement all groups at once.

The final modernization plan must select the smallest high-impact change set after the audit exit conditions are satisfied.

---

## 7. Current audit summary

Files materially audited:

16

Supporting runtime artifacts materially inspected:

2

Material findings:

8

Confirmed findings:

8

Confirmed RED blockers:

0

Confirmed ORANGE findings:

7

Confirmed YELLOW findings:

1

KEEP:

6

ADAPT:

10

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
- engine/executors/final_render_executor.py
- engine/executors/visual_pacing_executor.py
- engine/executors/qa_executor.py

Current direction:

Continue system audit.

No production implementation is authorized by this file.

End.