# FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE AUTHORITY INDEX
Project: FlowMind / Imagine What If
Updated: 2026-09-20
Mode: FAIL-CLOSED AUTHORITY REGISTRY
Scope: authority classification and routing only; no current operational authority

## 1. Purpose

This file records verified authority classification and routing for FlowMind.

Its purpose is to prevent:

- stale authority
- duplicated authority
- filename-based trust
- historical documents silently controlling current work
- legacy documents returning as active guidance
- architecture documents being mistaken for runtime proof
- stale Project Source copies overriding newer repo truth
- overlapping authority roles

This registry does NOT define:

- current mode
- current objective
- current step
- current next action
- current implementation priority
- current allowed work
- current forbidden work
- current operational exit condition

All current operational state belongs exclusively to FLOWMIND_ACTIVE_MAP.md.

This registry does not grant authority merely because a file is listed.

Actual content, freshness, scope, conflicts, and relevant evidence must be verified.

---

## 2. Status model

Every authority candidate is classified as exactly one of:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

TRUSTED:

verified for the explicit scope stated in this registry.

FROZEN LEGACY:

historical or retired material that must not control current work.

UNVERIFIED:

must not control architecture, implementation, or current work until audited.

If evidence is insufficient:

UNVERIFIED.

---

## 3. Authority publication gate

Authority changes must not be committed or pushed while any material risk remains unresolved.

Do not commit or push an authority change if:

- authority documents materially conflict
- a changed authority file has not been content-verified
- required validation fails
- git diff contains unexplained changes
- preflight fails
- an intended classification is unsupported by evidence
- secrets or unrelated changes may be included
- the active authority chain is internally inconsistent
- changed Project Source and repo versions cannot be reconciled

A request to commit does not override a failed safety or consistency gate.

Resolve the blocker first.

Then validate again.

This is a permanent publication rule.

It is not a current operational exit condition.

---

## 4. Authority roles

Authority is role-based.

No filename or document may grant itself permanent authority.

### 4.1 Permanent operating discipline

`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Classification:

TRUSTED

Controls:

- highest-priority permanent FlowMind operating discipline
- anti-drift rules
- authority verification discipline
- source verification discipline
- source synchronization discipline
- fail-closed behavior
- one-step discipline

Does not define current operational state.

Does not prove runtime implementation.

---

### 4.2 Product intent

`FLOWMIND_WORKING_TARGET.md`

Classification:

TRUSTED

Controls:

- high-level product intent
- optimization principles
- minimalism / ROI boundaries
- scope discipline

Does not define detailed target architecture.

Does not define current operational state.

Does not prove runtime implementation.

---

### 4.3 Detailed target architecture

`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`

Classification:

TRUSTED

Controls:

- detailed target architecture
- 12-module destination
- target layers
- target responsibilities
- target artifacts
- deferred scope

Defines where FlowMind is evolving toward architecturally.

Does not define current operational state.

Does not authorize implementation by itself.

Does not prove that target modules are implemented.

---

### 4.4 Current operational authority

`FLOWMIND_ACTIVE_MAP.md`

Classification:

TRUSTED

Controls:

- where current work is
- current mode
- current objective
- current step
- current allowed work
- current forbidden work
- current next operational action
- current operational exit conditions

This is the single current operational authority.

Historical start blocks, anchors, maps, sequences, guards, registries, and architecture documents must not compete with it.

---

### 4.5 Execution discipline

`docs/FLOWMIND_WORK_PROTOCOL_V1.md`

Classification:

TRUSTED

Controls:

- one-step execution
- evidence requirements
- file-edit discipline
- validation discipline
- failure handling
- idempotency
- secrets
- architecture discipline
- Git discipline
- Project Sources synchronization discipline
- response discipline
- stop conditions

Does not define current project state.

---

### 4.6 Map guard

`docs/FLOWMIND_MAP_GUARD_V1.md`

Classification:

TRUSTED

Controls:

- mandatory MAP CHECK
- authority alignment before technical work
- anti-drift stop conditions

Does not define current operational state.

Does not define target architecture.

Does not prove runtime truth.

---

### 4.7 Control-plane semantics

`CANONICAL_DISPATCHER_SPEC.md`

Classification:

TRUSTED

Scope:

control-plane semantics only.

Controls:

- state-transition discipline
- guarded transitions
- HALT / resume behavior
- state mutation rules
- approval / control semantics
- fail-closed dispatcher behavior

Does not define:

- product strategy
- current operational state
- target architecture
- runtime truth

Runtime implementation still requires runtime evidence.

---

### 4.8 Authority index

`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Classification:

TRUSTED

Scope:

authority classification and routing only.

Controls:

- TRUSTED / FROZEN LEGACY / UNVERIFIED classification
- authority-role routing
- publication safety rules
- Project Sources synchronization rules

Does not define current operational state.

This registry cannot turn an unverified implementation into runtime truth.

---

### 4.9 Runtime truth

Runtime truth comes from current repo and runtime evidence.

Relevant evidence may include:

- implementation
- valid inputs
- valid outputs
- validation output
- generated artifacts
- downstream consumption
- runtime logs
- reproducible execution
- failure behavior

Documents are not runtime proof.

---

## 5. TRUSTED authority files

| Path | Verified scope |
|---|---|
| `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md` | Highest-priority permanent operating discipline |
| `FLOWMIND_WORKING_TARGET.md` | High-level product intent |
| `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md` | Detailed target architecture |
| `FLOWMIND_ACTIVE_MAP.md` | Single current operational authority |
| `docs/FLOWMIND_WORK_PROTOCOL_V1.md` | Execution and cooperation discipline |
| `docs/FLOWMIND_MAP_GUARD_V1.md` | MAP CHECK and anti-drift guard |
| `CANONICAL_DISPATCHER_SPEC.md` | Control-plane semantics only |
| `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md` | Authority classification and routing |

A changed authority file remains a candidate version until:

- its contents are verified;
- required validation passes;
- publication gates pass;
- the intended version is committed and pushed;
- corresponding active Project Source content is synchronized when applicable.

---

## 6. FROZEN LEGACY authority-shaped files

| Path | Historical scope |
|---|---|
| `CHAT_START_BLOCK_FLOWMIND_CURRENT.md` | Historical operational checkpoint |
| `FLOWMIND_CURRENT_WORK_ANCHOR.md` | Historical Director Brain preparation checkpoint |
| `FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md` | Historical recovery trust-boundary checkpoint |
| `FLOWMIND_REPO_TRUST_BOUNDARY_V1.md` | Historical repository trust-boundary checkpoint |
| `FLOWMIND_SYSTEM_MAP_V1.md` | Historical recovery system map |
| `FLOWMIND_ACTION_SEQUENCE_V1.md` | Historical recovery execution sequence |
| `FLOWMIND_CANONICAL_STRUCTURE.md` | Historical architecture checkpoint |
| `docs/FLOWMIND_HARD_RULESET_V1.md` | Historical R01-R16 work-discipline checkpoint |
| `MASTER_PROMPTS_v2_FULL.txt` | Historical IronCore / horror prompt artifact; source-only |
| `CHAT_START_BLOCK.txt` | Historical start block; source-only |
| old IronCore v3.5 references | Historical context only |
| old horror rules | Historical or niche-specific material only |
| old migration-era architecture | Historical context only |
| retired runtime contours | Historical or retired runtime structures |

FROZEN LEGACY material:

- may be read
- may be compared
- may provide historical evidence
- may provide donor ideas after review

It must not:

- define current state
- define current next action
- define current architecture
- define current implementation permission
- regain runtime authority
- silently influence active decisions

Promotion from FROZEN LEGACY requires explicit re-audit and verified classification.

---

## 7. UNVERIFIED default

Anything not explicitly classified as TRUSTED or FROZEN LEGACY in this registry is:

UNVERIFIED.

This includes:

- authority-shaped documents not yet classified
- runtime components without sufficient evidence
- stale Project Source copies
- ambiguous repo files
- undocumented control paths
- historical classifications not re-verified

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
- existence in GitHub
- existence in Project Sources
- another document referencing it

Review first.

Then classify.

---

## 8. Runtime classification rule

Historical runtime classifications do not automatically survive into the current registry.

Runtime files and components require scope-specific evidence.

Potential evidence includes:

- code inspection
- input contract
- output contract
- validation
- artifact production
- downstream consumer
- reproducible runtime execution
- failure behavior

No runtime component becomes TRUSTED merely because an older registry, map, recovery document, or architecture document described it as active.

Target architecture is not runtime proof.

---

## 9. Validation tools rule

A validation tool does not become architecture authority merely because it is executed successfully.

`tools/preflight.sh` may be used as a validation helper only after its current contents have been inspected sufficiently to establish that running it is safe and relevant.

A successful preflight proves only the checks that the script actually performs.

It does not automatically:

- make scanned files TRUSTED
- prove runtime behavior outside its checks
- prove target architecture is implemented
- authorize production work

---

## 10. Project Sources synchronization rule

GitHub repository is the durable project master.

Project Sources are ChatGPT working context.

Project Sources do not become source of truth merely because they are uploaded.

An active Project Source must:

1. have verified content;
2. have a defined authority role;
3. have a current classification;
4. not conflict with newer verified repo evidence;
5. match the intended committed repo version when a repo version exists.

A stale Project Source copy is UNVERIFIED as a working copy until synchronized.

When an active authority file changes:

- verify the changed repo content;
- pass required validation;
- commit and push the intended version;
- synchronize the corresponding Project Source;
- verify the Project Source reflects the intended committed authority.

Internal upload suffixes such as:

- `(1)`
- `(2)`
- `(3)`

do not create new logical authority when canonical identity and verified content show they are copies of the same file.

---

## 11. Active Project Source authority set

The intended active authority context consists of:

- `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
- `FLOWMIND_WORKING_TARGET.md`
- `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
- `FLOWMIND_ACTIVE_MAP.md`
- `docs/FLOWMIND_MAP_GUARD_V1.md`
- `docs/FLOWMIND_WORK_PROTOCOL_V1.md`
- `CANONICAL_DISPATCHER_SPEC.md`
- `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Legacy Project Sources must remain outside active decision context.

Historical repository copies may remain where required for evidence.

Removing a legacy Project Source does not require deleting historical Git evidence.

---

## 12. Verified classification record

The verified authority model records:

1. `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
   - TRUSTED
   - highest-priority permanent operating discipline

2. `FLOWMIND_WORKING_TARGET.md`
   - TRUSTED
   - high-level product intent only

3. `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
   - TRUSTED
   - detailed target architecture only

4. `FLOWMIND_ACTIVE_MAP.md`
   - TRUSTED
   - single current operational authority

5. `docs/FLOWMIND_MAP_GUARD_V1.md`
   - TRUSTED
   - MAP CHECK and anti-drift enforcement only

6. `docs/FLOWMIND_WORK_PROTOCOL_V1.md`
   - TRUSTED
   - execution discipline only

7. `CANONICAL_DISPATCHER_SPEC.md`
   - TRUSTED
   - control-plane semantics only

8. `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`
   - TRUSTED
   - authority classification and routing only

9. `CHAT_START_BLOCK_FLOWMIND_CURRENT.md`
   - FROZEN LEGACY

10. `FLOWMIND_CURRENT_WORK_ANCHOR.md`
    - FROZEN LEGACY

11. `FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md`
    - FROZEN LEGACY

12. `FLOWMIND_REPO_TRUST_BOUNDARY_V1.md`
    - FROZEN LEGACY

13. `FLOWMIND_SYSTEM_MAP_V1.md`
    - FROZEN LEGACY

14. `FLOWMIND_ACTION_SEQUENCE_V1.md`
    - FROZEN LEGACY

15. `FLOWMIND_CANONICAL_STRUCTURE.md`
    - FROZEN LEGACY

16. `docs/FLOWMIND_HARD_RULESET_V1.md`
    - FROZEN LEGACY

17. `CHAT_START_BLOCK.txt`
    - FROZEN LEGACY
    - source-only historical artifact

18. `MASTER_PROMPTS_v2_FULL.txt`
    - FROZEN LEGACY
    - source-only historical artifact

This record describes classification.

It does not define current work.

---

## 13. Permanent prohibitions

Do not:

- trust a file because another file calls it TRUSTED
- use FROZEN LEGACY as active guidance
- use UNVERIFIED material to drive implementation
- treat architecture documentation as runtime evidence
- treat validation success as proof beyond validation scope
- treat test artifacts as production permission
- reactivate legacy modules without explicit audit
- allow historical next-action instructions to override FLOWMIND_ACTIVE_MAP.md
- maintain a second operational authority
- commit or push an authority change while material risk remains unresolved
- print or commit secrets
- use `.env` as architecture or product truth
- store current operational state in this registry

---

## 14. Classification change rule

A classification or authority-role change requires:

1. exact file identification;
2. actual content verification;
3. freshness check;
4. conflict check;
5. scope verification;
6. relevant repo / runtime evidence when applicable;
7. explicit TRUSTED / FROZEN LEGACY / UNVERIFIED classification;
8. validation of any changed authority files;
9. publication-gate verification before commit or push;
10. Project Source synchronization when applicable.

Do not silently promote authority.

Do not silently demote authority.

Do not infer classification from a filename.

---

## 15. Relationship to current operational state

This registry must not store a phase-specific:

- current mode
- current objective
- current step
- current next action
- current implementation priority
- current forbidden-work list
- current operational exit condition

Those belong exclusively to:

`FLOWMIND_ACTIVE_MAP.md`

When FlowMind changes phase, this registry does not need modification unless:

- an authority classification changes;
- an authority role changes;
- the active authority set changes;
- a synchronization or trust rule changes.

This prevents routine phase changes from creating duplicate operational authority.

---

## 16. Registry validity rule

This registry remains valid only while:

- classifications are evidence-based;
- roles do not overlap ambiguously;
- FLOWMIND_ACTIVE_MAP.md remains the single current operational authority;
- FROZEN LEGACY remains outside active guidance;
- UNVERIFIED material cannot drive implementation;
- runtime truth remains evidence-based;
- Project Source mismatches fail closed;
- publication gates block unresolved authority risk.

If any of these conditions are violated:

STOP.

Reconcile authority before relying on the registry.

End.