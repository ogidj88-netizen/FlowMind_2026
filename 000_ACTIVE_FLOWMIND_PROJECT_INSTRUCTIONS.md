# 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS

Status: HIGHEST PRIORITY ACTIVE PROJECT SOURCE
Project: FlowMind / Imagine What If
Governance model: AUTHORITY SYSTEM V2
Updated: 2026-09-30
Scope: permanent operating discipline, authority-recovery rules and anti-drift rules; no current operational state

## 1. Purpose

This file defines the highest-priority permanent operating rules for ChatGPT work on FlowMind.

Its purpose is to prevent:

- context drift
- architecture drift
- stale-document authority
- legacy reactivation
- filename-based trust
- duplicated operational authority
- duplicated authority routing
- authority migration deadlocks
- endless verification loops
- target architecture being confused with runtime proof
- historical work instructions being confused with current authorization
- permanent rules being coupled to a specific architecture version

If another Project Source conflicts with these permanent operating rules, this file wins within this scope.

This file does NOT define:

- current project state
- current mode
- current objective
- current next action
- current implementation sequence
- current allowed production work
- the current detailed-target filename or version

Current operational state belongs exclusively to FLOWMIND_ACTIVE_MAP.md.

---

## 2. Authority model

FlowMind authority is role-based.

A file receives authority from:

1. verified content
2. verified scope
3. current classification
4. authority role
5. applicable publication state

A filename, version number, directory, upload name, status label, Git presence or Project Source presence does not grant authority by itself.

### 2.1 Permanent operating discipline

Owner:

000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

Controls:

- permanent anti-drift rules
- authority discipline
- recovery from authority inconsistency
- source verification discipline
- synchronization discipline
- fail-closed behavior
- one-step work discipline
- authority-migration safety rules

Does not control current operational state.

### 2.2 Current operational authority

Owner:

FLOWMIND_ACTIVE_MAP.md

Controls only:

- where work is now
- current mode
- current objective
- current step
- current allowed work
- current forbidden work
- current next operational action
- current operational exit condition

No other active authority file may independently own those fields.

### 2.3 Product intent

Owner:

FLOWMIND_WORKING_TARGET.md

Controls:

- high-level product intent
- optimization principles
- scope discipline
- minimalism / ROI boundaries

It is not detailed target architecture.

It is not runtime proof.

### 2.4 Detailed target architecture

The exact current detailed-target file is NOT hard-coded in permanent operating rules.

The role:

CURRENT_TRUSTED_DETAILED_TARGET

is resolved only through:

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

The resolved detailed target controls:

- detailed target architecture
- target capability ownership
- architectural boundaries
- target artifacts and contracts
- architecture destination
- migration principles
- deferred architectural scope

It does not define current operational state.

It does not prove runtime implementation.

It does not authorize implementation by itself.

### 2.5 Authority classification and role routing

Owner:

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Controls:

- TRUSTED / FROZEN LEGACY / UNVERIFIED classification
- role-to-file routing
- CURRENT_TRUSTED_DETAILED_TARGET identity
- candidate authority identity where applicable
- publication state
- Project Sources reconciliation rules

The Registry does not define current operational state.

### 2.6 Work discipline

Owner:

docs/FLOWMIND_WORK_PROTOCOL_V1.md

Controls:

- execution discipline
- evidence sufficiency
- file-edit discipline
- validation discipline
- Git discipline
- response discipline
- anti-loop execution behavior

It must not redefine authority role pointers owned by the Registry.

### 2.7 Control-plane semantics

Owner:

CANONICAL_DISPATCHER_SPEC.md

Controls verified control-plane semantics only.

It is not:

- product strategy
- current operational authority
- detailed target architecture
- runtime proof

It must not hard-code a particular detailed-target architecture version.

### 2.8 Runtime truth

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

Documents do not substitute for runtime evidence.

---

## 3. Single-owner rule

Each kind of project truth must have one owner.

Permanent rules:
000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

Current operational state:
FLOWMIND_ACTIVE_MAP.md

Product intent:
FLOWMIND_WORKING_TARGET.md

Detailed-target identity and authority classification:
FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Detailed architecture content:
the file resolved by CURRENT_TRUSTED_DETAILED_TARGET

Execution discipline:
docs/FLOWMIND_WORK_PROTOCOL_V1.md

Control-plane semantics:
CANONICAL_DISPATCHER_SPEC.md

Runtime truth:
verified repo and runtime evidence

Other documents may reference these roles.

They must not create competing ownership.

---

## 4. Product alignment rule

Before a technical or architectural recommendation, ChatGPT must verify alignment with:

- FLOWMIND_WORKING_TARGET.md
- CURRENT_TRUSTED_DETAILED_TARGET as resolved by the Registry
- FLOWMIND_ACTIVE_MAP.md
- relevant current repo / runtime evidence

FLOWMIND_WORKING_TARGET.md answers:

what kind of system we are building and why.

CURRENT_TRUSTED_DETAILED_TARGET answers:

what detailed structure and capability ownership FlowMind is evolving toward.

FLOWMIND_ACTIVE_MAP.md answers:

what work is authorized now.

Repo and runtime evidence answer:

what actually exists and works.

Normal implementation must STOP on unresolved material conflict.

Authority reconciliation follows the dedicated procedure in this file instead of deadlocking.

---

## 5. File-content verification gate

Before ChatGPT recommends that a file is:

- added to active Project Sources
- treated as TRUSTED
- used as architecture authority
- used as runtime authority
- used to modify another authority document
- promoted from legacy or unverified status
- used as the basis for implementation

ChatGPT must verify the actual contents of that exact file.

Filename, path, age, declared status, reputation or another document's reference is insufficient evidence.

For a candidate authority file, verify only what is necessary to decide the current question:

1. exact file identity
2. actual current contents
3. declared status and scope
4. freshness relevant to the current decision
5. authority role
6. material conflicts
7. applicable repo/runtime evidence
8. intended classification

Do not repeat already-conclusive verification merely to increase confidence.

If evidence is insufficient after one targeted follow-up:

UNVERIFIED.

Then STOP that decision path.

---

## 6. Conflict taxonomy

Not every mismatch means the same thing.

FlowMind distinguishes:

### 6.1 EXPECTED_MIGRATION_MISMATCH

A temporary mismatch is EXPECTED_MIGRATION_MISMATCH only when:

- an authority migration or repair has been explicitly authorized by Evgen
- the affected files are inside the declared migration set
- the mismatch is a direct consequence of sequential one-file-at-a-time replacement
- the intended end state is already explicit
- runtime implementation remains frozen
- no unrelated authority is being changed

EXPECTED_MIGRATION_MISMATCH does NOT force the migration to restart.

It does NOT authorize runtime work.

It remains tracked until final authority-chain validation.

### 6.2 UNPLANNED_MATERIAL_CONFLICT

A conflict is UNPLANNED_MATERIAL_CONFLICT when:

- it is outside the declared migration set
- it changes the intended end state
- it introduces a second authority
- it changes product scope unexpectedly
- evidence contradicts the assumed migration basis
- validation fails materially
- repo/runtime evidence contradicts the proposed authority claim

UNPLANNED_MATERIAL_CONFLICT:

STOP.

Resolve before continuing.

### 6.3 Runtime conflict

If documentation and verified runtime evidence conflict about what is implemented:

runtime evidence wins for runtime truth.

Do not rewrite runtime merely to make documentation appear correct.

---

## 7. Authority Reconciliation Procedure

This section exists specifically to prevent authority deadlock.

If verified active authority files are materially inconsistent, stale, or mutually blocking:

normal implementation work STOPS.

However, authority reconciliation itself is allowed.

Authority reconciliation is a recovery procedure.

It is NOT a second operational authority and NOT a runtime mode.

Its sole purpose is to restore one coherent authority chain.

### 7.1 Bootstrap condition

Authority reconciliation may begin when:

- a material authority inconsistency is verified
- Evgen explicitly authorizes repair/reconciliation
- the intended end state is clear enough to state
- the repair does not require runtime implementation

A stale or conflicting Active Map must not make authority repair impossible.

When the Active Map itself is part of the verified inconsistency, this permanent recovery rule authorizes only the minimum authority-repair work needed to restore a coherent chain.

It does not authorize product implementation.

### 7.2 Required transaction declaration

Before the first authority edit, ChatGPT must state:

- transaction purpose
- intended end state
- migration set
- files outside scope
- runtime freeze
- exit condition

The declaration may be in chat during bootstrap.

As soon as the appropriate canonical authority file is updated, durable current-state ownership returns to the normal authority chain.

### 7.3 Migration-set rule

A migration set is a bounded list of authority files that must become mutually consistent.

Files are still handled:

ONE FILE AT A TIME.

The migration set does not permit batch editing by default.

It only prevents expected intermediate mismatches from being misclassified as new blockers.

### 7.4 During transaction

Allowed:

- inspect affected authority files
- fully replace one affected authority file at a time
- validate the current file
- continue to the next declared file after verification
- run final cross-file authority validation
- perform publication Git operations after validation
- synchronize Project Sources after commit/push

Forbidden:

- runtime implementation
- new architecture design unrelated to reconciliation
- provider changes
- feature work
- unrelated cleanup
- changing files outside the migration set without explicit re-scope
- treating the candidate target as runtime proof

### 7.5 No restart rule

Once a migration fact is conclusively verified:

carry it forward.

Do not restart the migration from the first file merely because:

- a later file still contains the old pointer
- a new chat is opened
- Project Source filenames contain suffixes
- one expected migration mismatch remains
- the candidate file still carries a pre-promotion status pending final publication

Repeat a completed check only when:

- that file changed
- the check failed
- new evidence materially changes the result
- a specific conflict directly requires re-evaluation

### 7.6 Transaction exit

Authority reconciliation completes only when:

1. every file in the migration set has the intended content
2. material stale active references are removed
3. one current detailed-target authority remains
4. one current operational authority remains
5. one control-plane authority remains
6. final authority validation passes
7. git diff contains only intended changes
8. required validation/preflight passes
9. intended authority changes are committed
10. intended authority changes are pushed
11. required Project Sources are synchronized
12. final authority-chain verification passes

After that:

normal operational work resumes from FLOWMIND_ACTIVE_MAP.md.

---

## 8. No filename trust

Do not assume:

- ACTIVE means active
- CURRENT means current
- CANONICAL means canonical
- TRUSTED means trusted
- FINAL means authoritative
- a higher version number means authoritative
- GitHub presence means trusted
- Project Sources presence means trusted
- another document's reference grants trust

Content, verified scope, current classification and evidence determine authority.

Names do not.

---

## 9. Current-state ownership rule

Current operational state must exist in one place only:

FLOWMIND_ACTIVE_MAP.md

No other active authority file may independently define:

- current mode
- current objective
- current next action
- current implementation priority
- current allowed production work
- current forbidden production work
- current operational exit condition

Exception:

the Authority Reconciliation Procedure may temporarily authorize authority-repair actions only when the Active Map is itself part of the verified inconsistency.

That exception ends immediately when the coherent authority chain is restored.

---

## 10. Project Sources rule

Project Sources are working context for ChatGPT.

They are not automatically source of truth.

A file may influence active decisions only after its relevant content and authority role are verified.

Legacy / FROZEN LEGACY files may remain available for evidence.

They must not control current decisions.

Secrets, credentials, `.env`, API keys or equivalent secret configuration must never be uploaded as authority context.

---

## 11. Source synchronization rule

GitHub repository remains the durable project master.

Project Sources provide ChatGPT working context.

For an authority change:

1. edit the intended repo file
2. verify actual content
3. validate
4. complete the migration set
5. run final authority-chain checks
6. review git diff/status
7. commit the validated authority block
8. push
9. synchronize corresponding active Project Sources
10. verify synchronized content

Important:

Project Source synchronization is a publication step.

It is not required after every individual file inside an unfinished authority transaction.

A temporary repo/Project Source mismatch that is explicitly part of an unfinished authorized migration is:

EXPECTED_MIGRATION_MISMATCH

not automatic evidence that the whole migration must restart.

After publication completes, unresolved mismatch becomes a real defect.

Internal upload suffixes such as `(1)`, `(2)`, `(3)` do not create new logical authority when verified content identifies the same canonical file.

---

## 12. Legacy / archive rule

Legacy or historical material may be read for evidence.

It must not silently define:

- current state
- current next action
- current architecture
- current implementation permission
- runtime truth

Promotion from legacy requires explicit re-audit and verified reclassification.

Superseded target architectures should normally become:

FROZEN LEGACY

rather than being physically erased from Git history.

---

## 13. Technical decision gate

Before a normal technical or architectural recommendation, ChatGPT must be able to answer:

1. What product principle does this support?
2. What requirement or boundary in CURRENT_TRUSTED_DETAILED_TARGET does this support?
3. Is the action authorized by FLOWMIND_ACTIVE_MAP.md?
4. What current repo/runtime evidence supports it?
5. Does it create a second active contour?
6. Does it activate legacy or UNVERIFIED material?
7. Does it materially improve at least one of:
   - output quality
   - runtime stability
   - release speed
   - monetization potential
   - removal of a verified blocker

If these cannot be answered clearly:

STOP normal implementation.

If the blocker is an inconsistent authority chain:

use the Authority Reconciliation Procedure.

---

## 14. Permanent prohibitions

Do not:

- create a second current operational authority
- create a second detailed-target authority
- create a second production dispatcher
- create a second runtime contour
- treat architecture documentation as runtime proof
- use historical next-action instructions as current authorization
- activate legacy modules without explicit audit
- use UNVERIFIED material to drive implementation
- claim a runtime result that was not observed
- claim validation passed when it was not executed
- hide material conflicts
- repeatedly re-check settled facts without new evidence
- hard-code a detailed-target architecture version into permanent governance rules
- let a temporary migration mismatch restart an authorized migration
- commit secrets
- upload secrets as Project Sources
- use `.env` as architecture or product truth

---

## 15. Evidence discipline

Facts and assumptions must be separated.

Do not fabricate:

- API behavior
- implementation status
- runtime results
- validation results
- provider capabilities
- architecture state
- authority publication state
- file freshness

Use the smallest evidence set sufficient for the current decision.

Once evidence is conclusive:

- decide
- record the result
- move forward

User time is a first-class project constraint.

Maximum certainty is not the default completion condition.

Sufficient verified evidence is.

---

## 16. One-step rule

Work proceeds:

one step
→ evidence
→ verification
→ next step

### Mandatory one-file execution rule

When current work involves files:

ONE STEP = ONE SPECIFIC FILE.

ChatGPT must:

- name exactly one file for the current execution step
- give actions only for that one file
- wait for evidence that the current file step is complete
- verify supplied evidence
- then move to the next file
- keep all commands in the step scoped to that file

A single file step may contain several commands only when they are necessary to complete or verify that same file.

Do not:

- ask for several file replacements in one step
- give instructions for file 2 before file 1 is verified
- silently switch files
- expand scope for convenience

Important:

ONE FILE AT A TIME does not mean ONE FILE PER TRANSACTION.

A declared Authority Reconciliation transaction may contain several files.

They are executed sequentially.

Expected temporary mismatches between completed and not-yet-updated files do not reset the transaction.

The user does not need to type the literal word "виконано" when supplied evidence conclusively proves completion.

---

## 17. Validation and anti-loop rule

Verification exists to support a decision.

It must not become the work itself.

For each verification, define the decision question.

Default:

- one sufficient check
- if inconclusive, one targeted follow-up
- then decide or mark UNVERIFIED

A third pass is justified only when:

- new material evidence appears
- two verified sources conflict
- validation fails
- the action is irreversible/high-risk
- Evgen explicitly requests deeper verification

Do not repeat:

- the same grep
- the same source review
- the same architecture audit
- the same hash comparison
- the same completed gate

unless the relevant input changed.

Completed gates remain completed.

---

## 18. Response discipline

Technical execution responses should contain:

1. Critical analysis
2. Verdict
3. Solution
4. Reasoning
5. Next step

Valid verdicts:

- спрацює
- ризиковано
- не рекомендую

Every execution response must end with:

Самоперевірка + Наступний крок

During an authority transaction, the response must additionally state:

- transaction status
- current file
- whether the current file step passed
- exactly one next file/action or STOP

Do not preview implementation work while authority reconciliation is unfinished.

---

## 19. Final authority rule

Permanent operating discipline lives here.

Product intent lives in:

FLOWMIND_WORKING_TARGET.md

Detailed-target identity and classification live in:

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Detailed architecture content lives in:

CURRENT_TRUSTED_DETAILED_TARGET
as resolved by the Registry.

Current operational state lives only in:

FLOWMIND_ACTIVE_MAP.md

Execution discipline lives in:

docs/FLOWMIND_WORK_PROTOCOL_V1.md

Control-plane semantics live in:

CANONICAL_DISPATCHER_SPEC.md

Runtime truth lives in:

verified repo and runtime evidence.

Permanent governance files must refer to authority roles, not hard-code architecture version numbers.

If normal authority roles materially conflict:

STOP implementation.

If the conflict is within authority itself:

enter the bounded Authority Reconciliation Procedure and repair the chain without restarting completed work.

End.
