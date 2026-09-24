# FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE AUTHORITY INDEX
Project: FlowMind / Imagine What If
Updated: 2026-09-24
Mode: FAIL-CLOSED AUTHORITY REGISTRY
Scope: authority classification and routing only; no current operational authority

Publication transition note:

This working-copy update defines the intended authority state after V3.1 promotion.

It does not become published authority merely because this file is edited locally.

Until:

- validation passes
- publication gates pass
- intended authority files are committed and pushed
- required Project Sources are synchronized
- final authority-chain verification passes

the previously published authority state remains effective.

---

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
- incomplete architecture migrations creating split authority

This registry does NOT define:

- current mode
- current objective
- current step
- current next action
- current implementation priority
- current allowed work
- current forbidden work
- current operational exit condition

All current operational state belongs exclusively to:

`FLOWMIND_ACTIVE_MAP.md`

This registry does not grant authority merely because a file is listed.

Actual content, freshness, scope, conflicts, and relevant evidence must be verified.

---

## 2. Status Model

Every authority candidate is classified as exactly one of:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

### TRUSTED

Verified for the explicit scope stated in this registry.

### FROZEN LEGACY

Historical, retired, or superseded material that must not control current work.

### UNVERIFIED

Must not control architecture, implementation, or current work until audited.

If evidence is insufficient:

UNVERIFIED.

---

## 3. Authority Publication Gate

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
- a superseded authority is still referenced as active by another trusted authority file

A request to commit does not override a failed safety or consistency gate.

Resolve the blocker first.

Then validate again.

A changed authority file remains a candidate working copy until:

1. exact contents are verified
2. required validation passes
3. publication gates pass
4. intended version is committed
5. intended version is pushed
6. corresponding active Project Source is synchronized when applicable
7. final authority chain is verified

---

# 4. Authority Roles

Authority is role-based.

No filename or document may grant itself permanent authority.

---

## 4.1 Permanent Operating Discipline

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

Does not define detailed target architecture.

Does not prove runtime implementation.

---

## 4.2 Product Intent

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

## 4.3 Detailed Target Architecture

`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`

Classification:

TRUSTED after publication gate completion.

Until publication gate completion, the local edited version is a candidate working copy and the last published trusted target remains effective.

Controls:

- detailed V3.1 target architecture
- seven logical system blocks
- target capability ownership
- Control Plane boundary
- Opportunity Intelligence
- Editorial Brain
- Production Brain
- Render / Quality / Compliance
- Delivery / Learning
- Capability Evolution
- persistent state and learning memory
- provider abstraction
- Capability Registry
- Human Decision Gateway
- cloud-first target
- cost and latency governance
- rights/compliance target
- target migration principles
- deferred architectural scope

Defines where FlowMind is evolving toward architecturally.

Does NOT define:

- current operational state
- current implementation sequence
- current implementation permission
- runtime truth

Does not prove that any V3.1 capability is implemented.

Architecture destination does not override runtime evidence.

---

## 4.4 Current Operational Authority

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

Historical maps, start blocks, sequences, architecture files, registries, and work anchors must not compete with it.

Target architecture defines destination.

Active Map defines where work happens now.

Runtime evidence defines what actually exists.

---

## 4.5 Execution Discipline

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

Does not define target architecture.

---

## 4.6 Map Guard

`docs/FLOWMIND_MAP_GUARD_V1.md`

Classification:

TRUSTED

Controls:

- mandatory MAP CHECK
- authority alignment before technical work
- anti-drift stop conditions

Does not define:

- current operational state
- detailed target architecture
- runtime truth

---

## 4.7 Control-Plane Semantics

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
- approval/control semantics
- fail-closed dispatcher behavior

Does not define:

- product strategy
- current operational state
- detailed target architecture
- runtime truth

The V3.1 Control Plane must evolve from verified control-plane semantics.

V3.1 does not authorize a second dispatcher or second execution authority.

---

## 4.8 Authority Index

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

Does not prove runtime implementation.

---

## 4.9 Runtime Truth

Runtime truth comes from verified current repo and runtime evidence.

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

Architecture is not runtime proof.

A V3.1 capability is not considered operational merely because it appears in the target architecture.

---

# 5. TRUSTED Authority Files

After successful V3.1 publication, the intended TRUSTED authority set is:

| Path | Verified scope |
|---|---|
| `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md` | Highest-priority permanent operating discipline |
| `FLOWMIND_WORKING_TARGET.md` | High-level product intent |
| `FLOWMIND_TARGET_ARCHITECTURE_V3_1.md` | Detailed target architecture |
| `FLOWMIND_ACTIVE_MAP.md` | Single current operational authority |
| `docs/FLOWMIND_WORK_PROTOCOL_V1.md` | Execution and cooperation discipline |
| `docs/FLOWMIND_MAP_GUARD_V1.md` | MAP CHECK and anti-drift guard |
| `CANONICAL_DISPATCHER_SPEC.md` | Control-plane semantics only |
| `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md` | Authority classification and routing |

A changed authority file remains a candidate working copy until publication gates complete.

---

# 6. FROZEN LEGACY Authority-Shaped Files

| Path | Historical scope |
|---|---|
| `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md` | Superseded V2.1 detailed target architecture |
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

`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md` is retained for architecture history and migration evidence.

It must not control new target decisions after V3.1 publication.

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

Promotion from FROZEN LEGACY requires explicit re-audit and verified reclassification.

---

# 7. UNVERIFIED Default

Anything not explicitly classified as TRUSTED or FROZEN LEGACY in this registry is:

UNVERIFIED.

This includes:

- authority-shaped documents not yet classified
- runtime components without sufficient evidence
- stale Project Source copies
- ambiguous repo files
- undocumented control paths
- historical classifications not re-verified
- architecture candidates before publication completion

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

# 8. Runtime Classification Rule

Historical runtime classifications do not automatically survive into the current registry.

Runtime components require scope-specific evidence.

Potential evidence includes:

- code inspection
- input contract
- output contract
- validation
- artifact production
- downstream consumer
- reproducible runtime execution
- failure behavior

No runtime component becomes trusted implementation merely because:

- V2.1 described it
- V3.1 describes it
- an older registry described it
- a Project Source contains it
- a test fixture produced something similarly named

Target architecture is not runtime proof.

---

# 9. Validation Tools Rule

A validation tool does not become architecture authority merely because it executes successfully.

`tools/preflight.sh` may be used as a validation helper only after its contents have been inspected sufficiently to establish that running it is safe and relevant.

A successful preflight proves only the checks that the script actually performs.

It does not automatically:

- make scanned files TRUSTED
- prove runtime behavior outside its checks
- prove V3.1 is implemented
- authorize production work
- validate unknown external providers
- validate business outcomes

---

# 10. Project Sources Synchronization Rule

GitHub repository is the durable project master.

Project Sources are ChatGPT working context.

Project Sources do not become source of truth merely because they are uploaded.

An active Project Source must:

1. have verified content
2. have a defined authority role
3. have a current classification
4. not conflict with newer verified repo evidence
5. match the intended committed repo version when a repo version exists

A stale Project Source copy is UNVERIFIED as a working copy until synchronized.

When an active authority file changes:

1. verify changed repo content
2. pass required validation
3. commit intended version
4. push intended version
5. synchronize corresponding Project Source
6. verify Project Source reflects the intended committed authority

For the V3.1 transition:

- the old V2.1 Project Source must not remain the active detailed target source after V3.1 publication
- the V3.1 Project Source must match the committed V3.1 repo file
- Project Source synchronization occurs after commit/push, not before

Internal upload suffixes such as:

- `(1)`
- `(2)`
- `(3)`

do not create new logical authority when canonical identity and verified content show they are copies of the same file.

---

# 11. Active Project Source Authority Set

After successful V3.1 publication and synchronization, the intended active authority context is:

- `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
- `FLOWMIND_WORKING_TARGET.md`
- `FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`
- `FLOWMIND_ACTIVE_MAP.md`
- `docs/FLOWMIND_MAP_GUARD_V1.md`
- `docs/FLOWMIND_WORK_PROTOCOL_V1.md`
- `CANONICAL_DISPATCHER_SPEC.md`
- `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md` becomes FROZEN LEGACY and must remain outside active target decision context.

Legacy Project Sources must remain outside active decision context.

Historical repository copies may remain where required for evidence.

Removing a legacy Project Source does not require deleting historical Git evidence.

---

# 12. Verified Classification Record

After successful V3.1 publication:

1. `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
   - TRUSTED
   - highest-priority permanent operating discipline

2. `FLOWMIND_WORKING_TARGET.md`
   - TRUSTED
   - high-level product intent only

3. `FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`
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

9. `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
   - FROZEN LEGACY
   - superseded detailed target architecture

10. `CHAT_START_BLOCK_FLOWMIND_CURRENT.md`
    - FROZEN LEGACY

11. `FLOWMIND_CURRENT_WORK_ANCHOR.md`
    - FROZEN LEGACY

12. `FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md`
    - FROZEN LEGACY

13. `FLOWMIND_REPO_TRUST_BOUNDARY_V1.md`
    - FROZEN LEGACY

14. `FLOWMIND_SYSTEM_MAP_V1.md`
    - FROZEN LEGACY

15. `FLOWMIND_ACTION_SEQUENCE_V1.md`
    - FROZEN LEGACY

16. `FLOWMIND_CANONICAL_STRUCTURE.md`
    - FROZEN LEGACY

17. `docs/FLOWMIND_HARD_RULESET_V1.md`
    - FROZEN LEGACY

18. `CHAT_START_BLOCK.txt`
    - FROZEN LEGACY
    - source-only historical artifact

19. `MASTER_PROMPTS_v2_FULL.txt`
    - FROZEN LEGACY
    - source-only historical artifact

This record describes classification.

It does not define current work.

---

# 13. V2.1 -> V3.1 Authority Transition

The V3.1 transition is a target-architecture authority replacement.

It is NOT:

- a runtime rewrite
- an automatic migration of code
- permission to create a second contour
- permission to reactivate legacy code
- permission to rewrite the dispatcher
- proof that V3.1 capabilities exist

Transition intent:

`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`

changes from:

TRUSTED detailed target architecture

to:

FROZEN LEGACY historical architecture.

`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`

changes from:

UNVERIFIED candidate working copy

to:

TRUSTED detailed target architecture

only when publication gates complete.

If publication fails:

STOP.

The last verified published authority remains effective.

---

# 14. Permanent Prohibitions

Do not:

- trust a file because another file calls it TRUSTED
- use FROZEN LEGACY as active guidance
- use UNVERIFIED material to drive implementation
- treat architecture documentation as runtime evidence
- treat validation success as proof beyond validation scope
- treat test artifacts as production permission
- reactivate legacy modules without explicit audit
- allow historical next-action instructions to override `FLOWMIND_ACTIVE_MAP.md`
- maintain a second operational authority
- maintain a second production dispatcher
- commit or push an authority change while material risk remains unresolved
- print or commit secrets
- use `.env` as architecture or product truth
- store current operational state in this registry
- silently switch target architecture
- silently promote a provider/model into production
- let a stale Project Source override committed repo authority

---

# 15. Classification Change Rule

A classification or authority-role change requires:

1. exact file identification
2. actual content verification
3. freshness check
4. conflict check
5. scope verification
6. relevant repo/runtime evidence when applicable
7. explicit TRUSTED / FROZEN LEGACY / UNVERIFIED classification
8. validation of changed authority files
9. publication-gate verification before commit or push
10. Project Source synchronization when applicable
11. final authority-chain verification

Do not silently promote authority.

Do not silently demote authority.

Do not infer classification from a filename.

---

# 16. Relationship to Current Operational State

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

- an authority classification changes
- an authority role changes
- the active authority set changes
- a synchronization/trust rule changes

The V2.1 -> V3.1 target transition qualifies because:

- detailed target authority changes
- active authority set changes
- active Project Source set changes

---

# 17. Registry Validity Rule

This registry remains valid only while:

- classifications are evidence-based
- roles do not overlap ambiguously
- `FLOWMIND_ACTIVE_MAP.md` remains the single current operational authority
- FROZEN LEGACY remains outside active guidance
- UNVERIFIED material cannot drive implementation
- runtime truth remains evidence-based
- Project Source mismatches fail closed
- publication gates block unresolved authority risk
- one detailed target architecture is active
- one control-plane authority is active
- V3.1 architecture does not become runtime truth merely through documentation

If any of these conditions are violated:

STOP.

Reconcile authority before relying on the registry.

---

# 18. Final Authority Model After V3.1 Promotion

Permanent discipline:

`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Product intent:

`FLOWMIND_WORKING_TARGET.md`

Detailed target architecture:

`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`

Current operational authority:

`FLOWMIND_ACTIVE_MAP.md`

Execution discipline:

`docs/FLOWMIND_WORK_PROTOCOL_V1.md`

MAP CHECK / anti-drift:

`docs/FLOWMIND_MAP_GUARD_V1.md`

Control-plane semantics:

`CANONICAL_DISPATCHER_SPEC.md`

Authority classification:

`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Runtime truth:

verified repo and runtime evidence

Historical V2.1 target:

`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
-> FROZEN LEGACY

End.