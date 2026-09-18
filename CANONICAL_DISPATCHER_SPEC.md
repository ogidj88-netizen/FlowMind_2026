# CANONICAL DISPATCHER SPEC

Status: CANONICAL CONTROL SPEC
Project: FlowMind / Imagine What If
Updated: 2026-09-18
Scope: control-plane contract only

## 1. Purpose

This document defines the intended canonical control-plane behavior for FlowMind.

It defines:

- project phase control
- guarded phase transitions
- HALT / resume behavior
- state mutation discipline
- approval gates
- legacy control separation

It does not define:

- product strategy
- creative reasoning
- Director Brain behavior
- module implementation
- target product architecture
- current runtime proof

Runtime implementation must be verified separately.

---

## 2. Authority scope

This specification controls only dispatcher/control-plane semantics.

It is subordinate to the verified FlowMind authority chain.

It must not override:

- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
- FLOWMIND_WORKING_TARGET.md
- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md
- FLOWMIND_ACTIVE_MAP.md
- newer verified runtime evidence

If this specification materially conflicts with current verified runtime evidence:

STOP.

Audit the conflict before changing runtime behavior.

---

## 3. Dispatcher role

Canonical Dispatcher is the control-plane authority for project phase transitions.

Its responsibility is to:

- read canonical project state
- validate state before transition
- determine whether a requested transition is allowed
- enforce transition guards
- record HALT state
- control resume
- enforce approval-dependent transitions
- persist state through the approved state layer

Dispatcher is not:

- the product brain
- the creative brain
- Director Brain
- Script Writer
- QA content evaluator
- production asset generator
- renderer
- legacy launcher

Dispatcher controls state flow.

It does not make creative content decisions.

---

## 4. Canonical state model

The dispatcher contract uses:

`projects/<PROJECT_ID>/PROJECT_STATE.json`

as the canonical persistent project-state location.

The canonical phase field is:

`phase`

The control contract must not depend on legacy station-style state such as:

- S1_DONE
- S2_DONE
- station completion flags
- legacy current_phase conventions
- ExecutionManifest.json as canonical runtime state

ExecutionManifest-style artifacts may exist as historical or test evidence.

They must not become parallel canonical state authority.

---

## 5. Canonical phases

The canonical control model recognizes:

- TOPIC
- SCRIPT
- SCENES
- ASSETS
- ASSEMBLY
- QA
- READY_FOR_UPLOAD
- UPLOADED
- ARCHIVED
- HALT

These names define the control contract.

This document does not by itself prove that every phase is currently implemented end-to-end.

Runtime support must be verified.

---

## 6. Transition discipline

All phase transitions must be explicit.

The dispatcher must reject:

- illegal transitions
- accidental no-op transitions when not explicitly allowed
- unsafe rollback
- transitions with missing required state
- transitions that bypass required gates
- transitions that rely on legacy state authority

No module may silently advance canonical project phase outside the approved control path.

---

## 7. Guarded transition examples

Required guard semantics include:

### ASSEMBLY -> QA

Allowed only when the required final assembly artifact exists and satisfies the dispatcher contract.

Historical field example:

`artifacts.final_video_path`

The exact current artifact contract must be verified against current runtime before implementation changes.

### QA -> READY_FOR_UPLOAD

Allowed only when the current QA contract has passed.

Historical field example:

`qa_passed = true`

READY_FOR_UPLOAD must not be opened merely because rendering completed.

### READY_FOR_UPLOAD -> UPLOADED

Allowed only after explicit upload approval under the current verified release policy.

Historical field example:

`approved_for_upload = true`

Automatic publication must not be inferred from this specification.

---

## 8. HALT behavior

Dispatcher must support a fail-closed HALT state.

HALT should record enough information to diagnose and resume safely.

Expected control data may include:

- halt_reason
- resume_hint
- previous valid phase
- relevant failure context

HALT must not silently convert into success.

---

## 9. Resume behavior

Resume must occur only through canonical control rules.

Resume must not:

- bypass failed validation
- erase failure evidence
- jump to an arbitrary phase
- reactivate legacy state flow
- bypass approval gates

The requested resume destination must be validated before state mutation.

---

## 10. State mutation discipline

Canonical project state must not have multiple uncontrolled writers.

State mutation must be:

- explicit
- validated
- atomic where applicable
- traceable
- routed through the approved state-control path

Direct uncontrolled writes to PROJECT_STATE.json are forbidden.

Modules may produce artifacts and module outputs.

They must not silently become independent phase-control authorities.

---

## 11. Expected implementation mapping

The following repo paths have historically represented the canonical dispatcher implementation:

- engine/canonical_dispatcher.py
- engine/state_validator.py
- engine/state_store.py

Historical command-surface paths include:

- tools/dispatcher.sh
- tools/dispatcher_cli.py
- tools/check_dispatcher.sh

Their presence in this document does not grant current TRUSTED runtime status.

Each path must be verified against:

- current code
- current contracts
- runtime behavior
- validation output
- downstream use

before current runtime claims are made.

---

## 12. Legacy separation

Legacy control paths must not become parallel control authority.

Historical examples include:

- main.py
- dispatcher/engine.py
- dispatcher/engine_v16.py
- engine/module_runner.py when routing legacy station modules
- ExecutionManifest-driven station flow
- engine/modules/* legacy execution paths

A legacy file may remain in the repository.

Repository presence does not make it active.

---

## 13. One-control-plane rule

FlowMind must have one canonical phase-control authority.

Do not introduce:

- second dispatcher
- parallel phase engine
- second canonical state file
- duplicate transition authority
- hidden module-level phase mutation
- legacy compatibility path that becomes a second runtime controller

Compatibility code must remain subordinate to canonical control.

---

## 14. Separation from productive intelligence

FlowMind productive intelligence and control-plane logic are different responsibilities.

Productive intelligence may decide:

- topic
- story
- script
- scene logic
- visual intent
- creative quality direction

Dispatcher decides only whether the project may move through canonical control state.

Creative reasoning must not be embedded into phase-control logic.

Phase-control logic must not impersonate creative reasoning.

---

## 15. QA and approval separation

Dispatcher enforces gate results.

Dispatcher does not create those results.

For example:

QA system:

- evaluates output
- produces PASS / FAIL or equivalent verified result

Dispatcher:

- reads the verified result
- permits or rejects the transition

Human or release approval:

- produces explicit approval state

Dispatcher:

- enforces that approval before the relevant transition

This separation must remain explicit.

---

## 16. Runtime proof rule

This specification is not runtime proof.

A dispatcher capability is considered current only when supported by relevant evidence such as:

- inspected implementation
- validation
- runtime log
- state transition result
- reproducible test
- generated state artifact
- verified downstream behavior

A historical status document is insufficient.

---

## 17. Failure behavior

Control failures must fail closed.

Forbidden:

- silent transition failure
- fake success
- automatic fallback to legacy control
- swallowing validation errors
- mutating state after failed validation
- continuing with ambiguous state

Errors must be surfaced clearly enough to diagnose.

---

## 18. Idempotency principle

Dispatcher operations should avoid uncontrolled duplicate effects.

Repeated validation of the same state must not corrupt it.

Repeated rejected transitions must not advance state.

Where a transition is not naturally idempotent, the implementation must explicitly protect against accidental duplicate execution.

---

## 19. Current audit rule

During the authority/source reconciliation phase:

- do not rewrite dispatcher runtime
- do not activate legacy dispatcher paths
- do not change phase behavior merely to match this document
- do not assume historical implementation paths are current
- audit specification and runtime separately

The current task is authority alignment, not dispatcher redevelopment.

---

## 20. Verification requirements

Before this specification is used to justify runtime changes, verify:

1. actual dispatcher implementation path;
2. actual state-store path;
3. actual validator path;
4. current PROJECT_STATE schema;
5. current transition rules;
6. HALT / resume behavior;
7. QA transition guard;
8. upload approval guard;
9. absence of competing active state writers;
10. absence of a second active control contour.

If verification fails:

do not redesign immediately.

Record the mismatch and resolve authority first.

---

## 21. Stable control principle

The canonical dispatcher should remain:

- narrow
- deterministic
- fail-closed
- state-focused
- non-creative
- auditable
- resistant to legacy ambiguity

One control plane.

One canonical state authority.

No parallel dispatcher.

No creative brain hidden inside control logic.

End.
