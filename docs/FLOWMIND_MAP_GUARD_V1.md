# FLOWMIND MAP GUARD V1

Status: ACTIVE OPERATIONAL GUARD
Project: FlowMind / Imagine What If
Scope: MAP CHECK and anti-drift enforcement only; no current operational authority

## 1. Purpose

This file prevents FlowMind work from drifting away from the verified authority chain, current operational map, product target, and runtime evidence.

This guard does NOT define:

- current mode
- current objective
- current step
- current next action
- current implementation priority
- current allowed production work
- current forbidden production work
- current operational exit condition

All current operational state belongs exclusively to FLOWMIND_ACTIVE_MAP.md.

This guard enforces alignment before technical or architectural work.

---

## 2. Required MAP CHECK

Before every technical or architectural execution response, the assistant must show:

MAP CHECK

Active map:

Current step:

Allowed action:

Forbidden action:

Evidence:

Verdict:

The MAP CHECK must be derived from verified authority and evidence.

The fields:

- Current step
- Allowed action
- Forbidden action
- operational exit condition

must come from FLOWMIND_ACTIVE_MAP.md.

If the assistant cannot fill the MAP CHECK from verified sources:

STOP.

Do not guess.

---

## 3. Authority routing

Authority is role-based.

### Permanent operating discipline

000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

Controls:

- permanent anti-drift rules
- source verification discipline
- authority discipline
- synchronization discipline
- fail-closed behavior
- one-step discipline

It does not define current operational state.

### Product intent

FLOWMIND_WORKING_TARGET.md

Controls:

- high-level product intent
- optimization principles
- scope discipline
- ROI / minimalism boundaries

It is not runtime proof.

### Detailed target architecture

FLOWMIND_TARGET_ARCHITECTURE_V3_1.md

Controls:

- detailed target architecture
- seven logical system blocks
- target capability ownership
- target responsibilities
- target artifacts and contracts
- architectural destination
- migration principles
- deferred architectural scope

It does not define current work.

It is not runtime proof.

It does not authorize implementation by itself.

### Current operational authority

FLOWMIND_ACTIVE_MAP.md

Controls:

- where we are now
- current mode
- current objective
- current step
- current allowed work
- current forbidden work
- current next operational action
- current operational exit conditions

It is the single current operational authority.

### Authority classification

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Controls:

- TRUSTED / FROZEN LEGACY / UNVERIFIED classification
- authority routing
- authority publication gates
- Project Sources reconciliation rules

It does not define current operational state.

### Execution discipline

docs/FLOWMIND_WORK_PROTOCOL_V1.md

Controls:

- execution discipline
- evidence requirements
- file editing discipline
- validation discipline
- Git discipline
- failure handling
- response discipline

It does not define current project state.

### Control-plane semantics

CANONICAL_DISPATCHER_SPEC.md

Controls verified dispatcher and state-transition semantics within its explicit scope.

It is not product strategy, current operational authority, or runtime proof.

### Runtime truth

Current repo and runtime evidence prove:

- what exists
- what runs
- what produces artifacts
- what is consumed downstream
- what passes validation
- what fails

Documents do not substitute for runtime evidence.

---

## 4. Current-state ownership rule

FLOWMIND_ACTIVE_MAP.md is the only source allowed to define current operational state.

This guard must never independently define or cache:

- Current mode
- Current objective
- Current step
- Current next action
- Current implementation priority
- Current allowed work
- Current forbidden work
- Current operational exit condition

Phase-specific restrictions must be read from FLOWMIND_ACTIVE_MAP.md at the time of the MAP CHECK.

Do not copy them into this file as a fallback.

If this guard and FLOWMIND_ACTIVE_MAP.md ever appear to define competing current states:

STOP.

FLOWMIND_MAP_GUARD_V1.md must be reconciled back to guard-only scope.

---

## 5. Unverified authority rule

A file must not control work merely because it:

- exists in the repository
- exists in Project Sources
- has ACTIVE, CURRENT, FINAL, CANONICAL, or TRUSTED in its name or body
- is newer by filename or version number
- is referenced by another authority document
- historically controlled work

Content, scope, freshness, classification, and evidence must be verified.

If verification is insufficient:

UNVERIFIED.

UNVERIFIED material must not drive implementation.

---

## 6. Legacy protection rule

Historical, frozen, archived, donor, migration-era, or retired material may be read for evidence.

It must not silently define:

- current state
- current next action
- current architecture
- current implementation permission
- current runtime truth

Promotion of legacy material requires explicit re-audit and verified classification.

---

## 7. MAP CHECK evidence rule

A valid MAP CHECK must distinguish:

- authority evidence
- repository evidence
- runtime evidence
- assumptions

Architecture documentation proves intent only.

Validation proves only what the validation actually checked.

Historical status documents do not prove runtime behavior.

A runtime claim requires relevant runtime or repository evidence.

If evidence contradicts documentation:

STOP.

Resolve the discrepancy before implementation.

---

## 8. Stop triggers

STOP when:

1. current operational step cannot be obtained from FLOWMIND_ACTIVE_MAP.md;
2. authority roles materially overlap;
3. authority documents materially conflict;
4. source freshness is unknown;
5. a file is trusted only because of its filename or declared status;
6. an action is not authorized by FLOWMIND_ACTIVE_MAP.md;
7. an action would create a second runtime contour;
8. an action would activate legacy or UNVERIFIED code without authorization;
9. runtime evidence contradicts authority documentation;
10. a runtime claim lacks evidence;
11. Project Source and repo authority versions materially differ;
12. a requested commit or push still contains unresolved authority risk.

Do not continue by assumption.

Obtain evidence first.

---

## 9. Source synchronization rule

GitHub repository remains the durable project master.

Project Sources provide ChatGPT working context.

When an active authority file changes:

- verify its actual repo content;
- pass required validation;
- commit and push the intended version before treating it as durable repo truth;
- synchronize the corresponding Project Source;
- verify that the working Project Source reflects the intended committed authority.

A Project Source mismatch is UNVERIFIED until checked.

Internal upload suffixes such as `(1)`, `(2)`, or `(3)` do not create separate logical authority when canonical identity and verified content match.

---

## 10. Anti-drift rule

Before recommending work, verify that the action:

1. is authorized by FLOWMIND_ACTIVE_MAP.md;
2. supports FLOWMIND_WORKING_TARGET.md;
3. is compatible with FLOWMIND_TARGET_ARCHITECTURE_V3_1.md;
4. respects verified authority classification;
5. does not create duplicate operational authority;
6. does not create a second runtime contour;
7. does not activate legacy or UNVERIFIED material;
8. is supported by sufficient repo / runtime evidence.

If these checks do not pass:

STOP.

---

## 11. Guard validity

This guard is valid only while it remains a guard rather than a second operational map.

It must:

- require MAP CHECK;
- route current state to FLOWMIND_ACTIVE_MAP.md;
- route product intent to FLOWMIND_WORKING_TARGET.md;
- route detailed architecture to FLOWMIND_TARGET_ARCHITECTURE_V3_1.md;
- route classification to FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md;
- route execution discipline to FLOWMIND_WORK_PROTOCOL_V1.md;
- route runtime truth to verified repo and runtime evidence;
- stop on unresolved authority conflicts.

It must not store phase-specific current work.

---

## 12. One-step rule

Work proceeds:

one step
→ evidence
→ verification
→ next step

No automatic jumping ahead.

End.