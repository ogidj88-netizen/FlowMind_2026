# FLOWMIND AUDIT FINDINGS V1

Status: ACTIVE AUDIT RECORD
Project: FlowMind / Imagine What If
Mode: SYSTEM AUDIT MODE
Authority: NONE
Purpose: persistent record of material findings discovered during system audit

This file is NOT:

- current operational authority
- target architecture
- runtime proof
- implementation authorization

It records material audit findings so they are not lost.

---

## 1. Finding types

KEEP
= component fits the target and no material modernization issue is identified.

RISK
= potential problem exists but additional evidence is required.

ADAPT
= component should remain but requires future modification.

REPLACE
= responsibility remains necessary but should probably move to a better implementation or external provider.

REMOVE
= component is unnecessary, obsolete, duplicated, or harmful.

GAP
= required capability is materially missing.

---

## 2. Severity

GREEN
= healthy / no material action required.

YELLOW
= confirmed or plausible issue that should be corrected but does not currently block the audit or production architecture.

ORANGE
= confirmed significant modernization or control issue with material architecture, reliability, cost, quality, or validation impact.

RED
= critical defect, safety/control issue, or blocker that requires pausing the audit because continuing would be unsafe, misleading, or impossible.

---

## 3. Resolution rule

During SYSTEM AUDIT MODE:

- material findings are recorded
- production code is not modified by default
- YELLOW and ORANGE findings normally wait until modernization planning
- RED findings pause the audit when continuing would be unsafe, misleading, or impossible
- suspected defects must not be silently upgraded to confirmed defects
- insufficient evidence remains explicitly unresolved

A finding is closed only after implementation and validation evidence exist.

---

## 4. Findings

### AUDIT-001

Component:

engine/canonical_dispatcher.py

Related components inspected:

- engine/state_validator.py
- engine/state_store.py
- tools/dispatcher_cli.py

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Finding:

HALT resume policy permits resuming directly into any phase included in RESUMABLE_PHASES.

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

Instead it:

1. verifies current phase is HALT
2. checks only that requested target belongs to RESUMABLE_PHASES
3. directly changes phase
4. clears HALT state
5. appends phase history
6. invokes _assert_phase_guards("HALT", target, candidate_state)
7. writes the candidate state

Observed _assert_phase_guards() rules cover:

- AUDIO -> QA
- QA -> READY_FOR_UPLOAD
- READY_FOR_UPLOAD -> UPLOADED

No HALT-specific resume guard exists in canonical_dispatcher.py.

Verification of engine/state_validator.py confirmed:

- state structure is validated
- phase names are validated
- phase_history structure is validated
- HALT/halted consistency is validated
- manifest integrity is validated

But state_validator.py does not validate legal phase-transition semantics.

Verification of engine/state_store.py confirmed:

- candidate state is validated
- immutable/runtime mutation boundaries are checked
- manifest mutation rules are checked
- writes are atomic and disk-guarded

But state_store.py does not validate legal phase-transition semantics.

Therefore no inspected lower-level guard prevents a structurally valid transition such as:

HALT -> READY_FOR_UPLOAD

when READY_FOR_UPLOAD is included in RESUMABLE_PHASES.

Risk:

The canonical control plane can bypass normal sequential phase-transition rules during HALT resume.

This may allow a project to resume at a later production/release phase without proving that the required normal transition path was completed.

Current audit decision:

Do not repair during SYSTEM AUDIT MODE.

This is a confirmed ORANGE control-plane defect, but it does not currently block or invalidate the audit because the resume path is not required for audit execution.

Required future correction:

Resume must be constrained by verified prior state and explicit resume policy.

A future implementation should:

- record or derive the only valid resume destination
- reject arbitrary resume targets
- preserve fail-closed behavior
- preserve phase history
- prevent bypass of QA or release gates
- add tests proving invalid HALT resume targets fail

Do not duplicate transition semantics inside state_validator.py or state_store.py unless the final architecture provides a single shared transition-policy contract.

Resolution status:

OPEN

---

### AUDIT-002

Component:

tools/run_dispatcher_checks.py

Related finding:

AUDIT-001

Classification:

ADAPT

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Finding:

The dispatcher validation suite does not detect the unsafe HALT resume behavior identified in AUDIT-001.

run_resume_test() constructs a synthetic state directly in phase:

HALT

with:

resume_hint = "resume_to_audio"

It then executes:

resume_from_halt("AUDIO")

and treats successful transition to AUDIO as the expected result.

The test verifies:

- resulting phase is AUDIO
- halted becomes false
- halt_reason is cleared
- resume_hint is cleared

But it does not verify:

- which valid production phase existed before HALT
- whether the requested resume target is derived from prior verified state
- whether the requested target is constrained by resume_hint
- whether arbitrary later-phase resume is rejected
- whether HALT -> READY_FOR_UPLOAD is rejected
- whether release gates can be bypassed through resume

Therefore the validation suite can finish with:

DISPATCHER_CHECKS_ALL_OK

while AUDIT-001 remains present.

Risk:

Dispatcher checks may provide false confidence that canonical transition behavior is safe.

Current audit decision:

Do not modify the validation suite during SYSTEM AUDIT MODE.

Required future correction:

After the HALT resume policy is corrected, dispatcher validation must include regression coverage for:

- valid resume to the explicitly permitted phase
- invalid resume to an unrelated earlier phase
- invalid resume to an unrelated later phase
- HALT -> READY_FOR_UPLOAD bypass attempt
- mismatch between recorded resume destination and requested destination
- preservation of QA and upload approval gates
- failure behavior remaining fail-closed

Resolution status:

OPEN

---

### AUDIT-003

Component:

tools/check_dispatcher.sh

Classification:

ADAPT

Severity:

YELLOW

Status:

CONFIRMED — OPEN

Finding:

The dispatcher validation wrapper does not use the same Python interpreter selection policy as the active dispatcher runtime wrapper.

Observed runtime wrapper behavior in tools/dispatcher.sh:

1. prefer .venv/bin/python
2. otherwise use python3
3. fail explicitly if neither exists

Observed validation wrapper behavior in tools/check_dispatcher.sh:

- uses python directly for py_compile
- uses python directly for run_dispatcher_checks.py

Therefore dispatcher validation may execute under a different Python interpreter or environment than the actual dispatcher runtime.

Risk:

Validation may pass or fail in an environment that is not identical to the environment used by the active dispatcher command surface.

This creates avoidable uncertainty around runtime validation.

No current evidence proves that this mismatch has caused an actual production failure.

Additional relationship:

tools/check_dispatcher.sh ultimately runs tools/run_dispatcher_checks.py.

Therefore its final:

[dispatcher-check] OK

also inherits the incomplete HALT resume validation described by AUDIT-002.

That inherited limitation is not classified as a separate additional defect.

Current audit decision:

Do not modify during SYSTEM AUDIT MODE.

Required future correction:

Dispatcher validation should use the same interpreter-resolution policy as the canonical runtime command surface.

Preferred outcome:

- use the project virtual environment when available
- use the same fallback policy as dispatcher.sh
- fail explicitly when the required runtime is unavailable
- avoid validating with one Python environment and running production with another

Resolution status:

OPEN

---

## 5. Audited component classifications

### engine/canonical_dispatcher.py

Classification:

ADAPT

Reason:

Core control-plane responsibility is correct and should remain internal FlowMind logic.

Confirmed AUDIT-001 requires future correction.

---

### tools/dispatcher_cli.py

Classification:

KEEP

Reason:

Thin operator interface over CanonicalDispatcher.

Does not duplicate phase or state logic.

No independent material defect identified.

---

### tools/dispatcher.sh

Classification:

KEEP

Reason:

Thin shell entrypoint into dispatcher_cli.py.

Uses fail-fast shell behavior and explicit interpreter selection.

No material defect identified.

---

### engine/state_validator.py

Classification:

KEEP

Reason:

Provides structural state validation, manifest validation, type checks, immutable-state protection, and integrity validation.

Transition semantics should remain owned by control-plane transition policy rather than being duplicated here.

No independent material defect identified.

---

### engine/state_store.py

Classification:

KEEP

Reason:

Provides validated, atomic and durable PROJECT_STATE writes.

Uses temp file replacement, fsync, validation, mutation guards, and cleanup on failure.

Transition semantics are outside its current responsibility.

No independent material defect identified.

---

### tools/run_dispatcher_checks.py

Classification:

ADAPT

Reason:

The validation suite provides useful smoke, rollback, QA, and approval coverage.

However, its resume validation does not detect AUDIT-001 and can report DISPATCHER_CHECKS_ALL_OK while unsafe HALT resume behavior remains possible.

Confirmed AUDIT-002 requires future correction.

---

### tools/check_dispatcher.sh

Classification:

ADAPT

Reason:

The wrapper is structurally simple and fail-fast.

However, it uses python directly instead of matching the canonical runtime interpreter-selection policy.

Confirmed AUDIT-003 requires future correction.

---

## 6. Modernization backlog

Current modernization items:

### M-001 — HALT resume safety

Source:

AUDIT-001

Priority:

To be ranked after system audit.

Required outcome:

HALT resume cannot bypass canonical production or release transition rules.

Implementation remains unauthorized during SYSTEM AUDIT MODE.

---

### M-002 — HALT resume regression coverage

Source:

AUDIT-002

Dependency:

M-001

Priority:

To be ranked after system audit.

Required outcome:

Dispatcher checks must fail when an unauthorized HALT resume target is requested and must prove preservation of QA and upload approval gates.

Implementation remains unauthorized during SYSTEM AUDIT MODE.

---

### M-003 — Dispatcher validation runtime consistency

Source:

AUDIT-003

Priority:

To be ranked after system audit.

Required outcome:

Dispatcher validation and dispatcher runtime use the same Python interpreter-selection policy.

Implementation remains unauthorized during SYSTEM AUDIT MODE.

---

## 7. Current audit summary

Files materially audited:

7

Material findings:

3

Confirmed findings:

3

Confirmed RED blockers:

0

Confirmed ORANGE findings:

2

Confirmed YELLOW findings:

1

KEEP:

4

ADAPT:

3

REPLACE:

0

REMOVE:

0

UNKNOWN:

0

Current direction:

Continue system audit.

End.