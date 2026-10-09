FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE AUTHORITY INDEX Project: FlowMind / Imagine What If
Governance model: SIMPLIFIED AUTHORITY MODEL Updated: 2026-10-07 Scope:
authority classification, role-to-file routing and publication-state
rules only; no current operational state

1. Purpose

This file is the single owner of FlowMind authority classification and
role-to-file routing.

It answers:

-   which file owns each authority role
-   which files are TRUSTED
-   which files are FROZEN LEGACY
-   which files are UNVERIFIED
-   which exact file is CURRENT_TRUSTED_DETAILED_TARGET
-   which files belong to the active authority set
-   how authority publication and Project Source synchronization are
    completed

It does not define current operational state.

Current operational and recovery state belongs only to:

FLOWMIND_ACTIVE_MAP.md

Runtime truth belongs to:

verified current repo and runtime evidence.

2. Classification Model

Every authority-shaped file is classified as exactly one of:

-   TRUSTED
-   FROZEN LEGACY
-   UNVERIFIED

TRUSTED means verified and authorized for the explicit scope assigned in
this Registry.

FROZEN LEGACY means historical, retired, superseded or intentionally
deactivated material. It may provide evidence but must not control
current work.

UNVERIFIED means it is not authorized to control current work.

Publication or migration state is separate from classification.

3. Canonical Authority Roles

3.1 Permanent operating and execution discipline

Role:

CORE_GOVERNANCE

File:

FLOWMIND_CORE_RULES.md

Classification:

TRUSTED

Controls:

-   permanent operating discipline
-   execution discipline
-   logical-action execution
-   evidence sufficiency
-   verification and anti-loop behavior
-   fresh-file and full-replacement discipline
-   Future Impact Gate
-   API/provider preflight discipline
-   security and reliability discipline
-   architecture minimalism discipline
-   Git discipline
-   response discipline
-   new-chat recovery rules

This is the single active owner of permanent operating and execution
discipline.

It does not define current operational state.

3.2 Product intent

Role:

PRODUCT_INTENT

File:

FLOWMIND_WORKING_TARGET.md

Classification:

TRUSTED

Controls:

-   high-level product intent
-   optimization principles
-   scope discipline
-   minimalism / ROI boundaries

It does not define detailed architecture or runtime truth.

3.3 Detailed target architecture

Role:

CURRENT_TRUSTED_DETAILED_TARGET

File:

FLOWMIND_TARGET_ARCHITECTURE_V3_2.md

Classification:

TRUSTED

Controls:

-   detailed target architecture
-   target capability ownership
-   architectural boundaries
-   target contracts and artifacts
-   architecture destination
-   migration principles
-   deferred architectural scope

This role is the only canonical pointer to the current trusted detailed
target.

Permanent governance files should reference:

CURRENT_TRUSTED_DETAILED_TARGET

rather than hard-code an architecture version when the concrete version
is not materially required.

The architecture file does not define current operational state or prove
runtime implementation.

3.4 Current operational and recovery authority

Role:

CURRENT_OPERATIONAL_AUTHORITY

File:

FLOWMIND_ACTIVE_MAP.md

Classification:

TRUSTED

Controls only current/recovery state required to continue work,
including:

-   current mode
-   current target
-   current status
-   verified boundaries
-   material NOT DONE state
-   deferred work
-   current allowed/forbidden work where needed
-   exit conditions
-   current next logical action
-   durable recovery anchors

No other active authority file may independently own current operational
or recovery state.

3.5 Control-plane semantics

Role:

CONTROL_PLANE_SEMANTICS

File:

CANONICAL_DISPATCHER_SPEC.md

Classification:

TRUSTED

Controls only:

-   dispatcher/control-plane semantic contract
-   state-transition discipline
-   guarded transitions
-   HALT / resume semantics
-   state mutation discipline
-   approval/control semantics

It does not define product strategy, current operational state,
detailed-target identity or runtime proof.

3.6 Authority registry

Role:

AUTHORITY_REGISTRY

File:

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Classification:

TRUSTED

Controls:

-   role-to-file routing
-   TRUSTED / FROZEN LEGACY / UNVERIFIED classification
-   CURRENT_TRUSTED_DETAILED_TARGET pointer
-   active authority set
-   authority publication rules
-   Project Sources synchronization rules

It does not define current operational state.

3.7 Runtime truth

Role:

RUNTIME_TRUTH

Source:

verified current repo and runtime evidence

Relevant evidence may include:

-   current code
-   valid input/output
-   validation output
-   generated artifacts
-   downstream consumption
-   runtime logs
-   reproducible execution
-   failure behavior

Documents are not runtime proof.

4. Transitional Compatibility Files

The following files remain temporarily present for compatibility during
the current governance simplification transaction:

4.1 Former permanent operating owner

File:

000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

State:

TRANSITIONAL COMPATIBILITY POINTER

Authority classification:

FROZEN LEGACY upon completion of the current governance publication
transaction.

During the unfinished transaction it must not independently define rules
and must point to:

FLOWMIND_CORE_RULES.md

4.2 Former execution-discipline owner

File:

docs/FLOWMIND_WORK_PROTOCOL_V1.md

State:

TRANSITIONAL REFERENCE / COMPATIBILITY DOCUMENT

Authority classification:

FROZEN LEGACY upon completion of the current governance publication
transaction.

During the unfinished transaction it must not independently define
execution rules and must point to:

FLOWMIND_CORE_RULES.md

These compatibility files are not separate active role owners.

5. Active Authority Set

The intended active authority set after completion of the current
governance publication transaction is:

1.  FLOWMIND_CORE_RULES.md
2.  FLOWMIND_WORKING_TARGET.md
3.  FLOWMIND_TARGET_ARCHITECTURE_V3_2.md
4.  FLOWMIND_ACTIVE_MAP.md
5.  CANONICAL_DISPATCHER_SPEC.md
6.  FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Only these files hold active authority roles defined by this Registry
after transaction completion.

The two transitional compatibility files in Section 4 remain outside the
active role-owner set.

A file not listed here does not gain active authority merely because it
exists in the repo or Project Sources.

5.1 Approved Audit Methodology Reference (non-authoritative)

Reference document: FLOWMIND_AUDIT_FRAMEWORK_V1.md

Classification: APPROVED METHODOLOGY REFERENCE; PUBLISHED IN REPOSITORY
Governance reconciliation remains open until cross-file validation is complete.

Purpose: define the system-wide audit method (Hard Gates, MQS-100,
FDS-100, VQS-100, evidence grading, future-impact checks, and
end-to-end validation).

This reference is NOT a seventh canonical authority, NOT a current
operational checkpoint, and NOT a source of implementation truth.
Its use is governed by the six canonical authority owners above.
The active audit target, progress, evidence boundary, and one next
logical action remain owned exclusively by FLOWMIND_ACTIVE_MAP.md.

The reference must be checked against the current repo before use.
A file existing locally does not by itself prove Git publication or
Project Sources synchronization.

6. FROZEN LEGACY Set

The following files are FROZEN LEGACY:

-   FLOWMIND_TARGET_ARCHITECTURE_V3_1.md
-   FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md
-   docs/FLOWMIND_MAP_GUARD_V1.md
-   CHAT_START_BLOCK_FLOWMIND_CURRENT.md
-   FLOWMIND_CURRENT_WORK_ANCHOR.md
-   FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
-   FLOWMIND_REPO_TRUST_BOUNDARY_V1.md
-   FLOWMIND_SYSTEM_MAP_V1.md
-   FLOWMIND_ACTION_SEQUENCE_V1.md
-   FLOWMIND_CANONICAL_STRUCTURE.md
-   docs/FLOWMIND_HARD_RULESET_V1.md
-   CHAT_START_BLOCK.txt
-   MASTER_PROMPTS_v2_FULL.txt

Upon successful completion and publication of the current governance
simplification transaction, also classify as FROZEN LEGACY:

-   000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
-   docs/FLOWMIND_WORK_PROTOCOL_V1.md

Also FROZEN LEGACY by category unless explicitly re-audited and
reclassified:

-   old IronCore authority-shaped material
-   old horror-specific authority-shaped material
-   old migration-era architecture
-   retired runtime contour documents
-   historical start blocks and work anchors

FROZEN LEGACY material may be read or used as historical evidence.

It must not define current state, current next action, current
architecture, implementation permission, or regain active authority
without explicit re-audit and Registry reclassification.

7. UNVERIFIED Default

Anything authority-shaped that is not explicitly classified as TRUSTED
or FROZEN LEGACY here is:

UNVERIFIED

Do not infer trust from:

-   filename
-   directory
-   ACTIVE / CURRENT / FINAL / CANONICAL / TRUSTED labels
-   version number
-   age
-   Git history
-   GitHub presence
-   Project Sources presence
-   another document referencing it

Review first, then classify.

8. Architecture-Version Rule

Only this Registry may bind:

CURRENT_TRUSTED_DETAILED_TARGET

to a concrete architecture file.

When a future architecture replaces the current target:

1.  validate the candidate architecture
2.  declare an authority reconciliation/publication transaction
3.  reconcile affected authority files
4.  update CURRENT_TRUSTED_DETAILED_TARGET here
5.  classify the superseded target as FROZEN LEGACY
6.  pass final cross-file authority validation
7.  commit and push the validated authority block
8.  synchronize affected Project Sources
9.  verify the final authority chain

A future version change should not require architecture-version edits in
unrelated permanent governance rules.

9. Authority Reconciliation and Expected Mismatch

Authority reconciliation follows the permanent execution discipline in:

FLOWMIND_CORE_RULES.md

During an authorized multi-file authority transaction:

EXPECTED_MIGRATION_MISMATCH

may temporarily exist between already-updated migration files and
not-yet-updated migration files.

This expected mismatch:

-   does not create a second authority
-   does not authorize runtime work
-   does not invalidate completed file PASS results
-   does not require migration restart
-   does not require premature Project Sources synchronization

An unexpected conflict outside the declared migration set is:

UNPLANNED_MATERIAL_CONFLICT

and must be resolved before transaction completion.

10. Dependency and Reference Integrity

When authority roles are merged, renamed, retired, or reassigned,
transaction completion requires a targeted dependency/reference scan.

The scan must determine whether active authority files still:

-   assign a retired file an active role
-   instruct recovery through a retired file
-   depend on a retired procedure that no longer exists
-   hard-code a superseded authority chain
-   recreate duplicate ownership indirectly

References that are purely historical, explanatory, or explicit
compatibility references do not require removal when they cannot control
current work.

Do not declare authority migration complete merely because the directly
edited files pass individually.

11. Publication Gate

Authority publication is evaluated at the validated transaction level.

Do not commit or push the authority block if:

-   a migration-set file failed validation
-   an UNPLANNED_MATERIAL_CONFLICT remains
-   active authority would contain duplicate role owners
-   CURRENT_TRUSTED_DETAILED_TARGET is ambiguous
-   current operational authority is duplicated
-   control-plane authority is duplicated
-   targeted dependency/reference integrity has not been checked
-   git diff contains unexplained changes
-   secrets or unrelated changes may be included
-   intended classifications are unsupported

Publication sequence:

1.  complete migration-set file replacements
2.  verify each file
3.  run targeted dependency/reference scan
4.  reconcile material active references
5.  run final cross-file authority validation
6.  inspect git diff/status
7.  stage only intended changes
8.  commit the validated governance block
9.  push
10. synchronize every affected active Project Source
11. verify synchronized contents
12. run final authority/recovery verification

Do not publish merely because an EXPECTED_MIGRATION_MISMATCH existed
safely during intermediate edits. It must be resolved across the
completed migration set first.

12. Project Sources Rule

GitHub repository is the durable project master.

Project Sources are ChatGPT working context.

An active Project Source must:

-   correspond to an active authority role or be clearly
    non-authoritative context
-   match the intended committed repo version when the repo version
    exists
-   not override newer verified repo evidence
-   not silently reactivate FROZEN LEGACY material

During an unfinished authorized authority transaction, repo/Project
Source mismatch may temporarily be:

EXPECTED_MIGRATION_MISMATCH

when it is a known consequence of the declared transaction.

Project Sources synchronization occurs after the validated governance
block is committed and pushed.

Do not synchronize each authority file independently in the middle of
the transaction unless a specific recovery reason requires it.

After commit/push, every Project Source affected by the governance
transaction must be replaced or synchronized to the intended committed
version before the transaction is considered complete.

This includes changed active authorities and any compatibility source
whose old content could recreate retired ownership.

After synchronization, any unresolved mismatch in an active authority
source is a defect.

Internal upload suffixes such as (1), (2), (3), etc. do not create a new
logical authority when verified content identifies the same canonical
file.

13. Current-State Rule

This Registry must not store:

-   current mode
-   current target
-   current next logical action
-   current implementation priority
-   current allowed/forbidden production work
-   current operational exit condition
-   current runtime implementation status

Those belong only to:

FLOWMIND_ACTIVE_MAP.md

This Registry may define stable authority roles, classifications,
migration rules and publication rules.

It must not become a second Active Map.

14. Runtime Classification Rule

Authority classification and runtime/component state are separate
systems.

Runtime labels do not grant document authority.

No runtime component becomes implemented merely because:

-   target architecture describes it
-   a historical architecture described it
-   an authority file references it
-   a Project Source contains it
-   a fixture resembles it

Runtime capability requires relevant runtime evidence.

15. Validation-Tools Rule

A validation tool proves only what it actually checks.

A passing validation does not automatically:

-   make every scanned file TRUSTED
-   prove end-to-end runtime behavior
-   prove business outcomes
-   validate unknown providers
-   authorize unrelated implementation

Use validation evidence only within its actual scope.

16. Classification-Change Rule

A classification or authority-role change requires enough evidence to
establish:

1.  exact file identity
2.  actual current content
3.  intended role
4.  material conflicts
5.  intended classification
6.  required validation
7.  publication state
8.  Project Source synchronization state where applicable

Do not silently promote or demote authority.

Do not infer classification from filename.

Do not repeat already-completed verification without material reason.

17. Registry Validity

This Registry is valid only while:

-   each active authority role has one owner
-   FLOWMIND_CORE_RULES.md is the single permanent operating/execution
    owner
-   CURRENT_TRUSTED_DETAILED_TARGET resolves to one file
-   FLOWMIND_ACTIVE_MAP.md is the single current operational/recovery
    authority
-   transitional compatibility files do not regain independent authority
-   FROZEN LEGACY remains outside active guidance
-   UNVERIFIED material cannot drive implementation
-   runtime truth remains evidence-based
-   dependency/reference integrity is checked when authority ownership
    changes
-   Project Source mismatches are resolved at publication completion
-   one control-plane authority remains active

If those conditions are materially violated:

STOP normal implementation

Use authority reconciliation only for the evidence required to resolve
the conflict.

18. Canonical Authority Model

Permanent operating/execution discipline: FLOWMIND_CORE_RULES.md

Product intent: FLOWMIND_WORKING_TARGET.md

Detailed-target identity: FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md Role:
CURRENT_TRUSTED_DETAILED_TARGET

Current trusted detailed target: FLOWMIND_TARGET_ARCHITECTURE_V3_2.md

Current operational/recovery authority: FLOWMIND_ACTIVE_MAP.md

Control-plane semantics: CANONICAL_DISPATCHER_SPEC.md

Authority classification/routing: FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Runtime truth: verified current repo and runtime evidence

Transitional compatibility only:
000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
docs/FLOWMIND_WORK_PROTOCOL_V1.md

Historical V3.1 target: FLOWMIND_TARGET_ARCHITECTURE_V3_1.md -> FROZEN
LEGACY

Historical V2.1 target: FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md ->
FROZEN LEGACY

Historical Map Guard: docs/FLOWMIND_MAP_GUARD_V1.md -> FROZEN LEGACY

End.
