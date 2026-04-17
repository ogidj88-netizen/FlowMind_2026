# FLOWMIND — DIRECTOR ENGINE v1

## 1. Purpose

Director Engine is the only creative planning engine in FlowMind.

Its job is to transform a validated script into a deterministic visual direction package that can be executed by downstream engines.

Director Engine does NOT execute production.
It defines:
- scene structure
- shot structure
- visual intent
- subtitle intent
- SFX intent
- music intent
- motion / transition intent
- normalized asset queries

Director Engine is the only allowed creative brain in the production contour.

---

## 2. Position in Pipeline

Director Engine runs after:
- TOPIC ENGINE
- SCRIPT ENGINE

Director Engine runs before:
- ASSET ENGINE
- ASSEMBLY ENGINE
- QA / PACKAGE ENGINE

Canonical phase:
- SCENES

---

## 3. Core Responsibility

Director Engine converts:
- validated script
- working promise
- style lock

into:
- scene plan
- shot schema compliant shot plan
- subtitle intent layer
- SFX intent layer
- music intent layer
- motion / transition preset intent
- normalized and realistic asset queries

Director Engine defines creative logic only.
It must not perform execution.

---

## 4. Inputs

Director Engine input contract:

### Required
- project_id
- topic contract
- working_promise
- style_lock
- script.txt
- script metrics

### Context Inputs
- previous_scene_context (optional for first scene)
- current_scene_context
- next_scene_context (optional for last scene)

### Constraints
- shot schema v1
- no abstract visual requests
- no style drift
- hook intensity requirements
- asset realism requirements

---

## 5. Outputs

Director Engine must produce the following artifacts:

### A. Scene Plan
Each scene must include:
- scene_id
- scene_role
- covered_script_segment
- scene_goal
- scene_emotion
- approximate_duration
- hook_flag (true/false)

### B. Shot Plan
Shot plan must conform to `FLOWMIND_SHOT_SCHEMA_V1.md`.

Every shot must include:
- shot_id
- timing object
- scene_role
- visual block
- text_overlay block
- audio_intent block
- constraints block

### C. Subtitle Intent Layer
For each relevant shot:
- subtitle enabled / disabled
- subtitle content
- subtitle style
- subtitle position

### D. SFX Intent Layer
For each relevant shot:
- whether SFX is needed
- type of accent
- strength / emphasis level

### E. Music Intent Layer
Per scene or segment:
- target energy
- emotional direction
- whether ducking is required
- whether rise / drop is needed

### F. Motion / Transition Intent
Per shot:
- motion preset
- transition in
- transition out
- emphasis preset if needed

### G. Normalized Asset Queries
Each shot must include:
- realistic searchable query
- optional fallback query
- no fantasy-only phrasing
- no abstract-only phrasing

---

## 6. Hard Rules

### Rule 1 — Full Script Coverage
100% of script must be mapped into scenes and shots.

No script block may remain visually unassigned.

### Rule 2 — Hook Priority
The first 15 seconds must be directed more aggressively than the rest of the video.

Minimum hook requirements:
- at least 3 shot changes
- at least 2 text overlays
- clear visual confirmation of hook promise

### Rule 3 — Realistic Visual Intent
Director Engine must only output visually feasible requests.

Allowed:
- realistic stock-searchable subjects
- concrete objects
- people, devices, environments, actions

Forbidden:
- symbolic-only visuals
- fantasy-only visuals
- metaphor-only prompts that cannot be sourced or generated safely

### Rule 4 — Style Lock Compliance
Every scene and shot must obey the project style lock.

No mixing of incompatible visual styles is allowed.

### Rule 5 — Query Normalization
Director Engine must think in meaning, but output in searchable form.

Each shot query must be:
- concise
- literal
- stock-search-friendly

### Rule 6 — No Execution Logic
Director Engine must not:
- pick final assets
- generate audio
- calculate final render instructions
- assemble subtitles into video
- render effects directly

### Rule 7 — No Auto-Correction of Upstream Failures
If script is weak or invalid, Director Engine must fail.
It must not rewrite the script internally.

---

## 7. Internal Layers

Director Engine may contain internal sublayers, but they are not separate core engines.

Allowed internal layers:
- Scene Decomposition Layer
- Shot Expansion Layer
- Hook Intensification Layer
- Subtitle Intent Layer
- SFX Intent Layer
- Music Intent Layer
- Motion / Transition Intent Layer
- Query Normalization Layer

These layers exist inside Director Engine only.

They must not create independent orchestration paths.

---

## 8. PASS Conditions

Director Engine passes only if all conditions are true:

1. Full script coverage exists
2. All scenes are concrete and usable
3. All shots comply with Shot Schema v1
4. Hook section meets minimum dynamics
5. All visual queries are realistic
6. Style lock is preserved
7. Subtitle intent exists where needed
8. SFX intent exists where needed
9. Music intent is coherent with scene emotion
10. No impossible shots are present

---

## 9. FAIL Conditions

Director Engine must fail if any of the following happens:

- scene plan is abstract
- shot plan violates shot schema
- visual queries are unrealistic
- hook section is visually weak
- style consistency is broken
- script coverage is incomplete
- scene durations are nonsensical
- intent layers contradict each other
- output is not executable by Asset Engine

---

## 10. Forbidden Behaviors

Director Engine is explicitly forbidden from:

- choosing concrete stock files
- choosing concrete SFX files
- choosing final music track
- rewriting script content
- modifying topic contract
- changing working promise
- changing dispatcher phase
- creating fallback artifacts
- bypassing Shot Schema
- bypassing style lock

---

## 11. Interface to Asset Engine

Director Engine hands off only structured intent.

Asset Engine is responsible for:
- resolving voice artifact
- resolving asset reality
- timing reconciliation
- repeat filtering
- final asset selection

Director Engine must never collapse into Asset Engine.

This separation is mandatory.

---

## 12. Interface to QA / Package Engine

Director Engine does not decide final quality alone.

QA / Package Engine later validates:
- whether hook was actually delivered
- whether visual flow stayed coherent
- whether packaging matches promise

Director Engine supplies the plan.
QA decides whether the result remained faithful.

---

## 13. Operating Principle

Director Engine is not a generator of random cinematic ideas.

Director Engine is a deterministic creative planner.

Its output must be:
- structured
- contract-bound
- style-bound
- executable
- debuggable

Without Director Engine:
- the system becomes random

Without strict Director boundaries:
- the system becomes unstable

Director Engine exists to preserve creative quality without destroying runtime stability.

---

## 14. Conclusion

Director Engine v1 is the single creative planning authority in FlowMind.

It transforms script into executable visual direction.

It does not execute.
It does not improvise outside contract boundaries.
It does not replace any downstream engine.

Its role is to make the system:
- visually coherent
- creatively directed
- operationally stable
- ready for deterministic execution
