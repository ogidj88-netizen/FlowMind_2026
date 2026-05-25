# FLOWMIND TARGET ARCHITECTURE V2.1 — 12 MODULES

Status: FINAL TARGET ARCHITECTURE  
Project: FlowMind / Imagine What If  
Version: 2.1  
Mode: TARGET SYSTEM MAP  
Date: 2026-05-25

---

## 1. Purpose

This document defines the target architecture FlowMind is evolving toward.

It answers:

- what system we are building
- why the current skeleton is not enough
- why the 27-module version is preserved only as a capability map
- why the 12-module version is the accepted implementation structure
- which capabilities from the 27-module map are preserved
- which modules matter first
- what must not be built yet

This document is not runtime proof.

A module exists only after:

- implementation
- validation
- artifact output
- downstream consumption
- runtime evidence

This document is the source of truth for FlowMind target architecture v2.1 only.

It does not override:

- active project instructions
- source-of-truth registry
- dispatcher/control specs
- current work anchor
- runtime evidence

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

FlowMind must evolve into:

opportunity -> hook -> retention -> script -> director plan -> shots -> assets -> audio -> render -> quality review -> human decision

Director Brain is the main quality driver.

---

## 3. Current System vs Target System

### Current system

The current system has a rough 12-step execution skeleton.

It can already produce a local:

- final_video.mp4

This proves the pipeline can technically generate a reviewable file.

It does not prove the system can consistently create strong YouTube-style content.

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

The current skeleton remains the execution backbone.

We evolve it.

We do not rewrite everything.

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

## 6. Director Brain Priority

Director Brain is the first implementation priority.

It includes:

- Module 5 — Director Engine
- Module 6 — Shot Planner / Scene Splitter
- Module 7 — Visual Concept & Pacing
- Module 8 — Overlay & Text Planner

The first MVP may exclude Overlay if it slows the first proof.

The first MVP target is:

script -> director_plan.json -> shot_list.json -> visual_pacing_plan.json -> render -> review

Goal:

Reduce PowerPoint/slideshow feeling by creating:

- shorter meaningful shots
- clearer visual intent
- better shot variety
- asset-specific motion rules
- controlled reveal for information cards

---

## 7. Director Brain MVP Definition of Done

Director Brain MVP is accepted only if:

1. director_plan.json is not generic and contains concrete visual intent.
2. shot_list.json contains timing, purpose, visual description, and motion instruction.
3. visual_pacing_plan.json is actually used by the renderer.
4. Unjustified static segments above 12 seconds are reduced.
5. Shot changes are meaningful, not random.
6. Charts, dense cards, and infographics do not become less readable.
7. Manual review scores the video as less PowerPoint-like by at least +2/10.
8. If the video is not visibly better, the MVP is not accepted even if all JSON files are valid.

---

## 8. Retention Heatmap

Retention Heatmap is not a separate module.

It is a supporting artifact used across the system.

Lifecycle:

1. Planned retention:
   generated in Module 2 — Hook & Retention Architect.

2. Directed retention:
   updated or checked inside Director Brain.

3. Post-render retention risk:
   reviewed in Module 12 — Human Review & Quality Scorer.

Artifact:

- retention_heatmap.json

Rule:

Do not create a separate Retention Heatmap module now.

---

## 9. Non-Negotiable Rules

1. Current skeleton remains the execution backbone.
2. No new parallel runtime contour.
3. No activation of legacy modules.
4. No upload automation before consistently watchable output.
5. No full in-memory rewrite.
6. Critical artifacts must remain on disk.
7. Internal sub-steps may be in-memory only inside a module.
8. No blind Ken Burns on all assets.
9. Motion must depend on asset type and content role.
10. Each new module must produce visible improvement or a measurable blocker report.
11. After each major output-affecting change: render and review the video.
12. Commit only after meaningful work blocks.
13. Do not build all 12 modules at once.
14. No production placeholders, stubs, or fake output.
15. If a module has no input/output contract, it is not real.

---

## 10. Deferred Scope

Do not build now:

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
- 12 empty module folders

---

## 11. Current Immediate Implementation Target

The next real implementation target is not Market Intelligence and not upload.

The next real target is:

Director Brain MVP:

- Director Engine
- Shot Planner / Scene Splitter
- Visual Concept & Pacing

Success criterion:

A new rendered video must look visibly more dynamic than the current baseline.

If Director Brain MVP does not improve the video, do not continue to the next modules.

Fix Director Brain first.

---

## 12. Relationship With Current Work Anchor

FLOWMIND_CURRENT_WORK_ANCHOR.md defines where we are now.

This file defines where we are going.

Use both:

- CURRENT_WORK_ANCHOR = current operating state
- TARGET_ARCHITECTURE_V2_12_MODULES = destination

If they conflict, stop and reconcile before coding.

---

## 13. Final Summary

FlowMind v2.1 target is:

- 12 modules
- 7 layers
- 27 capabilities preserved
- artifact-based
- director-first
- review-gated
- no premature upload
- no overbuilt market automation
- no blind motion
- no second runtime contour

The first quality leap must come from Director Brain, not from more infrastructure.

End.
