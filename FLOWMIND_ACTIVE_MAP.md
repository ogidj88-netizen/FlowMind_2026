# FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP
Project: FlowMind / Imagine What If
Mode: SYSTEM AUDIT MODE

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

The production re-entry investigation produced useful evidence, but implementation is intentionally paused.

The project direction has been reconsidered after the long development pause and major changes in the external AI market.

Verified decisions:

- FlowMind remains worth evaluating and continuing
- FlowMind is not intended to compete as its own foundation model or commodity media generator
- FlowMind target architecture is v2.2
- FlowMind is the decision and orchestration brain above replaceable external AI providers
- monetization and performance feedback are long-term core intelligence concerns
- internal use comes first
- later service or SaaS commercialization remains possible but is not current scope
- unnecessary custom capabilities should be removed or replaced when stronger external solutions exist
- no production implementation should continue until the existing system has been audited against the updated target
- user time is a first-class constraint
- verification must stop once sufficient evidence exists

---

## 3. Current mode

Current mode:

SYSTEM AUDIT MODE

Current objective:

Perform one evidence-based audit of the existing FlowMind system before further production implementation.

The audit must determine:

- what currently exists
- what actually works
- what is incomplete
- what is broken
- what is duplicated
- what is obsolete
- what should remain internal FlowMind logic
- what should be delegated to external AI or service providers
- what should be removed
- what is still missing relative to target architecture v2.2

The audit exists to produce a modernization decision.

It does not exist to maximize documentation or verification activity.

---

## 4. Audit principle

The audit compares:

CURRENT VERIFIED SYSTEM

against:

FLOWMIND TARGET ARCHITECTURE V2.2

The purpose is not to preserve old work merely because time was invested in it.

The purpose is also not to rewrite everything from zero.

Each inspected component must earn its place.

Default classifications:

- KEEP
- ADAPT
- REPLACE
- REMOVE
- UNKNOWN

Meaning:

KEEP
= current implementation still fits the target and provides value.

ADAPT
= useful implementation exists but must change to fit the target.

REPLACE
= capability is still required, but a stronger external provider or simpler implementation should perform it.

REMOVE
= capability is unnecessary, duplicated, obsolete, or economically unjustified.

UNKNOWN
= evidence is insufficient for a decision.

UNKNOWN must not be converted into a guess.

---

## 5. Audit questions

For each relevant component, answer only what is necessary:

1. What responsibility does it currently own?
2. Is it part of the active runtime contour?
3. What evidence shows that it actually works?
4. Which v2.2 target responsibility does it map to?
5. Is this responsibility strategic FlowMind intelligence or commodity execution?
6. Should FlowMind own it internally?
7. Could an external AI/service now perform it better, cheaper, or more reliably?
8. Does keeping it improve:
   - monetization potential,
   - decision quality,
   - content quality,
   - automation,
   - reliability,
   - speed?
9. Classification:
   KEEP / ADAPT / REPLACE / REMOVE / UNKNOWN.
10. What is the smallest future action required?

Do not answer questions that are irrelevant to the component being inspected.

---

## 6. Strategic ownership rule

FlowMind should preferentially own:

- canonical state
- orchestration
- decision logic
- opportunity evaluation
- business rules
- provider selection logic
- validation logic
- quality gates
- performance interpretation
- monetization interpretation
- decision memory
- feedback loops

FlowMind should not automatically own commodity execution capabilities.

Examples of potentially external execution:

- general LLM reasoning
- search
- trend data
- image generation
- video generation
- TTS
- music generation
- stock media sourcing
- transcription
- rendering services
- analytics sources

Whether a capability is internal or external must be decided from evidence, quality, cost, reliability, and strategic value.

Do not replace working internal logic merely because an external tool exists.

Do not preserve inferior internal execution merely because it already exists.

---

## 7. Provider rule

Named providers are implementation choices, not architecture.

During audit, identify provider coupling where relevant.

Target:

FlowMind module
-> capability contract
-> selected provider
-> normalized result
-> validation
-> downstream artifact

The audit may recommend provider abstraction.

The audit must not automatically implement provider abstraction.

Automatic multi-provider routing remains deferred until justified by evidence.

---

## 8. Monetization rule

The system is ultimately judged by business outcomes.

Audit priority should favor components that affect:

- selection of economically useful opportunities
- audience demand
- hooks and retention
- content quality
- production cost
- production speed
- ability to collect performance data
- ability to connect content decisions to revenue outcomes

A technically elegant component with little economic impact has low priority.

A simple component with direct economic impact may have high priority.

---

## 9. Audit execution rule

Audit proceeds one file at a time.

Default:

ONE STEP = ONE SPECIFIC FILE.

For each file:

inspect
-> understand responsibility
-> obtain sufficient evidence
-> classify
-> stop checking
-> move to next file

Do not:

- repeatedly verify an established fact
- inspect unrelated files in the same step
- modify code during evidence collection
- create speculative replacement architecture
- create new providers during audit
- refactor while still determining what exists

If a file points to another file that must be inspected:

finish classification of the current file first when possible.

Then move to the next file as a separate step.

---

## 10. Audit scope

The audit may inspect:

- production entrypoints
- dispatcher/control logic
- canonical state handling
- executors
- modules
- provider integrations
- artifact contracts
- renderer
- validation
- QA
- generated runtime artifacts
- configuration
- tests where needed to establish behavior

Legacy material is inspected only when necessary to determine whether active code depends on it.

Do not perform a general legacy archaeology exercise.

---

## 11. Code freeze during audit

Production code modification is not authorized during SYSTEM AUDIT MODE.

Allowed exceptions:

- none by default

If a critical defect is discovered:

record it.

Do not immediately repair it unless Evgen explicitly ends or pauses the audit and authorizes implementation.

The purpose is to understand the whole system before changing its structure.

This prevents local fixes from locking us into obsolete architecture.

---

## 12. Verification sufficiency

Verification follows:

docs/FLOWMIND_WORK_PROTOCOL_V1.md

Key rule:

sufficient evidence
-> decision
-> stop checking

Default maximum:

- one primary check
- one targeted follow-up only if required

More checking requires a specific reason under the protocol.

User time is the most constrained resource.

---

## 13. Forbidden actions now

Do not:

- modify production Python code
- resume qa_executor.py work
- implement the previously identified QA blocker
- automatically resume Director Brain
- rewrite dispatcher
- build a new runner
- create a second runtime contour
- reactivate frozen legacy
- add providers
- add speculative integrations
- build automatic provider routing
- build SaaS infrastructure
- implement YouTube upload
- implement monetization automation
- optimize code before audit evidence exists
- start multiple audit files in one step
- preserve a component only because work was previously invested in it

---

## 14. Audit output

The audit must ultimately produce a clear modernization picture.

For the current FlowMind system we must know:

- what stays
- what changes
- what is replaced externally
- what is deleted
- what is missing
- what becomes the FlowMind Brain
- what remains commodity execution
- what the shortest route to a monetizable internal system is

The audit is complete only when there is enough evidence to choose the modernization plan.

It is not necessary to inspect every file in the repository.

Stop when further inspection would not materially change the modernization decision.

---

## 15. Exit condition

SYSTEM AUDIT MODE ends when:

1. the active production contour is understood;
2. the major current components are classified;
3. material obsolete or duplicated areas are identified;
4. internal strategic intelligence is separated from commodity execution;
5. relevant provider coupling is understood;
6. major gaps against target architecture v2.2 are identified;
7. the modernization direction is clear;
8. the shortest path to first monetizable operation can be selected;
9. further inspection is unlikely to materially change the decision;
10. Evgen approves moving from audit to implementation planning.

Only then may implementation work resume.

---

## 16. Current next action

Current next action:

Begin the evidence-based audit of the existing FlowMind production system.

Start from the current active production entry/control path, not from historical architecture documents.

Inspect one specific file at a time.

No production code change is authorized during the audit.

End.