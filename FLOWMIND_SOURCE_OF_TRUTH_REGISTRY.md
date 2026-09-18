# FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE AUTHORITY INDEX

Project: FlowMind / Imagine What If

Updated: 2026-09-18

Mode: FAIL-CLOSED AUTHORITY REGISTRY

## 1. Purpose

This file records the verified authority classification for FlowMind.

Its purpose is to prevent:

- stale authority
- duplicated authority
- filename-based trust
- recovery-era documents silently controlling current work
- legacy documents returning as active guidance
- architecture documents being mistaken for runtime proof
- stale Project Source copies overriding newer repo truth

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

## 3. Audit publication gate

The authority-audit block must not be committed or pushed while any material risk remains unresolved.

Do not commit or push if:

- authority documents materially conflict
- a changed authority file has not been content-verified
- required validation fails
- git diff contains unexplained changes
- preflight fails
- an intended classification is unsupported by evidence
- secrets or unrelated changes may be included
- the active authority chain is internally inconsistent

A request to commit does not override a failed safety or consistency gate.

Resolve the blocker first.

Then validate again.

---

## 4. Authority roles

Authority is role-based.

No filename or document may grant itself permanent authority.

### 4.1 Operating discipline

`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Classification:

TRUSTED

Controls:

- highest-priority FlowMind operating discipline
- anti-drift rules
- authority verification
- source synchronization rules
- current audit constraints

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

Defines where FlowMind is evolving toward.

Does not prove that target modules are implemented.

---

### 4.4 Current operational state

`FLOWMIND_ACTIVE_MAP.md`

Classification:

TRUSTED

Controls:

- where current work is
- current objective
- current allowed work
- current forbidden work
- current next operational step
- audit exit conditions

This is the single current operational authority.

Historical start blocks, anchors, maps, and action sequences must not compete with it.

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
- Project Sources synchronization
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

Does not define target architecture or runtime truth.

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
- approval/control semantics
- fail-closed dispatcher behavior

Does not prove that every referenced dispatcher implementation exists or works.

Runtime implementation still requires runtime evidence.

---

### 4.8 Authority index

`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

Classification:

TRUSTED

Scope:

authority classification and routing only.

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
| `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md` | Highest-priority operating discipline and anti-drift |
| `FLOWMIND_WORKING_TARGET.md` | High-level product intent |
| `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md` | Detailed target architecture |
| `FLOWMIND_ACTIVE_MAP.md` | Single current operational authority |
| `docs/FLOWMIND_WORK_PROTOCOL_V1.md` | Execution and cooperation discipline |
| `docs/FLOWMIND_MAP_GUARD_V1.md` | Mandatory map-alignment guard |
| `CANONICAL_DISPATCHER_SPEC.md` | Control-plane semantics only |
| `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md` | Authority classification and routing |

These classifications apply to the versions contained in the validated authority-audit commit.

Before that commit exists, the modified working tree remains a candidate state and must pass all publication gates.

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
| retired runtime contours | Must not become active without explicit re-audit |

FROZEN LEGACY material:

- may be read
- may be compared
- may provide historical evidence
- may provide donor ideas after review

It must not:

- define current state
- define current next action
- define current architecture
- regain runtime authority
- silently influence active decisions

---

## 7. UNVERIFIED default

Anything not explicitly classified as TRUSTED or FROZEN LEGACY in this registry is:

UNVERIFIED.

This includes authority-shaped documents and runtime components that have not passed the current verification gate.

Do not infer trust from:

- filename
- directory
- ACTIVE label
- CURRENT label
- FINAL label
- CANONICAL label
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

No runtime component becomes TRUSTED merely because an older registry, map, or recovery document described it as active.

---

## 9. Validation tools rule

A validation tool does not become architecture authority merely because it is executed successfully.

`tools/preflight.sh` may be used as an audit validation helper only after its current contents are inspected sufficiently to establish that running it is safe and relevant.

A successful preflight proves only the checks that the script actually performs.

It does not automatically make scanned files TRUSTED.

---

## 10. Project Sources rule

GitHub repository is the durable project master.

Project Sources are ChatGPT working context.

Project Sources do not become source of truth merely because they are uploaded.

An active Project Source must:

1. have verified content
2. have a defined authority role
3. have a current classification
4. not conflict with newer repo evidence
5. match the intended committed repo version when a repo version exists

A stale Project Source copy is UNVERIFIED as a working copy until synchronized.

Internal upload suffixes such as:

- `(1)`
- `(2)`
- `(3)`

do not create new logical authority when canonical identity and verified content show they are copies of the same file.

---

## 11. Project Sources reconciliation

### KEEP / SYNCHRONIZE

The following active authority sources should remain available after synchronization:

- `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
- `FLOWMIND_WORKING_TARGET.md`
- `FLOWMIND_ACTIVE_MAP.md`
- `docs/FLOWMIND_MAP_GUARD_V1.md`
- `docs/FLOWMIND_WORK_PROTOCOL_V1.md`
- `CANONICAL_DISPATCHER_SPEC.md`
- `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

### ADD AFTER COMMIT

Add the verified detailed target architecture:

- `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`

### REMOVE FROM ACTIVE PROJECT SOURCES

Remove legacy sources that must not influence active decisions:

- `CHAT_START_BLOCK.txt`
- `CHAT_START_BLOCK_FLOWMIND_CURRENT.md`
- `MASTER_PROMPTS_v2_FULL.txt`

Repository historical copies may remain where applicable.

Removing an active Project Source does not require deleting historical Git evidence.

---

## 12. Completed authority-audit findings

The current audit established:

1. `000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`
   - TRUSTED
   - highest-priority operating discipline

2. `FLOWMIND_WORKING_TARGET.md`
   - TRUSTED
   - high-level product intent only

3. `FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`
   - TRUSTED
   - detailed target architecture only

4. `FLOWMIND_ACTIVE_MAP.md`
   - previous version was stale
   - replacement establishes one current operational authority

5. `docs/FLOWMIND_MAP_GUARD_V1.md`
   - previous version depended on stale recovery authority
   - replacement aligns map checks with the current authority chain

6. `docs/FLOWMIND_WORK_PROTOCOL_V1.md`
   - replacement consolidates active execution discipline
   - preserves required historical HARD_RULESET principles without keeping parallel policy authority

7. `CANONICAL_DISPATCHER_SPEC.md`
   - replacement limits its authority to control-plane semantics
   - no longer acts as product brain or runtime proof

8. `CHAT_START_BLOCK_FLOWMIND_CURRENT.md`
   - FROZEN LEGACY

9. `FLOWMIND_CURRENT_WORK_ANCHOR.md`
   - FROZEN LEGACY

10. `FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md`
    - FROZEN LEGACY

11. `FLOWMIND_REPO_TRUST_BOUNDARY_V1.md`
    - FROZEN LEGACY

12. `FLOWMIND_SYSTEM_MAP_V1.md`
    - FROZEN LEGACY

13. `FLOWMIND_ACTION_SEQUENCE_V1.md`
    - FROZEN LEGACY

14. `FLOWMIND_CANONICAL_STRUCTURE.md`
    - FROZEN LEGACY

15. `docs/FLOWMIND_HARD_RULESET_V1.md`
    - FROZEN LEGACY
    - useful principles migrated into current operating documents

16. `CHAT_START_BLOCK.txt`
    - FROZEN LEGACY
    - Project Source only; absent from current repo

17. `MASTER_PROMPTS_v2_FULL.txt`
    - FROZEN LEGACY
    - Project Source only; absent from current repo

---

## 13. Prohibitions

Do not:

- trust a file because another file calls it TRUSTED
- use FROZEN LEGACY as active guidance
- use UNVERIFIED material to drive implementation
- treat architecture documentation as runtime evidence
- treat validation success as proof beyond the validation scope
- treat test artifacts as production permission
- reactivate legacy modules without explicit audit
- allow historical current-next-action instructions to override `FLOWMIND_ACTIVE_MAP.md`
- maintain a second operational authority
- commit or push an authority block while material risk remains unresolved
- print or commit secrets
- use `.env` as architecture or product truth

---

## 14. Current objective

Current mode:

SYSTEM MAP MODE

Current objective:

Complete authority and Project Sources reconciliation before production development resumes.

Production implementation remains paused.

No Director Brain implementation, renderer tuning, provider expansion, Telegram integration, YouTube upload, TikTok crossposting, or legacy runtime activation is authorized by this audit.

---

## 15. Exit condition

The authority/source audit is complete only when:

1. every active Project Source has a current classification
2. active authority roles no longer overlap ambiguously
3. `FLOWMIND_ACTIVE_MAP.md` is the single current operational authority
4. legacy operational documents are frozen
5. control specifications are audited
6. changed authority files pass validation
7. the validation helper used for preflight is safe to run
8. preflight passes
9. git diff contains only intended changes
10. no unresolved commit risk remains
11. the authority block is committed
12. the commit is pushed
13. active Project Sources are synchronized with committed authority
14. stale legacy Project Sources are removed from active context

If any condition fails:

STOP.

Do not declare the audit complete.

---

## 16. One-step rule

Audit work proceeds:

one step

→ evidence

→ verification

→ next step

Do not jump ahead.

Do not commit after every individual file.

Commit only after one coherent validated authority-audit block.

End.
