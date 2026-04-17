# FLOWMIND — 6 CORE ENGINES CONTRACTS v1

## 1. Purpose
This document defines the canonical architecture of FlowMind as a 6-engine production system.

It exists to:
- eliminate ambiguity
- enforce strict module boundaries
- define input/output contracts
- enforce PASS/FAIL behavior
- prevent architectural drift

This document is the single source of truth for production implementation.

---

## 2. Global System Laws

### Law 1 — Single Control Contour
- Dispatcher is the only control layer
- PROJECT_STATE.json is the only state authority
- No engine can change phase autonomously

### Law 2 — Dumb Execution
All execution engines:
- take a contract
- execute
- return output

They must NOT:
- compensate for other modules
- generate fallback artifacts
- change system logic

### Law 3 — Fail Closed
If an engine cannot produce valid output:
- it must fail
- no placeholders allowed

### Law 4 — Director = Only Creative Brain
Only Director defines:
- scenes
- shots
- visual logic
- timing intent

All other engines execute.

### Law 5 — Audio = Master Clock
Final audio defines:
- real timing
- scene duration

### Law 6 — Working Promise Lock
Every video must:
- follow its promise
- not deviate across modules

### Law 7 — Style Lock
Every video has a fixed style.
All engines must respect it.

### Law 8 — Anti-Repeat
Previously used stock assets must not repeat.
Enforced by Asset Engine.

---

## 3. Lifecycle

TOPIC → SCRIPT → SCENES → ASSETS → ASSEMBLY → QA → READY_FOR_UPLOAD → UPLOADED

No deviations allowed.

---

## 4. TOPIC ENGINE

Input:
- niche/profile
- signals

Output:
- topic
- hook
- working_title
- working_promise
- numeric_anchor OR trigger_word
- style_lock

PASS:
- specific topic
- strong hook
- clear promise

FAIL:
- vague topic
- weak hook
- unclear promise

Forbidden:
- writing script
- selecting assets
- directing scenes

---

## 5. SCRIPT ENGINE

Input:
- topic contract

Output:
- script.txt
- metrics

PASS:
- > minimum length
- strong early hook
- aligned with promise

FAIL:
- short
- weak
- off-topic

Forbidden:
- asset selection
- directing visuals

---

## 6. DIRECTOR ENGINE

Input:
- script
- style_lock

Output:
- scene plan
- shot plan
- subtitle intent
- SFX intent
- music intent
- motion intent
- normalized asset queries

PASS:
- full script coverage
- realistic shots
- strong hook visuals

FAIL:
- abstract scenes
- impossible visuals
- weak hook dynamics

Forbidden:
- selecting actual assets
- generating audio
- assembling video

---

## 7. ASSET ENGINE

Input:
- shot plan
- queries
- style_lock

Output:
- voice file
- timeline
- selected assets

PASS:
- audio exists
- all shots resolved
- no repeats
- style respected
- timeline matches audio

FAIL:
- missing audio
- missing assets
- repeats
- style mismatch

Forbidden:
- rewriting script
- changing direction
- assembling video

---

## 8. ASSEMBLY ENGINE

Input:
- timeline
- assets
- audio
- subtitles
- SFX
- music
- motion presets

Output:
- final.mp4

PASS:
- file exists
- video valid
- audio synced

FAIL:
- broken file
- missing audio
- major desync

Forbidden:
- creative decisions
- altering plan

---

## 9. QA / PACKAGE ENGINE

Input:
- final video
- topic contract
- metadata

Output:
- QA verdict
- 2 titles
- 2 thumbnails
- review package

PASS:
- valid video
- hook delivered
- consistent meaning
- promise respected

FAIL:
- technical errors
- mismatch content
- misleading packaging

Forbidden:
- rewriting script
- reassembling video

---

## 10. Non-Core Modules
These are internal layers, not engines:
- stock memory
- timing reconciliation
- subtitles
- SFX
- music
- query normalization

---

## 11. Out of Scope (v1)
- A/B testing infra
- BPM sync
- phoneme alignment
- multi-channel scaling
- self-modifying logic

---

## 12. Conclusion
FlowMind is:
- a strict pipeline
- with one brain (Director)
- one control (Dispatcher)
- and dumb execution modules

This guarantees:
- stability
- debuggability
- scalability
