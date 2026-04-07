# FLOWMIND ACTION SEQUENCE V1

## Status
Canonical action order for rebuilding one working FlowMind contour.
This document defines execution order only.
It does not replace system map, dispatcher rules, or canonical state policy.

---

## Core rule

Build only one working contour.

Forbidden:
- parallel rebuild tracks
- new migration branches as active work
- second control centers
- architecture expansion before baseline works
- jumping over steps because something “seems obvious”

Allowed:
- one active contour
- one active priority
- one validation gate after each step
- legacy only as audit source, not authority

---

## Phase order

### Phase 1 — Locked mistakes and principles
Purpose:
- preserve lessons already paid for
- prevent repeating structural errors

Exit condition:
- principles locked
- interaction rules locked
- anti-chaos rules locked

Status:
- completed

---

### Phase 2 — Audit and cleanup
Purpose:
- inspect actual repository reality
- separate working parts from noise
- identify legacy, duplicate, dead, and unclear zones

Must produce:
- clear list of trusted modules
- clear list of untrusted modules
- clear list of dead or frozen modules

Exit condition:
- repo reality is visible
- no fake clarity remains

Status:
- partially completed / requires final consolidation

---

### Phase 3 — Canonical system map
Purpose:
- define one system shape
- mark what is canonical, frozen, legacy, unknown

Must produce:
- one readable system map
- explicit separation of:
  - confirmed
  - unverified
  - frozen legacy

Exit condition:
- one shared architectural picture exists

Status:
- completed

---

### Phase 4 — Canonical action sequence
Purpose:
- define exact rebuild order
- remove ambiguity about “what next”

Must produce:
- one execution sequence
- one step-at-a-time order
- no parallel active workstreams

Exit condition:
- next actions are deterministic

Status:
- in progress

---

### Phase 5 — Build one working contour
Purpose:
- assemble one real operating system
- restore working flow without architectural drift

Build order:
1. repo trust boundary
2. canonical state boundary
3. dispatcher entry path
4. approval/control path
5. production path
6. validation path
7. final operational smoke test

Exit condition:
- one contour runs end-to-end
- result is verified by execution, not assumption

Status:
- not started

---

## Operational order inside Phase 5

### Step 1 — Repo trust boundary
Define:
- what folders/files are canonical
- what is frozen legacy
- what must not be touched during active rebuild

Success signal:
- trusted zone is explicit

### Step 2 — Canonical state boundary
Verify:
- one state authority
- no shadow state
- no reverse write from legacy paths

Success signal:
- state mutation authority is singular

### Step 3 — Dispatcher entry path
Verify:
- one real entry path
- dispatcher controls transition logic
- no hidden side-entry starts runs

Success signal:
- one start path only

### Step 4 — Approval/control path
Verify:
- approval flow is explicit
- manual gates are clear
- no ambiguous override behavior

Success signal:
- operator actions are deterministic

### Step 5 — Production path
Verify:
- core production flow is connected
- script -> assets -> assembly -> QA path is real
- path can run without architectural guessing

Success signal:
- one production chain is runnable

### Step 6 — Validation path
Verify:
- every critical stage has a check
- failure produces a visible stop
- no silent pass

Success signal:
- failures are detectable and localizable

### Step 7 — Final smoke test
Run:
- one minimal end-to-end test through canonical contour

Success signal:
- one actual working contour exists

---

## Non-goals

This document does not authorize:
- building advanced intelligence layers now
- restarting broad migration work
- adding new orchestration frameworks
- expanding multi-channel logic
- inventing new abstractions before baseline recovery

---

## Decision standard

A step is complete only if:
- it is explicitly documented
- it is validated
- it reduced ambiguity
- it moved the system closer to one working contour

If not, it is not complete.

---

## Current next focus

Immediate focus after this document:
- finalize trusted vs frozen repo boundary

That is the next action after Action Sequence V1 is locked.
