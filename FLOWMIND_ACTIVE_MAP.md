# FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP
Project: FlowMind / Imagine What If
Mode: PRODUCTION REENTRY MODE
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

## 2. Verified Authority Transition

The V3.1 target-architecture promotion sequence has completed.

Verified outcome:

- FLOWMIND_TARGET_ARCHITECTURE_V3_1.md is the trusted detailed target architecture

- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md is FROZEN LEGACY historical architecture

- all active authority references route detailed target architecture to V3.1

- changed authority files passed required validation / preflight

- intended authority migration was committed and pushed

- changed active Project Sources were synchronized

- V2.1 was removed from active Project Source target-decision context

- final authority-chain verification passed

This authority transition did not change runtime implementation truth.

Architecture publication is not implementation evidence.

---

## 3. Current Mode

Current mode:

PRODUCTION REENTRY MODE

Current objective:

Resume real FlowMind product development from verified repo and runtime evidence.

The immediate objective is to compare the verified current implementation against the trusted V3.1 target architecture and identify exactly one highest-value real implementation gap.

Do not select work from architecture importance alone.

Do not select work from historical next-action documents.

Do not automatically resume a previously planned module.

Evidence and ROI determine the next implementation target.

---

## 4. Verified Runtime Evidence Baseline

The AS-IS runtime walkthrough was completed before V3.1 promotion.

Verified runtime baseline projects include:

- projects/FM_RUNTIME_BASELINE_20260923/
- projects/FM_RUNTIME_BASELINE_20260923_R2/
- projects/FM_RUNTIME_BASELINE_20260923_R3/

These baselines are evidence artifacts.

Do not modify them merely to make current runtime appear compliant with V3.1.

Do not repeat the complete AS-IS walkthrough unless:

- evidence is missing
- current code materially changed
- a contradiction is discovered
- the selected implementation target requires narrower verification

Existing runtime findings must be reused before performing new broad inspection.

---

## 5. Current Step

Current step:

Compare verified current runtime against V3.1 and identify one highest-value implementation gap.

Required sequence:

VERIFIED CURRENT REPO / RUNTIME EVIDENCE
→ MAP EXISTING COMPONENTS TO V3.1
→ CLASSIFY EACH RELEVANT COMPONENT
→ KEEP / MODIFY / REPLACE / REMOVE / MISSING
→ IDENTIFY ONE MATERIAL GAP
→ VERIFY ROI / IMPACT
→ AUTHORIZE ONE IMPLEMENTATION TARGET
→ IMPLEMENT
→ VALIDATE

No implementation change starts before the exact gap is evidenced and authorized.

---

## 6. Classification Rule

For each relevant existing component use exactly one classification:

### KEEP

Current implementation already satisfies the required V3.1 responsibility sufficiently for the present production stage.

### MODIFY

The current component is useful but requires a controlled change to satisfy the V3.1 responsibility.

### REPLACE

The current implementation is structurally incompatible with the required responsibility and modification would create greater risk or complexity than replacement.

### REMOVE

The component is redundant, unsafe, obsolete, or creates competing authority / runtime behavior.

### MISSING

V3.1 requires a capability for which no verified current implementation exists.

Classification must be evidence-based.

Do not classify from filenames alone.

---

## 7. Selection Rule

After classification, select exactly one next implementation target.

The selected target must have the highest practical value based on:

- output quality
- runtime stability
- production completion
- release speed
- monetization impact
- blocker removal
- implementation risk
- implementation cost

Prefer the smallest controlled change that closes the highest-value verified gap.

Do not optimize components that are not currently blocking meaningful production progress.

---

## 8. Allowed Actions Now

Allowed:

- inspect already verified runtime evidence

- inspect specific repo files required to classify a V3.1 responsibility

- compare current implementation with V3.1

- reuse completed AS-IS walkthrough evidence

- classify relevant components as:
  KEEP / MODIFY / REPLACE / REMOVE / MISSING

- identify one highest-value implementation gap

- verify ROI and operational impact

- authorize one implementation target

- after authorization, modify one specific implementation file at a time

- run focused validation relevant to the selected target

- preserve the current canonical dispatcher and state authority unless evidence proves a required controlled change

Default execution remains:

ONE STEP = ONE SPECIFIC FILE

unless explicitly authorized otherwise.

---

## 9. Forbidden Actions Now

Do not:

- restart the full repository audit without a verified need

- restart the full runtime walkthrough without a verified need

- implement multiple architecture gaps at once

- rewrite the whole pipeline

- create a second dispatcher

- create a second runtime contour

- create duplicate project-state authority

- reactivate FROZEN LEGACY modules automatically

- treat V2.1 as current target architecture

- treat V3.1 documentation as proof of implementation

- add new providers merely because V3.1 allows provider abstraction

- build cloud infrastructure merely because V3.1 is cloud-first

- build Capability Evolution before a verified production need

- expand signal sources before existing production blockers are resolved

- add optional integrations without direct production value

- activate autonomous public upload without separate evidence and authorization

- modify learning policies before production evidence justifies the change

- optimize cost before the relevant production path actually works unless cost itself is the blocking risk

---

## 10. Runtime Truth Rule

Runtime truth comes only from current verified repo and runtime evidence.

A capability is not operational merely because:

- V3.1 describes it
- a file exists
- a function exists
- a test fixture exists
- an artifact name exists
- a historical document says it worked

Operational capability requires relevant evidence such as:

- valid implementation
- valid input
- successful execution
- expected output
- downstream consumption
- validation
- observable failure behavior where applicable

If documentation and runtime evidence conflict:

STOP.

Runtime evidence wins for implementation status.

---

## 11. Production Contour Rule

FlowMind must maintain one production contour.

Do not introduce:

- parallel orchestration
- alternative project-state ownership
- alternative dispatcher authority
- uncontrolled direct state writers
- legacy bypass paths

The current verified runtime should evolve toward V3.1 through controlled KEEP / MODIFY / REPLACE / REMOVE / MISSING decisions.

Prefer evolution over rewrite.

---

## 12. Architecture Rule

V3.1 defines the destination.

It does not dictate implementation order.

Implementation order is determined by:

current evidence
→ current blocker
→ business impact
→ implementation risk
→ ROI

Do not build later-stage architecture merely because it is architecturally attractive.

Minimalism remains the default.

---

## 13. Git Safety Rule

Known runtime baseline directories may exist as untracked evidence:

- projects/FM_RUNTIME_BASELINE_20260923/
- projects/FM_RUNTIME_BASELINE_20260923_R2/
- projects/FM_RUNTIME_BASELINE_20260923_R3/

Do not stage them accidentally.

Do not use broad staging such as:

git add .

when unrelated or evidence files are present.

Stage only explicitly intended files.

---

## 14. Exit Condition

PRODUCTION REENTRY MODE completes when:

1. relevant existing runtime components are compared against V3.1

2. evidence-based KEEP / MODIFY / REPLACE / REMOVE / MISSING classification exists for the current decision scope

3. exactly one highest-value real implementation gap is identified

4. its ROI / impact is verified

5. one implementation target is explicitly authorized

At that point:

move from re-entry analysis to focused implementation.

Do not open multiple implementation targets simultaneously.

---

## 15. Current Next Action

Current next action:

Use the already completed AS-IS runtime walkthrough and current repo evidence to compare the existing production contour against V3.1.

Produce the minimum evidence-backed KEEP / MODIFY / REPLACE / REMOVE / MISSING classification required to identify exactly one highest-value implementation gap.

Do not implement yet.

End.