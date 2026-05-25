# FLOWMIND CURRENT TO TARGET INTEGRATION MAP

Status: ACTIVE INTEGRATION MAP  
Project: FlowMind / Imagine What If  
Mode: DIRECTOR BRAIN MVP PREPARATION  
Target architecture: FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md  
Current anchor: FLOWMIND_CURRENT_WORK_ANCHOR.md

---

## 1. Purpose

This file maps the existing programmed FlowMind skeleton to the target FlowMind v2.1 architecture.

It answers:

- what already exists
- where each existing artifact belongs in the new 12-module target architecture
- what must be evolved
- what must not be rewritten
- where the first real implementation work starts
- how to avoid creating a second runtime contour

This file is not a new architecture.

It is a compatibility bridge between:

- current programmed skeleton
- target 12-module system

---

## 2. Core integration rule

The current skeleton remains the execution backbone.

The target architecture does not replace the current skeleton immediately.

We evolve the existing system by inserting the missing quality layers into the current flow.

Forbidden interpretation:

- do not create a second pipeline
- do not build 12 new empty module folders
- do not rewrite dispatcher
- do not rewrite runner
- do not activate legacy modules
- do not start upload or provider integrations

Correct interpretation:

- preserve current working skeleton
- add Director Brain MVP first
- prove improvement through render and review
- expand only after proof

---

## 3. Current programmed skeleton

The current skeleton already has a rough production path:

topic / input
-> script
-> script QA
-> scenes
-> assets
-> resolved assets
-> assembly
-> audio plan
-> audio render
-> audio loudness
-> final render
-> QA

This skeleton can produce:

- final_video.mp4

This proves technical execution exists.

It does not prove YouTube-quality video.

Target architecture v2.1 adds the missing media-quality layers.

---

## 4. Current skeleton mapped to target modules

| Current skeleton area | Existing / expected artifacts | Target module | Integration meaning |
|---|---|---|---|
| topic / manual input | manual topic, project context | Module 1 — Opportunity & Validation | Keep manual or semi-manual for now. Do not automate trends yet. |
| script | script.txt, script_meta.json | Module 3 — Script Writer | Keep current script flow. Improve later after Director Brain proof. |
| script QA | script_qa.json | Module 4 — Script QA & Validation | Keep current QA. Harden later. |
| scenes | scenes.json | Module 5 / 6 — Director Engine + Shot Planner | Main upgrade area. Current scenes are too coarse. |
| visual pacing | visual_pacing_plan.json | Module 7 — Visual Concept & Pacing | Reuse existing artifact name. Strengthen logic. |
| assets | assets.json | Module 9 — Asset System | Keep current asset path. Later map assets to shot_id. |
| resolved assets | resolved_assets.json | Module 9 — Asset System | Keep current resolver. Later validate against shot intent. |
| audio plan | audio_plan.json | Module 10 — Audio System | Keep current audio structure. Audio is not first bottleneck. |
| audio render | audio_render.json | Module 10 — Audio System | Keep current output. |
| audio loudness | audio_loudness_report.json | Module 10 — Audio System | Keep current validation. |
| assembly | assembly_plan.json | Module 11 — Assembly & Renderer | Must later read shot_list and visual_pacing_plan. |
| final render | final_video.mp4, final_render_report.json | Module 11 — Assembly & Renderer | Keep current renderer; evolve only as needed for Director Brain MVP. |
| QA | qa_report.json | Module 12 — Human Review & Quality Scorer | Current QA blocks upload. Later add quality scoring and review artifact. |

---

## 5. Existing skeleton interpretation

The current system is a rough output generator.

It is valuable because it already gives:

- project state
- artifacts
- audio
- render
- QA blocker
- local final video
- a baseline for comparison

It is not enough because it lacks:

- strong visual intent
- shot-level direction
- meaningful pacing
- asset-specific motion rules
- review loop based on biggest blocker

Therefore, the current system must be evolved, not replaced.

---

## 6. First integration target

The first integration target is:

Director Brain MVP

Minimum vertical slice:

script.txt
-> director_plan.json
-> shot_list.json
-> visual_pacing_plan.json
-> assembly / renderer
-> final_video.mp4
-> manual review

MVP modules involved:

- Module 5 — Director Engine
- Module 6 — Shot Planner / Scene Splitter
- Module 7 — Visual Concept & Pacing

Optional after MVP:

- Module 8 — Overlay & Text Planner

Overlay is useful, but it must not block the first Director Brain proof.

---

## 7. Required new artifacts for Director Brain MVP

The first real implementation should introduce or strengthen only these artifacts:

### director_plan.json

Purpose:

- define visual intent
- define emotional direction
- define scene purpose
- define pacing direction
- define asset intent

Must not be generic.

### shot_list.json

Purpose:

- split long scenes into shots
- map script segments to shots
- define shot timing
- define shot purpose
- define motion instruction
- define asset requirement hints

Must reduce PowerPoint/slideshow feeling.

### visual_pacing_plan.json

Purpose:

- define timing rules
- define shot pacing
- define motion rules by asset type
- define static limits
- define controlled reveal rules

Must be used by renderer.

A JSON artifact is not useful unless it is consumed downstream.

---

## 8. Renderer integration requirement

The biggest technical risk is renderer non-consumption.

Director Brain MVP is not complete if it only creates JSON.

Renderer / assembly must consume the new planning layer.

Minimum requirement:

- assembly/render logic must use shot_list.json or its derived data
- visual_pacing_plan.json must affect actual video output
- output video must visibly differ from baseline

If renderer cannot use the new plans, Director Brain MVP is not integrated.

---

## 9. Success criteria for first integration

Director Brain MVP is accepted only if:

1. director_plan.json exists and is not generic.
2. shot_list.json exists and contains timing, purpose, visual description, and motion instruction.
3. visual_pacing_plan.json exists and is consumed by renderer.
4. unjustified static segments above 12 seconds are reduced.
5. shot changes are meaningful, not random.
6. charts, dense cards, and infographics remain readable.
7. manual review scores video as less PowerPoint-like by at least +2/10.
8. final_video.mp4 exists after the integration run.
9. if the video is not visibly better, MVP is not accepted even if JSON files are valid.

---

## 10. What not to change during first integration

Do not change:

- dispatcher architecture
- runner architecture
- upload gate
- YouTube upload logic
- Telegram integration
- provider integrations
- full Market Intelligence automation
- current audio pipeline unless required by renderer timing
- current asset system beyond what Director Brain MVP requires

Do not create:

- 12 empty module folders
- a parallel runtime
- a second state model
- fake module shells
- production placeholders

---

## 11. Target module implementation order

Do not build modules in numeric order.

Correct implementation order:

1. Module 5 — Director Engine
2. Module 6 — Shot Planner / Scene Splitter
3. Module 7 — Visual Concept & Pacing
4. Module 11 — Assembly & Renderer integration for new plans
5. Module 12 — minimal manual review / quality comparison
6. Module 8 — Overlay & Text Planner
7. Module 2 — Hook & Retention Architect
8. Module 4 — Script QA & Validation
9. Module 9 — Asset System hardening
10. Module 10 — Audio System hardening
11. Module 1 — Opportunity & Validation automation

Deferred:

- Publish Package
- Upload
- Telegram
- thumbnails
- multi-provider asset routing

---

## 12. Integration decision rules

After Director Brain MVP render:

If video is visibly better:

- keep the integration
- proceed to Overlay or Hook/Retention layer

If video is not visibly better:

- do not proceed to other modules
- revise Director Engine / Shot Planner / Pacing
- do not blame Asset System or Market Intelligence before proving Director Brain

If renderer cannot consume the new artifacts:

- pause creative work
- fix renderer integration only to the minimum required level

If output becomes less readable:

- reduce motion
- add controlled reveal
- protect dense cards and charts

---

## 13. Relationship to target architecture

FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md defines where FlowMind is going.

This file defines how the current skeleton connects to that target.

FLOWMIND_CURRENT_WORK_ANCHOR.md defines what is active right now.

Use all three:

1. TARGET_ARCHITECTURE = destination
2. CURRENT_WORK_ANCHOR = current operating state
3. CURRENT_TO_TARGET_INTEGRATION_MAP = bridge from current code to target system

If these files conflict, stop and reconcile before coding.

---

## 14. Final summary

Current skeleton is not thrown away.

It remains the execution backbone.

The first real upgrade is Director Brain MVP.

The first proof is not a document.

The first proof is a new render that looks less like a PowerPoint slideshow.

End.
