# FLOWMIND AUDIT FINDINGS V1

Status: ACTIVE AUDIT RECORD
Project: FlowMind / Imagine What If
Mode: SYSTEM AUDIT MODE
Authority: NONE
Purpose: persistent record of material findings discovered during system audit

This file is not operational authority, target architecture, runtime proof, or implementation authorization.

---

## 1. Classification

KEEP
= component fits the target with no material modernization requirement found.

ADAPT
= component remains useful but requires future modification.

REPLACE
= responsibility remains necessary but should move to a stronger implementation or external provider.

REMOVE
= component is obsolete, duplicated, harmful, or unnecessary.

UNKNOWN
= evidence is insufficient.

Severity:

GREEN
= healthy.

YELLOW
= confirmed or plausible issue worth correcting, but low immediate impact.

ORANGE
= confirmed material architecture, reliability, quality, control, or validation problem.

RED
= critical blocker requiring audit pause because continuing would be unsafe, misleading, or impossible.

During SYSTEM AUDIT MODE, YELLOW and ORANGE findings are recorded but not implemented by default.

RED may pause the audit.

A finding closes only after correction and validation evidence exist.

---

## 2. Findings

### AUDIT-001 — Unsafe HALT resume policy

Component:

engine/canonical_dispatcher.py

Related:

- engine/state_validator.py
- engine/state_store.py
- tools/dispatcher_cli.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

resume_from_halt() accepts any target contained in RESUMABLE_PHASES.

Observed resumable targets include:

- TOPIC
- SCRIPT
- SCENES
- ASSETS
- ASSEMBLY
- AUDIO
- QA
- READY_FOR_UPLOAD

resume_from_halt() does not use the normal ALLOWED_PHASE_TRANSITIONS path.

No HALT-specific resume guard was observed.

state_validator.py validates state structure and integrity but not legal transition semantics.

state_store.py validates state and mutation boundaries but not legal transition semantics.

Therefore no inspected lower-level guard prevents a structurally valid transition such as:

HALT -> READY_FOR_UPLOAD

Risk:

HALT resume can bypass the normal sequential production and release path.

Required future outcome:

- derive valid resume destination from verified prior state or canonical resume policy
- reject arbitrary targets
- fail closed
- preserve QA and release gates
- add regression coverage

Resolution:

OPEN

---

### AUDIT-002 — Dispatcher validation misses unsafe resume

Component:

tools/run_dispatcher_checks.py

Related:

AUDIT-001

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

run_resume_test() creates HALT state and treats:

resume_from_halt("AUDIO")

as successful expected behavior.

It verifies state cleanup but does not verify:

- prior phase
- canonical permitted resume destination
- resume target consistency
- rejection of arbitrary targets
- rejection of HALT -> READY_FOR_UPLOAD
- preservation of release gates

Therefore the suite can report:

DISPATCHER_CHECKS_ALL_OK

while AUDIT-001 remains present.

Required future outcome:

After AUDIT-001 is corrected, add negative regression coverage for invalid resume destinations and release-gate bypass.

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

tools/dispatcher.sh selects:

1. .venv/bin/python
2. python3 fallback

tools/check_dispatcher.sh instead invokes:

python

directly.

Risk:

Validation may execute under a different Python environment from runtime.

No evidence currently proves an actual production failure from this mismatch.

Required future outcome:

Runtime and validation must use the same interpreter-selection policy.

Resolution:

OPEN

---

### AUDIT-004 — Hard-coded niche intelligence inside SCENES executor

Component:

engine/executors/scenes_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Scene generation contains hard-coded domain terms such as:

- refrigerator
- water heater
- dryer
- freezer
- pool pump
- bill
- kilowatt
- fixed charges

Visual intent also contains assumptions about:

- utility bills
- household energy use
- hidden costs

The executor combines:

- script segmentation
- scene generation
- asset-type selection
- visual-intent generation
- on-screen text
- production notes

Fixed policy includes:

- WORDS_PER_MINUTE = 145
- MIN_SCENE_COUNT = 6
- MAX_SCENE_COUNT = 18
- English-only execution

Risk:

Reusable FlowMind production logic contains historical niche-specific creative intelligence and mixes responsibilities belonging to Brain / Director / Shot / Visual planning.

Positive evidence:

Useful boundaries remain:

- SCENES phase guard
- script QA gate
- structured artifact generation
- placeholder rejection
- validation
- canonical state registration
- surfaced failures

Required future outcome:

Preserve validation and artifact/state boundaries.

Move creative decision logic toward:

FlowMind Brain / Director
-> capability contract
-> selected provider
-> normalized scene / shot / visual plan
-> deterministic validation and persistence

Resolution:

OPEN

---

### AUDIT-005 — Scene-level assembly contract blocks shot-aware production

Component:

engine/executors/assembly_executor.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

The executor currently behaves as an assembly planning stage.

Input assets are required to have:

- provider_status = planned
- license_status = pending
- local_path = null
- source_url = null

Output always reports:

- assembly_status = planned
- render_ready = false

That planning-only behavior is not by itself considered a defect.

The material limitation is the timeline contract.

build_asset_index() rejects more than one asset with the same scene_id.

For every scene, run_assembly_executor() retrieves one asset by scene_id and creates exactly one timeline item.

validate_timeline() requires:

timeline length == scene count

Therefore the current contract is structurally:

scene
-> one asset
-> one timeline item

It cannot natively represent multiple shots or beats inside one scene with different assets, timing, motion, or visual roles.

This conflicts with FlowMind target architecture v2.2 where Director / Shot Planner / Visual Pacing must be able to drive shot-aware or beat-aware production.

Additional contract risk:

validate_assets_payload() allows asset_count to exceed scene_count.

However assets whose scene_id does not correspond to an actual scene are not explicitly rejected by the observed assembly logic and may not appear in the resulting timeline.

Risk:

- production assembly remains scene-level
- Director/Visual Pacing decisions cannot become first-class production timeline structure
- richer multi-shot editing requires an external bridge instead of being represented by the canonical assembly contract
- unused or orphan asset-plan entries may pass input validation

Positive evidence:

The executor has useful responsibilities worth preserving:

- ASSEMBLY phase guard
- script QA dependency
- scene and asset validation
- deterministic planning artifact
- explicit render readiness state
- canonical state artifact registration
- surfaced failures

Required future outcome:

Preserve the deterministic planning and validation boundary but evolve the assembly contract toward:

scene
-> shot / beat plan
-> one or more resolved assets
-> timing and motion instructions
-> normalized production timeline
-> renderer

Do not bind the canonical assembly contract to a specific external media or rendering provider.

The exact migration must be selected after the remaining production and render path is audited.

Resolution:

OPEN

---

## 3. Audited component classifications

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

engine/executors/assembly_executor.py
= ADAPT

---

## 4. Modernization backlog

### M-001 — HALT resume safety

Source:

AUDIT-001

Required outcome:

HALT resume cannot bypass canonical transition and release rules.

---

### M-002 — HALT resume regression coverage

Source:

AUDIT-002

Dependency:

M-001

Required outcome:

Dispatcher validation proves unauthorized resume targets fail closed.

---

### M-003 — Dispatcher validation runtime consistency

Source:

AUDIT-003

Required outcome:

Dispatcher runtime and validation use the same Python interpreter-selection policy.

---

### M-004 — Brain-driven scene planning

Source:

AUDIT-004

Required outcome:

Remove historical niche-specific creative logic from scenes_executor while preserving validation, artifact and canonical-state boundaries.

Creative planning remains provider-agnostic at the canonical contract level.

---

### M-005 — Shot-aware assembly contract

Source:

AUDIT-005

Required outcome:

Evolve scene-level assembly planning into a production contract capable of representing multiple shots or beats per scene without creating a second runtime contour.

Preserve deterministic validation and canonical state integration.

Final implementation direction must be selected only after downstream production/render components are audited.

---

## 5. Current audit summary

Files materially audited:

10

Material findings:

5

Confirmed findings:

5

Confirmed RED blockers:

0

Confirmed ORANGE findings:

4

Confirmed YELLOW findings:

1

KEEP:

5

ADAPT:

5

REPLACE:

0

REMOVE:

0

UNKNOWN:

0

Current direction:

Continue system audit.

End.