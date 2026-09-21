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

engine/state_validator.py validates state structure, phase names, manifest integrity and HALT consistency, but does not validate legal transition semantics.

engine/state_store.py validates state and mutation boundaries and provides atomic durable writes, but also does not validate legal transition semantics.

Therefore no inspected lower-level guard prevents a structurally valid transition such as:

HALT -> READY_FOR_UPLOAD

when that target is present in RESUMABLE_PHASES.

Risk:

HALT resume can potentially bypass the normal sequential production and release transition path.

Required future outcome:

- valid resume destination must come from verified prior state or explicit canonical resume policy
- arbitrary resume targets must fail closed
- QA and release gates must remain impossible to bypass
- regression tests must prove invalid resume attempts fail

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

run_resume_test() creates a synthetic HALT state and successfully executes:

resume_from_halt("AUDIO")

The test verifies only that:

- phase becomes AUDIO
- halted becomes false
- halt_reason is cleared
- resume_hint is cleared

It does not verify:

- actual phase before HALT
- canonical permitted resume destination
- resume_hint/target consistency
- rejection of arbitrary resume targets
- rejection of HALT -> READY_FOR_UPLOAD
- preservation of release gates through resume

Therefore the suite can report:

DISPATCHER_CHECKS_ALL_OK

while AUDIT-001 remains present.

Required future outcome:

After AUDIT-001 is corrected, add negative regression coverage for invalid resume destinations and release-gate bypass attempts.

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

tools/dispatcher.sh selects runtime Python using:

1. .venv/bin/python
2. fallback to python3
3. explicit failure if unavailable

tools/check_dispatcher.sh instead invokes:

python

directly for compilation and dispatcher checks.

Risk:

Validation may run under a different interpreter/environment from the actual dispatcher runtime.

No evidence currently proves this mismatch has caused a production failure.

Required future outcome:

Validation and runtime must use the same Python interpreter-selection policy.

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

Scene generation contains hard-coded domain terms including examples such as:

- refrigerator
- water heater
- dryer
- freezer
- pool pump
- bill
- charges
- kilowatt
- fixed charges

Visual intent contains niche-specific assumptions such as:

- utility bill visuals
- household energy use
- hidden-cost explanation

The executor also combines several creative responsibilities:

- script segmentation
- scene generation
- asset-type selection
- visual-intent generation
- on-screen text generation
- production-note generation

Current segmentation is primarily paragraph-driven.

Current fixed policy also includes:

- WORDS_PER_MINUTE = 145
- MIN_SCENE_COUNT = 6
- MAX_SCENE_COUNT = 18
- English-only content execution

Risk:

A supposedly reusable FlowMind production component contains creative intelligence specialized for one historical niche.

This reduces:

- generality
- creative quality
- adaptability to new niches
- usefulness of Director Brain
- provider interchangeability

It also mixes responsibilities that target architecture v2.2 separates across scene/shot planning, visual concept, asset strategy and overlay/text planning.

Positive evidence:

The executor has useful structural behavior worth preserving:

- canonical SCENES phase guard
- script QA gate
- structured scenes artifact
- placeholder rejection
- explicit validation
- canonical state artifact registration
- surfaced failures

Required future outcome:

Preserve the useful executor/artifact boundary, but remove hard-coded niche creative intelligence.

Target direction:

FlowMind Brain / Director decision
-> capability contract
-> selected AI provider where appropriate
-> normalized scene / shot / visual plan
-> deterministic validation
-> artifact persistence
-> canonical state registration

Do not move provider identity into the canonical contract.

Fixed pacing and language policy should become configurable or decision-derived only where real use cases require it.

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

Dispatcher runtime and dispatcher validation use the same Python interpreter-selection policy.

---

### M-004 — Brain-driven scene planning

Source:

AUDIT-004

Required outcome:

Remove historical niche-specific creative logic from scenes_executor while preserving useful validation, artifact and canonical-state boundaries.

Scene, shot, visual, asset and overlay decisions must follow target architecture v2.2 responsibilities and remain provider-agnostic at the contract level.

---

## 5. Current audit summary

Files materially audited:

9

Material findings:

4

Confirmed findings:

4

Confirmed RED blockers:

0

Confirmed ORANGE findings:

3

Confirmed YELLOW findings:

1

KEEP:

5

ADAPT:

4

REPLACE:

0

REMOVE:

0

UNKNOWN:

0

Current direction:

Continue system audit.

End.