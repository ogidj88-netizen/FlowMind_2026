# FLOWMIND TARGET ARCHITECTURE V2.1 — 12 MODULES

Status: FINAL TARGET ARCHITECTURE
Project: FlowMind / Imagine What If
Version: 2.1
Mode: TARGET SYSTEM MAP
Original date: 2026-05-25
Authority reconciliation update: 2026-09-18
Scope: detailed target architecture only; no current operational authority; not runtime proof

---

## 1. Purpose

This document defines the target architecture FlowMind is evolving toward.

It answers:

- what system we are building
- why the current skeleton is not enough
- why the 27-module version is preserved only as a capability map
- why the 12-module version is the accepted implementation structure
- which capabilities from the 27-module map are preserved
- which architectural areas are expected to matter most for quality
- what scope is intentionally deferred

This document is not runtime proof.

A module exists only after:

- implementation
- validation
- artifact output
- downstream consumption
- runtime evidence

This document is the source of truth for FlowMind target architecture v2.1 only.

It does not define:

- current project state
- current next action
- current allowed work
- current implementation sequence
- current runtime truth

It must not override:

- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
- FLOWMIND_ACTIVE_MAP.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- verified dispatcher/control specifications within their scope
- newer verified repo or runtime evidence

Operational priority always comes from the verified active authority chain.

Historical implementation-priority statements in older versions of this document must not be interpreted as current authorization.

---

## 2. Core Truth

27 modules = Capability Map.

This means the original 27-module structure listed the important functions and questions the system must eventually handle.

12 modules = Implementation Structure.

This means those capabilities are consolidated into fewer, stronger, more practical modules.

We are not deleting the important capabilities from the 27-module map.

We are packaging them into 12 modules to avoid:

- orchestration hell
- excessive artifact sprawl
- slow development
- fake architectural progress
- polishing structure instead of improving video output

FlowMind must not remain a primitive chain:

topic -> script -> images -> voiceover -> video

FlowMind must evolve toward:

opportunity -> hook -> retention -> script -> director plan -> shots -> assets -> audio -> render -> quality review -> human decision

Director Brain is a principal target quality driver.

This is an architectural statement, not a current operational instruction.

---

## 3. Design Baseline vs Target System

### Historical design baseline

At the time the original architecture was drafted, the system was described as having a rough 12-step execution skeleton and being capable of producing a local:

- final_video.mp4

That description is retained only as historical design context.

It must not be treated as current runtime proof.

Current implementation state must be established from current repo and runtime evidence.

### Target system

Target FlowMind v2.1 is:

- 12 modules
- 7 layers
- 27 capabilities preserved
- artifact-based
- dispatcher-controlled
- director-led
- review-gated
- quality-improvement oriented

The migration principle is:

evolve the verified execution backbone rather than rewriting the entire system without evidence.

If current runtime evidence shows that an older backbone assumption is no longer valid, runtime evidence wins.

---

## 4. Mapping: 27 Capabilities -> 12 Modules

| 27-module capability group | Implemented in v2.1 | Module |
|---|---|---:|
| Signal Scanner, Source Collector, Trend Freshness, Topic Evaluator, Audience Pain, Angle Engine, Business Gate | Opportunity & Validation | 1 |
| Hook Engine, Retention Architect | Hook & Retention Architect | 2 |
| Script Writer | Script Writer | 3 |
| Script Editorial QA, Fact/Risk QA | Script QA & Validation | 4 |
| Director Engine | Director Engine | 5 |
| Shot Planner | Shot Planner / Scene Splitter | 6 |
| Visual Concept Engine, Visual Pacing Engine | Visual Concept & Pacing | 7 |
| Overlay / On-screen Text Planner | Overlay & Text Planner | 8 |
| Asset Requirement Planner, Asset Source Router, Asset Resolver, License QA | Asset System | 9 |
| Voice Strategy, Audio Planner, Audio Renderer, Loudness QA | Audio System | 10 |
| Assembly Planner, Renderer, Render QA | Assembly & Renderer | 11 |
| Human Review, Biggest Blocker | Human Review & Quality Scorer | 12 |
| Publish Package | Deferred until consistently watchable output and explicit approval workflow | - |

---

## 5. Final Module Structure

The Priority column below describes architectural importance for the target system.

It does not define the current implementation order.

| No. | Module | Layer | Main responsibility | Key output | Priority |
|---:|---|---|---|---|---|
| 1 | Opportunity & Validation | Strategy | Topic, evidence, pain, angle, business verdict, basic risk check | opportunity_brief.json + source/evidence section | Low / semi-manual |
| 2 | Hook & Retention Architect | Editorial Brain | Hook, retention map, first retention heatmap | hook_pack.json + retention_map.json | High |
| 3 | Script Writer | Editorial Brain | Voice-over script | script.txt + script_meta.json | Medium |
| 4 | Script QA & Validation | Editorial Brain | Editorial QA + fact/risk QA | script_qa.json | High |
| 5 | Director Engine | Director Brain | Visual and emotional direction | director_plan.json | Critical |
| 6 | Shot Planner / Scene Splitter | Director Brain | Split scenes into shots | shot_list.json | Critical |
| 7 | Visual Concept & Pacing | Director Brain | Style, motion rules, pacing, anti-slideshow logic | visual_concept.json + visual_pacing_plan.json | Critical |
| 8 | Overlay & Text Planner | Director Brain | On-screen emphasis, numbers, callouts | overlay_plan.json | High |
| 9 | Asset System | Asset System | Asset requirements, resolving, format/license QA | asset_requirements.json + resolved_assets.json | Medium |
| 10 | Audio System | Audio System | Voice, audio planning, render, loudness QA | audio_plan.json + audio_render.json + audio_loudness_report.json | Medium |
| 11 | Assembly & Renderer | Production | Timeline, final render, technical render QA | final_video.mp4 + final_render_report.json | Medium |
| 12 | Human Review & Quality Scorer | Review & Improvement | Automatic scoring + human review + biggest blocker | video_quality_score.json + human_review_verdict.json | High |

---

## 6. Director Brain Architectural Priority

Within the target architecture, Director Brain is expected to be a high-impact quality area.

It includes:

- Module 5 — Director Engine
- Module 6 — Shot Planner / Scene Splitter
- Module 7 — Visual Concept & Pacing
- Module 8 — Overlay & Text Planner

This architectural priority does not authorize implementation.

Current implementation sequencing must come from FLOWMIND_ACTIVE_MAP.md and the verified authority chain.

When production implementation is explicitly authorized, a Director Brain MVP may use the target flow:

script -> director_plan.json -> shot_list.json -> visual_pacing_plan.json -> render -> review

The target quality goal is to reduce PowerPoint/slideshow feeling through:

- shorter meaningful shots
- clearer visual intent
- better shot variety
- asset-specific motion rules
- controlled reveal for information cards

Overlay may be deferred from the first Director Brain proof if the active implementation plan explicitly allows it.

---

## 7. Future Director Brain MVP Definition of Done

If and when Director Brain implementation is authorized by the current operational authority, its MVP acceptance criteria are:

1. director_plan.json is not generic and contains concrete visual intent.
2. shot_list.json contains timing, purpose, visual description, and motion instruction.
3. visual_pacing_plan.json is actually used by the renderer.
4. Unjustified static segments above 12 seconds are reduced.
5. Shot changes are meaningful, not random.
6. Charts, dense cards, and infographics do not become less readable.
7. Manual review scores the video as less PowerPoint-like by at least +2/10.
8. If the video is not visibly better, the MVP is not accepted even if all JSON files are valid.

These are future target acceptance criteria.

They are not a current next action.

---

## 8. Retention Heatmap

Retention Heatmap is not a separate module in target architecture v2.1.

It is a supporting artifact used across the system.

Target lifecycle:

1. Planned retention:
   generated in Module 2 — Hook & Retention Architect.

2. Directed retention:
   updated or checked inside Director Brain.

3. Post-render retention risk:
   reviewed in Module 12 — Human Review & Quality Scorer.

Artifact:

- retention_heatmap.json

Rule:

Do not create a separate Retention Heatmap module in the v2.1 target structure.

---

## 9. Non-Negotiable Target Architecture Rules

1. Evolve verified working structure instead of performing an unsupported full rewrite.
2. No new parallel runtime contour.
3. No activation of legacy modules without explicit audit.
4. No upload automation before consistently watchable output and explicit approval.
5. No full in-memory rewrite of critical artifact flow.
6. Critical artifacts must remain inspectable on disk where contracts require them.
7. Internal sub-steps may be in-memory inside a module when this does not break artifact contracts.
8. No blind Ken Burns behavior on all assets.
9. Motion must depend on asset type and content role.
10. Each implemented module must produce visible improvement or a measurable blocker report.
11. When output-affecting work is authorized, major changes must be followed by render and review.
12. Commit only after meaningful validated work blocks.
13. Do not attempt all 12 modules as one implementation block.
14. No production placeholders, stubs, or fake output.
15. If a module has no verified input/output contract, it is not operationally real.

These are target architecture constraints.

They do not define the current work step.

---

## 10. Deferred Target Scope

The following capabilities are intentionally outside the immediate target architecture path unless separately authorized by the current operational authority:

- full Opportunity Engine automation
- external trend scraping
- multi-provider asset routing
- YouTube upload
- Telegram integration
- publish package
- thumbnail automation
- full business ROI automation
- runner rewrite
- dispatcher rewrite
- creation of empty module folders without implementation value

Deferred scope does not mean permanently forbidden.

It means these items must not become active merely because they appear in historical plans.

Current authorization must come from the verified authority chain.

---

## 11. Architectural Sequencing Note

The target architecture expects the Director Brain area to provide one of the earliest major quality improvements once production implementation is authorized.

That expectation is architectural, not operational.

It must not be interpreted as:

- the current project step
- automatic permission to implement Director Brain
- permission to change renderer behavior
- permission to bypass authority/source reconciliation
- permission to skip runtime verification

When FLOWMIND_ACTIVE_MAP.md eventually authorizes production implementation, the operational plan may select Director Brain or another verified blocker based on current evidence.

Architecture suggests direction.

The Active Map selects current work.

---

## 12. Relationship With Current Operational Authority

FLOWMIND_ACTIVE_MAP.md defines:

- where we are now
- current allowed work
- current forbidden work
- current next operational step
- current exit conditions

This file defines:

- where the target architecture is going
- the accepted 12-module structure
- target responsibilities
- target artifacts
- architectural constraints

FLOWMIND_CURRENT_WORK_ANCHOR.md is FROZEN LEGACY.

It must not define current operating state or current next action.

Historical work anchors may be used only as historical evidence.

If target architecture and current operational authority materially conflict:

STOP.

Reconcile the conflict through:

- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_ACTIVE_MAP.md
- current repo and runtime evidence
- explicit user decision when required

Do not silently choose an older next action.

---

## 13. Final Summary

FlowMind v2.1 target is:

- 12 modules
- 7 layers
- 27 capabilities preserved
- artifact-based
- director-led
- review-gated
- no premature upload
- no overbuilt market automation
- no blind motion
- no second runtime contour

Director Brain remains an important target quality driver.

It is not automatically the current next action.

Current implementation work must always come from the verified current operational authority.

Target architecture defines destination.

Active Map defines where we work now.

Runtime evidence defines what actually exists.

End.
