# FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP
Project: FlowMind / Imagine What If
Mode: PRODUCTION REENTRY MODE

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
  FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

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

## 2. Verified transition

The authority/source reconciliation phase is complete.

Verified outcome:

- one current operational authority exists:
  FLOWMIND_ACTIVE_MAP.md

- permanent operating discipline is separated from current operational state

- product intent is separated from detailed target architecture

- authority classification is separated from current operational state

- MAP GUARD no longer owns or caches current operational state

- stale operational authority has been removed or frozen

- active authority files have been reconciled

- Project Sources have been synchronized with the verified authority chain

- repo validation / preflight passed

- authority changes were committed and pushed

Production work may therefore resume.

This does NOT mean that historical implementation instructions become current again.

Production work resumes only from verified current repo/runtime evidence.

---

## 3. Current mode

Current mode:

PRODUCTION REENTRY MODE

Current objective:

Resume real FlowMind product development by identifying exactly one highest-value implementation gap from verified current repo/runtime evidence and then implementing that gap without creating a second runtime contour.

The next implementation target must not be selected from:

- stale next-action documents
- historical work anchors
- old chat instructions
- legacy modules
- filename assumptions
- architecture intent alone

The target must be selected from current evidence.

---

## 4. Current step

Current step:

Identify the next concrete production implementation target.

Required sequence:

CURRENT REPO / RUNTIME EVIDENCE
→ COMPARE WITH VERIFIED TARGET ARCHITECTURE
→ IDENTIFY ONE REAL GAP
→ VERIFY ROI / IMPACT
→ AUTHORIZE ONE IMPLEMENTATION TARGET
→ IMPLEMENT
→ VALIDATE

Do not start implementation until the exact gap is evidenced.

Do not automatically resume Director Brain merely because historical documents previously named it as a next action.

Do not select a module merely because it appears important in the target architecture.

Evidence comes first.

---

## 5. Target-selection criteria

The next production task must satisfy all of the following:

1. it exists inside the verified FlowMind target architecture;

2. current repo/runtime evidence shows that it is:
   - missing,
   - incomplete,
   - incorrect,
   - disconnected,
   - or materially blocking the production pipeline;

3. fixing it directly improves at least one of:
   - output quality,
   - runtime stability,
   - production speed,
   - automation,
   - monetization potential;

4. it does not create a second runtime contour;

5. it does not reactivate FROZEN LEGACY code;

6. it does not require speculative infrastructure before measurable value exists;

7. it can be validated with concrete evidence.

If several candidates exist:

choose the smallest change with the highest direct product impact.

Minimalism wins over architectural ambition.

---

## 6. Allowed actions now

Allowed:

- inspect current production repo files
- inspect current runtime behavior
- inspect generated production artifacts
- run existing pipeline paths
- run focused validation
- compare actual implementation with verified target architecture
- identify missing or broken production links
- select one evidence-backed implementation target
- modify production code after the target is verified
- add or update tests directly required by that implementation
- run relevant validation and preflight
- commit and push verified work
- synchronize an authority Project Source when that authority file itself changes

File execution must follow:

ONE STEP = ONE SPECIFIC FILE

unless the user explicitly requests batch mode.

---

## 7. Forbidden actions now

Do not:

- restart authority/source cleanup without new evidence of an authority conflict
- create another current operational document
- create a second runtime contour
- reactivate legacy runner paths
- activate engine/module_runner.py without explicit verified authorization
- activate engine/modules/* merely because they exist
- rewrite dispatcher without evidence that dispatcher behavior is the actual blocker
- add providers merely for optionality
- add integrations merely because they are planned
- add YouTube upload before the production pipeline is ready for publishing
- add Telegram integration
- add TikTok crossposting
- add speculative Pexels/Pixabay integration
- optimize infrastructure before the current production bottleneck is identified
- treat target architecture as proof that a module already exists
- treat historical status documents as current authorization
- implement multiple unrelated gaps at once

---

## 8. Runtime truth rule

Runtime truth outranks documentation about implementation state.

A production capability is considered real only when supported by relevant evidence such as:

- current implementation
- successful execution
- generated artifact
- downstream consumption
- runtime log
- validation output
- reproducible behavior

A file saying that something exists is not enough.

A target architecture saying that something should exist is not enough.

A historical successful run is not automatically proof of current behavior.

---

## 9. Production-contour rule

FlowMind must have one active production contour.

Before modifying code, verify that the change belongs to the current contour.

STOP if the proposed action would:

- create a parallel pipeline
- introduce a second dispatcher path
- introduce a second runner path
- bypass the current manifest/state model
- revive retired architecture
- duplicate an existing responsibility without evidence

Extend the current verified contour.

Do not build around it.

---

## 10. Decision rule

For every proposed implementation target, answer:

1. What exact current problem exists?
2. What evidence proves it?
3. What verified target-architecture responsibility does it map to?
4. What product result improves if we fix it?
5. What is the smallest correct implementation?
6. How will runtime validation prove success?

If these cannot be answered:

STOP.

Gather evidence.

Do not implement from assumption.

---

## 11. Exit condition

PRODUCTION REENTRY MODE ends only when:

1. one exact implementation gap has been identified from current repo/runtime evidence;

2. that gap has been mapped to the verified target architecture;

3. its product / ROI impact has been established;

4. exactly one implementation target has been authorized;

5. the implementation has been completed;

6. relevant validation passes;

7. no second runtime contour or legacy reactivation was introduced;

8. the resulting runtime behavior is evidenced.

After that:

FLOWMIND_ACTIVE_MAP.md must be updated to the next operational phase.

---

## 12. One-step execution rule

Operational work follows the permanent rule defined in:

000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

Default:

ONE STEP = ONE SPECIFIC FILE.

For the current production re-entry phase:

one file
→ evidence
→ verification
→ verdict
→ next file

Do not jump ahead.

Do not batch files unless the user explicitly requests batch mode.

---

## 13. Current next action

Current next action:

Inspect current repo/runtime evidence to identify the single highest-value production implementation gap.

No production code change is authorized until that exact gap is verified.

End.
