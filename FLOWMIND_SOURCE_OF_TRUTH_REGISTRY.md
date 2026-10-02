# FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE AUTHORITY INDEX
Project: FlowMind / Imagine What If
Governance model: AUTHORITY SYSTEM V2
Updated: 2026-09-30
Scope: authority classification, role-to-file routing and publication-state rules only; no current operational state

## 1. Purpose

This file is the single owner of FlowMind authority classification and role-to-file routing.

It exists to answer:

- which file owns each authority role
- which files are TRUSTED
- which files are FROZEN LEGACY
- which files are UNVERIFIED
- which exact file is CURRENT_TRUSTED_DETAILED_TARGET
- which files belong to the active authority set
- how authority publication and Project Source synchronization are completed

This file does NOT define:

- current mode
- current objective
- current step
- current next action
- current implementation priority
- current allowed work
- current forbidden work
- current operational exit condition
- runtime implementation truth

All current operational state belongs exclusively to:

FLOWMIND_ACTIVE_MAP.md

Runtime truth belongs to:

verified repo and runtime evidence.

---

## 2. Status model

Every authority-shaped file is classified as exactly one of:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

### TRUSTED

Verified and authorized for the explicit scope assigned in this Registry.

### FROZEN LEGACY

Historical, retired, superseded or intentionally deactivated material.

It may be used as evidence.

It must not control current work.

### UNVERIFIED

Not authorized to control current work.

If evidence is insufficient:

UNVERIFIED.

No additional trust label is required.

Publication/migration state is separate from classification.

---

## 3. Canonical authority roles

### 3.1 Permanent operating discipline

Role:
PERMANENT_OPERATING_DISCIPLINE

File:
`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Classification:
TRUSTED

Controls:

- permanent anti-drift rules
- authority reconciliation rules
- source-verification discipline
- authority-migration safety rules
- fail-closed behavior
- permanent one-step governance

Does not define current operational state.

---

### 3.2 Product intent

Role:
PRODUCT_INTENT

File:
`FLOWMIND_WORKING_TARGET.md`

Classification:
TRUSTED

Controls:

- high-level product intent
- optimization principles
- scope discipline
- minimalism / ROI boundaries

Does not define detailed architecture.

Does not define runtime truth.

---

### 3.3 Detailed target architecture

Role:
CURRENT_TRUSTED_DETAILED_TARGET

File:
`FLOWMIND_TARGET_ARCHITECTURE_V3_2.md`

Classification:
TRUSTED

Controls:

- detailed target architecture
- target capability ownership
- architectural boundaries
- target contracts and artifacts
- architecture destination
- migration principles
- deferred architectural scope

This role is the ONLY canonical pointer to the current trusted detailed target.

Permanent governance files must reference:

CURRENT_TRUSTED_DETAILED_TARGET

rather than hard-code an architecture version.

The architecture file does not define current operational state.

The architecture file does not prove runtime implementation.

---

### 3.4 Current operational authority

Role:
CURRENT_OPERATIONAL_AUTHORITY

File:
`FLOWMIND_ACTIVE_MAP.md`

Classification:
TRUSTED

Controls only:

- current mode
- current objective
- current step
- current allowed work
- current forbidden work
- current next action
- current operational exit condition

No other active authority file may independently own those fields.

---

### 3.5 Execution discipline

Role:
EXECUTION_DISCIPLINE

File:
`docs/FLOWMIND_WORK_PROTOCOL_V1.md`

Classification:
TRUSTED

Controls:

- one-step execution
- MAP CHECK procedure
- evidence sufficiency
- anti-loop verification
- full-file replacement discipline
- validation discipline
- Git discipline
- Project Sources synchronization procedure
- response discipline
- authority-reconciliation execution procedure

Does not define current operational state.

Does not define detailed-target identity.

---

### 3.6 Control-plane semantics

Role:
CONTROL_PLANE_SEMANTICS

File:
`CANONICAL_DISPATCHER_SPEC.md`

Classification:
TRUSTED

Controls only:

- dispatcher/control-plane semantic contract
- state-transition discipline
- guarded transitions
- HALT / resume semantics
- state mutation discipline
- approval/control semantics

Does not define:

- product strategy
- current operational state
- detailed-target identity
- runtime proof

---

### 3.7 Authority registry

Role:
AUTHORITY_REGISTRY

File:
`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Classification:
TRUSTED

Controls:

- role-to-file routing
- TRUSTED / FROZEN LEGACY / UNVERIFIED classification
- CURRENT_TRUSTED_DETAILED_TARGET pointer
- active authority set
- authority publication rules
- Project Sources authority synchronization rules

Does not define current operational state.

---

### 3.8 Runtime truth

Role:
RUNTIME_TRUTH

Source:
verified current repo and runtime evidence

Relevant evidence may include:

- current code
- valid input/output
- validation output
- generated artifact
- downstream consumption
- runtime log
- reproducible execution
- failure behavior

Documents are not runtime proof.

---

## 4. Active authority set

The active authority set is:

1. `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
2. `FLOWMIND_WORKING_TARGET.md`
3. `FLOWMIND_TARGET_ARCHITECTURE_V3_2.md`
4. `FLOWMIND_ACTIVE_MAP.md`
5. `docs/FLOWMIND_WORK_PROTOCOL_V1.md`
6. `CANONICAL_DISPATCHER_SPEC.md`
7. `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Only these files hold active authority roles defined by this Registry.

A file not listed here does not gain active authority merely because it exists in repo or Project Sources.

---

## 5. FROZEN LEGACY set

The following files are explicitly FROZEN LEGACY:

- `FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`
- `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
- `docs/FLOWMIND_MAP_GUARD_V1.md`
- `CHAT_START_BLOCK_FLOWMIND_CURRENT.md`
- `FLOWMIND_CURRENT_WORK_ANCHOR.md`
- `FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md`
- `FLOWMIND_REPO_TRUST_BOUNDARY_V1.md`
- `FLOWMIND_SYSTEM_MAP_V1.md`
- `FLOWMIND_ACTION_SEQUENCE_V1.md`
- `FLOWMIND_CANONICAL_STRUCTURE.md`
- `docs/FLOWMIND_HARD_RULESET_V1.md`
- `CHAT_START_BLOCK.txt`
- `MASTER_PROMPTS_v2_FULL.txt`

Also FROZEN LEGACY by category unless explicitly re-audited and reclassified:

- old IronCore authority-shaped material
- old horror-specific authority-shaped material
- old migration-era architecture
- retired runtime contour documents
- historical start blocks and work anchors

FROZEN LEGACY material may:

- be read
- be compared
- provide historical evidence
- provide donor ideas after audit

It must NOT:

- define current state
- define current next action
- define current architecture
- define implementation permission
- regain runtime authority
- override the active authority set
- silently influence current decisions

Promotion from FROZEN LEGACY requires explicit re-audit and Registry reclassification.

---

## 6. UNVERIFIED default

Anything authority-shaped that is not explicitly classified as TRUSTED or FROZEN LEGACY here is:

UNVERIFIED.

Do not infer trust from:

- filename
- directory
- ACTIVE label
- CURRENT label
- FINAL label
- CANONICAL label
- TRUSTED label
- version number
- age
- Git history
- GitHub presence
- Project Sources presence
- another document referencing it

Review first.

Then classify.

---

## 7. Architecture-version rule

Only this Registry may bind:

CURRENT_TRUSTED_DETAILED_TARGET

to a concrete architecture file.

Permanent governance files must not hard-code the current detailed-target architecture version.

When a future architecture replaces the current target:

1. candidate architecture is created and validated
2. authority reconciliation / publication transaction is declared
3. affected authority files are reconciled
4. this Registry updates CURRENT_TRUSTED_DETAILED_TARGET
5. superseded target becomes FROZEN LEGACY
6. final authority validation passes
7. validated authority block is committed and pushed
8. Project Sources are synchronized
9. final authority chain is verified

A future version change should not require architecture-version edits in unrelated permanent governance rules.

---

## 8. Authority reconciliation and expected mismatch

Authority reconciliation is defined by:

`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

and executed under:

`docs/FLOWMIND_WORK_PROTOCOL_V1.md`

During an authorized multi-file authority transaction:

EXPECTED_MIGRATION_MISMATCH

may temporarily exist between:

- already-updated migration files
and
- not-yet-updated migration files

This expected mismatch:

- does not create a second authority
- does not authorize runtime work
- does not invalidate completed file PASS results
- does not require migration restart
- does not require premature Project Source synchronization

An unexpected conflict outside the declared migration set is not protected by this rule.

That is:

UNPLANNED_MATERIAL_CONFLICT

and must be resolved before transaction completion.

---

## 9. Publication gate

Authority publication is evaluated at the validated work-block / transaction level.

Do not commit or push an authority block if:

- a migration-set file failed validation
- an UNPLANNED_MATERIAL_CONFLICT remains
- the active authority set would contain duplicate role owners
- CURRENT_TRUSTED_DETAILED_TARGET is ambiguous
- current operational authority is duplicated
- control-plane authority is duplicated
- git diff contains unexplained changes
- preflight or required validation fails
- secrets or unrelated changes may be included
- intended classifications are unsupported

Do not block publication merely because an EXPECTED_MIGRATION_MISMATCH existed during intermediate sequential edits.

Before commit/push, that expected mismatch must be resolved across the completed migration set.

Publication sequence:

1. complete migration-set file replacements
2. verify each file
3. run one final cross-file authority validation
4. inspect git diff/status
5. run required validation / preflight
6. stage only intended changes
7. commit the validated authority block
8. push
9. synchronize affected active Project Sources
10. verify synchronized contents
11. verify final authority chain

---

## 10. Project Sources rule

GitHub repository is the durable project master.

Project Sources are ChatGPT working context.

An active Project Source must:

- correspond to an active authority role or be clearly non-authoritative context
- match the intended committed repo version when the repo version exists
- not override newer verified repo evidence
- not silently reactivate FROZEN LEGACY material

During an unfinished authorized authority transaction:

repo/Project Source mismatch may temporarily be:

EXPECTED_MIGRATION_MISMATCH

when it is a known consequence of the declared transaction.

Project Sources synchronization occurs:

after the validated authority block is committed and pushed.

Do not synchronize each authority file independently in the middle of the transaction unless a specific recovery reason requires it.

After synchronization:

any unresolved mismatch in an active authority source is a defect.

Internal upload suffixes such as:

- `(1)`
- `(2)`
- `(3)`

do not create a new logical authority when verified content identifies the same canonical file.

---

## 11. Current-state rule

This Registry must not store:

- current mode
- current objective
- current step
- current next action
- current implementation priority
- current allowed work
- current forbidden work
- current operational exit condition

Those belong only to:

FLOWMIND_ACTIVE_MAP.md

This Registry may define stable authority roles and classifications.

It must not become a second Active Map.

---

## 12. Runtime classification rule

Authority classification and runtime/component state are separate systems.

Runtime components may have operational labels such as:

- ACTIVE
- DONOR
- ARCHIVE
- BROKEN
- IDEA
- UNKNOWN

Those labels do not grant document authority.

No runtime component becomes implemented merely because:

- target architecture describes it
- a historical architecture described it
- an authority file references it
- a Project Source contains it
- a test fixture resembles it

Runtime capability requires relevant runtime evidence.

---

## 13. Validation-tools rule

A validation tool proves only what it actually checks.

For example:

`tools/preflight.sh`

may be used only after its relevant behavior is understood sufficiently for the current purpose.

A passing validation does not automatically:

- make every scanned file TRUSTED
- prove end-to-end runtime behavior
- prove business outcomes
- validate unknown providers
- authorize unrelated implementation

Use validation evidence within its actual scope.

---

## 14. Classification-change rule

A classification or authority-role change requires enough evidence to establish:

1. exact file identity
2. actual current content
3. intended role
4. material conflicts
5. intended classification
6. required validation
7. publication state
8. Project Source synchronization state where applicable

Do not silently promote authority.

Do not silently demote authority.

Do not infer classification from filename.

Do not repeat already-completed verification without a material reason.

---

## 15. Registry validity

This Registry is valid only while:

- each active authority role has one owner
- CURRENT_TRUSTED_DETAILED_TARGET resolves to one file
- FLOWMIND_ACTIVE_MAP.md remains the single current operational authority
- FROZEN LEGACY remains outside active guidance
- UNVERIFIED material cannot drive implementation
- runtime truth remains evidence-based
- permanent governance files do not hard-code detailed-target versions
- authority reconciliation distinguishes EXPECTED_MIGRATION_MISMATCH from UNPLANNED_MATERIAL_CONFLICT
- Project Source mismatches are resolved at publication completion
- one control-plane authority remains active

If those conditions are violated:

STOP normal implementation.

Use authority reconciliation when the conflict is inside authority itself.

---

## 16. Current canonical authority model

Permanent operating discipline:
`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Product intent:
`FLOWMIND_WORKING_TARGET.md`

Detailed-target identity:
`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`
role:
CURRENT_TRUSTED_DETAILED_TARGET

Current trusted detailed target:
`FLOWMIND_TARGET_ARCHITECTURE_V3_2.md`

Current operational authority:
`FLOWMIND_ACTIVE_MAP.md`

Execution discipline:
`docs/FLOWMIND_WORK_PROTOCOL_V1.md`

Control-plane semantics:
`CANONICAL_DISPATCHER_SPEC.md`

Authority classification:
`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Runtime truth:
verified repo and runtime evidence

Historical V3.1 target:
`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`
-> FROZEN LEGACY

Historical V2.1 target:
`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
-> FROZEN LEGACY

Historical Map Guard:
`docs/FLOWMIND_MAP_GUARD_V1.md`
-> FROZEN LEGACY

End.
