# FlowMind Canonical Structure

## 0. System layers

### A. Topic Intelligence Layer
- Topic Intelligence Lite v1
- collects market signals
- filters weak topics before production
- outputs Topic Queue

### B. Control Layer
- Manifest
- Dispatcher
- Project State

### C. Production Layer
- Topic execution pipeline
- artifact generation
- QA

### D. Publication Layer
- Telegram approval
- upload scheduling
- publication

---

## 1. Core authority

### [0] Manifest
- immutable project definition
- defines niche, mode, render profile, queue source, and project rules
- must remain locked after creation

### [1] Dispatcher
- single control authority
- only component allowed to mutate Project State
- controls transitions and gate decisions

### [2] Project State
- mutable only through dispatcher-controlled transitions
- represents the current lifecycle phase
- stores guards, approvals, halt state, and phase history

---

## 2. Canonical flow

### Topic selection flow
[TI] Topic Intelligence Lite
↓
[QUEUE] Topic Queue
↓
[PPG] Pre-Production Gate

### Production flow
[3] TOPIC_SELECTED
↓
[4] SCRIPT_READY
↓
[5] SCENES_READY
↓
[6] ASSETS_READY
↓
[7] ASSEMBLY_READY
↓
[8] QA_PASSED

### Review and publication flow
[9] READY_FOR_REVIEW
↓
[10] TELEGRAM_APPROVED
↓
[11] READY_FOR_UPLOAD
↓
[12] SCHEDULED
↓
[13] PUBLISHED

---

## 3. Topic Intelligence role

Topic Intelligence Lite v1:
- does not produce videos
- does not write scripts
- does not predict guaranteed virality
- filters weak topics before production

Inputs:
- Google Trends
- YouTube market check
- Reddit pain support

Outputs:
- Topic Queue
- Top topic packets
- shortlist
- kill list

---

## 4. Module sequence

### Topic Intelligence
- collects signals
- clusters and scores topic candidates
- outputs topic packets

### Script Module
- input: approved topic packet + manifest + allowed state
- output: script artifact

### Scenes Module
- input: script artifact
- output: scene breakdown

### Assets Module
- input: scenes
- output: asset set

### Assembly Module
- input: assets + structure
- output: final video artifact

### QA Module
- input: final video artifact
- output: QA result

### Review Layer
- input: QA-passed package
- output: Telegram approval decision

### Upload Layer
- input: approved upload-ready package
- output: publication side-effect
- ends in PUBLISHED

---

## 5. Dependency rules

Manifest
→ defines project contract

Dispatcher
→ controls state transitions
→ enforces gate rules

Project State
→ represents active phase and approval state

Modules
→ must not bypass dispatcher authority
→ run only when their phase is valid

Artifacts
→ are outputs of module execution
→ must align with current state phase

Topic Queue
→ is the only source of next production topic

---

## 6. Hard invariants

- Manifest is immutable after lock
- Dispatcher is the only state authority
- Only one active phase is valid at a time
- Phase transitions must be explicit
- No-op transitions are forbidden
- Weak topics must not enter production
- Upload cannot happen before QA pass
- Upload cannot happen before Telegram approval
- Phase history must always be preserved
- Runtime execution must not rewrite manifest authority

---

## 7. What is inside the canonical structure
- topic intelligence placement
- control authority
- lifecycle phases
- module order
- dependency direction
- transition rules
- artifact relationship to phases
- approval and publication flow

---

## 8. What is outside the canonical structure
- implementation details of uploader
- ffmpeg internals
- provider-specific execution logic
- optimization logic
- forecasting engines
- deep analytics
- advanced multi-channel strategy

---

## 9. Canonical conclusion

The canonical structure of FlowMind is:

Topic Intelligence
→ Topic Queue
→ Pre-Production Gate
→ Dispatcher-controlled Production
→ QA
→ Telegram Approval
→ Upload / Publish

Execution details are separate and must not redefine the structure.
