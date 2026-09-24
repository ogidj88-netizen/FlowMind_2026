# FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP
Project: FlowMind / Imagine What If
Mode: TARGET ARCHITECTURE PROMOTION MODE
Updated: 2026-09-24

## 1. Purpose

This file is the single current operational authority for FlowMind.

It defines only:

- where the project is now
- current mode
- current objective
- current step
- current allowed work
- current forbidden work
- current exit condition

It does NOT define:

- permanent operating discipline
- high-level product intent
- detailed target architecture
- runtime truth
- historical project state

Authority routing:

- permanent operating discipline:
  000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

- high-level product intent:
  FLOWMIND_WORKING_TARGET.md

- detailed target architecture:
  FLOWMIND_TARGET_ARCHITECTURE_V3_1.md

- authority classification:
  FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

- MAP CHECK / anti-drift:
  docs/FLOWMIND_MAP_GUARD_V1.md

- execution discipline:
  docs/FLOWMIND_WORK_PROTOCOL_V1.md

- control-plane semantics:
  CANONICAL_DISPATCHER_SPEC.md

- actual implementation truth:
  verified repo and runtime evidence

---

## 2. Verified Background

The previous authority/source reconciliation phase was completed successfully.

Verified outcome before the V3.1 transition:

- one current operational authority existed:
  FLOWMIND_ACTIVE_MAP.md

- permanent operating discipline was separated from current operational state

- product intent was separated from detailed target architecture

- authority classification was separated from current operational state

- MAP GUARD no longer owned or cached current operational state

- stale operational authority had been removed or frozen

- active authority files had been reconciled

- Project Sources had been synchronized with the then-published authority chain

- repo validation / preflight had passed

- authority changes had been committed and pushed

Production re-entry subsequently exposed real runtime evidence and enabled a new architecture review.

That review resulted in an explicitly authorized V3.1 target architecture candidate.

V3.1 promotion is now the current work.

This does NOT mean V3.1 capabilities are implemented.

Target architecture remains distinct from runtime truth.

---

## 3. Current Mode

Current mode:

TARGET ARCHITECTURE PROMOTION MODE

Current objective:

Promote FLOWMIND_TARGET_ARCHITECTURE_V3_1.md into the single trusted detailed target architecture while preserving:

- one current operational authority
- one production contour
- current verified runtime truth
- existing control-plane semantics
- full auditability
- fail-closed publication discipline

This is an authority/documentation transition.

It is NOT a production runtime rewrite.

---

## 4. Why This Mode Exists

The previously trusted detailed target architecture was:

FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

A new candidate has now been created:

FLOWMIND_TARGET_ARCHITECTURE_V3_1.md

The V3.1 candidate consolidates later verified architecture decisions including:

- simplified logical ownership boundaries
- Opportunity Intelligence
- Packaging-first Editorial Brain
- two-pass Director
- Media Router
- deterministic rendering
- Quality and Compliance
- persistent Learning Loop
- External / Competitor Intelligence
- persistent FlowMind memory
- cloud-first target
- Capability Registry
- Capability Evolution Loop
- Human Decision Gateway
- cost and latency governance

The user explicitly authorized finalization and promotion of V3.1.

The promotion must still satisfy publication and verification gates.

---

## 5. Current Step

Current step:

Complete the V3.1 authority migration.

Required sequence:

V3.1 CANDIDATE CREATED
→ VERIFY CONTENT
→ UPDATE AUTHORITY REGISTRY
→ UPDATE TRUSTED AUTHORITY REFERENCES
→ VERIFY AUTHORITY CONSISTENCY
→ RUN RELEVANT VALIDATION / PREFLIGHT
→ REVIEW GIT DIFF / STATUS
→ COMMIT
→ PUSH
→ SYNCHRONIZE PROJECT SOURCES
→ VERIFY FINAL AUTHORITY CHAIN
→ RETURN TO PRODUCTION REENTRY

Do not treat V3.1 as durable published authority until this sequence completes.

---

## 6. Verified Progress In This Transition

Verified so far:

### V3.1 target file

`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md`

- created
- non-empty
- expected header present
- Authority Note present
- expected ending present
- suspicious terminal/session contamination check passed
- candidate file currently exists as an untracked repo file

### Source of Truth Registry

`FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md`

- updated locally for the intended V3.1 authority state
- V3.1 target references present
- V2.1 retained as historical/FROZEN LEGACY after successful publication
- registry consistency line verified
- `git diff --check` passed for the edited registry

### Permanent project instructions

`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

- original local file verified against known content
- detailed-target routing updated from V2.1 to V3.1
- old V2.1 detailed-target references removed
- V3.1 references verified
- `git diff --check` passed

### Active Map baseline

Before this edit:

- local Active Map matched Git HEAD
- local SHA and Git HEAD SHA matched
- no local diff existed
- Project Source copy did not byte-match current repo copy and must therefore be synchronized later

This proves the repo copy is the current durable baseline for this edit.

---

## 7. Allowed Actions Now

Allowed:

- inspect one current authority file at a time
- replace one current authority file at a time
- update references from V2.1 to V3.1 where authority role requires it
- verify each changed authority file
- compare changed authority files for consistency
- inspect validation/preflight scripts before execution when required
- run relevant authority validation
- run preflight when safe and relevant
- inspect git diff
- inspect git status
- commit only intended V3.1 authority migration files
- push the verified authority migration
- synchronize changed active Project Sources after push
- remove/supersede stale active Project Source copies where required
- verify the final authority chain
- update this Active Map after successful publication to return to production work

File execution follows:

ONE STEP = ONE SPECIFIC FILE

unless the user explicitly authorizes batch mode.

---

## 8. Forbidden Actions Now

Do not:

- modify production implementation code
- implement V3.1 runtime capabilities merely because they appear in the target
- create another current operational document
- create a second runtime contour
- create a second dispatcher
- activate legacy runner paths
- reactivate FROZEN LEGACY runtime modules
- rewrite dispatcher behavior
- add new providers
- add optional integrations
- activate YouTube upload
- add Telegram integration
- add TikTok integration
- build speculative infrastructure
- perform provider/model migration
- modify learning policies
- run paid provider jobs merely for this authority migration
- treat V3.1 documentation as implementation evidence
- commit unrelated runtime baseline directories
- silently include unrelated untracked files in the authority commit

---

## 9. V2.1 Transition Rule

During successful V3.1 publication:

`FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md`

transitions from:

TRUSTED detailed target architecture

to:

FROZEN LEGACY historical target architecture.

It may remain in Git for:

- history
- migration evidence
- architectural comparison

It must not remain in the active Project Source authority set after V3.1 publication.

V2.1 runtime-era code is NOT automatically legacy merely because the V2.1 architecture document becomes FROZEN LEGACY.

Runtime components are classified from current repo/runtime evidence.

---

## 10. V3.1 Promotion Rule

`FLOWMIND_TARGET_ARCHITECTURE_V3_1.md` becomes durable trusted detailed target architecture only after:

1. exact candidate content is verified
2. authority references are reconciled
3. no material authority conflict remains
4. relevant validation passes
5. preflight passes where applicable
6. git diff is reviewed
7. only intended migration files are staged
8. commit succeeds
9. push succeeds
10. active Project Sources are synchronized
11. final authority chain is verified

Until then:

the migration is in progress.

Fail closed if publication fails.

---

## 11. Runtime Truth Rule

Runtime truth remains independent of this migration.

A V3.1 capability is operationally real only when supported by evidence such as:

- current implementation
- valid inputs
- successful execution
- generated output
- downstream consumption
- validation output
- reproducible runtime behavior
- failure behavior

Architecture does not manufacture runtime truth.

Changing target documentation does not change implementation status.

---

## 12. Production Contour Rule

FlowMind must continue to have one production contour.

The V3.1 architecture migration must not:

- create a parallel pipeline
- create a second dispatcher
- create a second runner authority
- bypass existing state
- bypass existing manifest/control semantics
- reactivate retired implementation automatically

After architecture publication, existing runtime components must be classified against V3.1 as:

- KEEP
- MODIFY
- REPLACE
- REMOVE
- MISSING

That comparison happens only after the authority migration completes.

---

## 13. Project Sources Rule For This Transition

GitHub repository remains the durable project master.

Project Sources are ChatGPT working context.

Current Project Sources may temporarily contain the previous published authority while the V3.1 migration is still local.

Do not synchronize candidate working copies before the intended repo versions:

- pass validation
- are committed
- are pushed

After push:

- synchronize every changed active authority Project Source
- add the verified V3.1 target source
- ensure V2.1 no longer participates as active target authority
- verify Project Source content matches intended committed repo content

Any stale Project Source mismatch is UNVERIFIED until synchronized.

---

## 14. Git Safety Rule

The V3.1 authority commit must contain only intended authority migration files.

Known runtime baseline directories currently exist as untracked working-tree artifacts:

- `projects/FM_RUNTIME_BASELINE_20260923/`
- `projects/FM_RUNTIME_BASELINE_20260923_R2/`
- `projects/FM_RUNTIME_BASELINE_20260923_R3/`

They must NOT be accidentally staged merely because they are visible in `git status`.

Do not use broad staging such as:

`git add .`

for this migration.

Stage exact intended files only.

---

## 15. Exit Condition

TARGET ARCHITECTURE PROMOTION MODE ends only when all of the following are true:

1. `FLOWMIND_TARGET_ARCHITECTURE_V3_1.md` is verified

2. `FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md` correctly classifies:
   - V3.1 as detailed target architecture
   - V2.1 as FROZEN LEGACY after publication

3. all active authority documents route detailed architecture to V3.1

4. no active authority document incorrectly treats V2.1 as current detailed target

5. no current operational authority duplication exists

6. validation required for the authority migration passes

7. preflight passes where applicable

8. intended Git diff is reviewed

9. only intended authority migration files are committed

10. push succeeds

11. changed active Project Sources are synchronized

12. V3.1 is present in active Project Sources as the detailed target

13. V2.1 is removed from active target decision context

14. final authority chain is verified

15. runtime truth remains unchanged unless separately evidenced

After all conditions pass:

update `FLOWMIND_ACTIVE_MAP.md` again.

Return to:

PRODUCTION REENTRY MODE

Then execute:

CURRENT REPO / RUNTIME EVIDENCE
→ COMPARE WITH V3.1
→ KEEP / MODIFY / REPLACE / REMOVE / MISSING
→ IDENTIFY ONE HIGHEST-VALUE REAL GAP
→ VERIFY ROI / IMPACT
→ AUTHORIZE ONE IMPLEMENTATION TARGET
→ IMPLEMENT
→ VALIDATE

---

## 16. One-Step Execution Rule

Operational work follows the permanent rule defined in:

`000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md`

Default:

ONE STEP = ONE SPECIFIC FILE.

For this migration:

one authority file
→ evidence
→ verification
→ verdict
→ next authority file

Do not jump ahead.

Do not batch files unless the user explicitly requests batch mode.

---

## 17. Current Next Action

Current next action:

Continue reconciling remaining TRUSTED authority references from the superseded V2.1 target to the V3.1 target, one verified authority file at a time.

No production implementation work is authorized during this transition.

End.