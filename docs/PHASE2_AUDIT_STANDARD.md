# PHASE 2 — AUDIT STANDARD

## Purpose
Phase 2 exists to remove everything that weakens one active working contour and to separate:
- what stays,
- what is frozen,
- what is removed,
- what remains uncertain pending verification.

This phase does not design a new abstract architecture.
This phase cleans the real system until one stable contour becomes visible.

---

## Core Rule
We do not ask:
- "What else can be added?"

We ask:
- "What remains if everything non-critical is removed?"

---

## Canon Frame For Audit
A block may remain in the future canonical working contour only if it passes all relevant checks below.

### 1. One Active Contour
The block must belong to one active working contour now.
If it creates or supports a parallel contour, it fails.

### 2. Real Execution Need
The block must be needed for a real execution path.
Not "useful later", not "strategically interesting", but needed for the real working flow.

### 3. No Functional Duplication
If the block duplicates another block's function, one of them must be frozen or removed.

### 4. No Second Control Center
The block must not create a second center of control, orchestration, truth, routing, or decision-making.

### 5. Clear Role
The block's role must be explainable in one short practical sentence.
If its role is vague, inflated, or abstract, it fails.

### 6. No Complexity Cascade
If keeping the block requires adding multiple extra layers, bridges, adapters, or side-logic, it is a freeze/remove candidate.

### 7. Stability Over Cleverness
The block must improve stability, clarity, or execution reliability.
Pure conceptual sophistication is not enough.

---

## Allowed Audit Outcomes

### KEEP
Use only if the block:
- belongs to the one active contour,
- is needed now,
- has a clear role,
- does not duplicate,
- does not create extra control logic.

### FREEZE
Use if the block:
- may be useful later,
- is strong but not timely,
- requires extra architecture around itself,
- does not help the nearest real execution cycle.

### REMOVE
Use if the block:
- duplicates meaning or function,
- creates confusion,
- pulls the system into parallel architecture thinking,
- has no clear place in one contour,
- adds complexity before need.

### UNCERTAIN
Use only if:
- the block may matter,
- but current evidence is not enough to keep or remove it honestly,
- and it requires direct inspection later.

---

## Audit Decision Template

For each audited block, we must state:

### Block Name
### Practical Role
### Belongs to one active contour? (yes/no)
### Needed for real execution now? (yes/no)
### Duplicates another function? (yes/no)
### Creates extra complexity or control logic? (yes/no)
### Verdict:
- KEEP
- FREEZE
- REMOVE
- UNCERTAIN

### Reason:
One short direct explanation.

---

## Restrictions
During Phase 2:
- no new parallel architecture,
- no migration expansion,
- no speculative module growth,
- no saving weak blocks because they feel "important",
- no mixing future ideas with current execution needs.

---

## Final Principle
The future stable architecture is not invented first.

It is revealed after aggressive removal of:
- duplication,
- premature structure,
- parallel control logic,
- and non-critical complexity.

