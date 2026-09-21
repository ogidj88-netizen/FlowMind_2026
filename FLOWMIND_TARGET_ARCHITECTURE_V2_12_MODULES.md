# FLOWMIND TARGET ARCHITECTURE V2.2 — 12 MODULES

Status: FINAL TARGET ARCHITECTURE
Project: FlowMind / Imagine What If
Version: 2.2
Mode: TARGET SYSTEM MAP
Original date: 2026-05-25
Authority reconciliation update: 2026-09-18
Architecture evolution update: 2026-09-21
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
- how FlowMind separates its own decision intelligence from external AI execution providers
- how monetization and real performance feedback are expected to influence future decisions
- what scope is intentionally deferred

This document is not runtime proof.

A module exists only after:

- implementation
- validation
- artifact output
- downstream consumption
- runtime evidence

This document is the source of truth for FlowMind target architecture v2.2 only.

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
- polishing structure instead of improving business and content output

FlowMind must not remain a primitive chain:

topic -> script -> images -> voiceover -> video

FlowMind must evolve toward:

opportunity
-> business potential
-> hook
-> retention
-> script
-> director plan
-> production execution
-> quality review
-> publication decision
-> performance data
-> monetization data
-> next decision

FlowMind is not intended to become its own foundation model, video generator, TTS engine, image generator, search engine, analytics platform, or distribution platform.

FlowMind is the decision and orchestration intelligence above those capabilities.

External systems provide capabilities.

FlowMind decides:

- what should be done
- why it should be done
- which capability is required
- which provider should execute it
- whether the result is acceptable
- whether the result should move forward
- what the real-world outcome was
- what the system should do differently next time

Director Brain remains an important target quality driver.

Business and monetization intelligence become cross-cutting target concerns across the architecture.

These are architectural statements, not current operational instructions.

---

## 3. FlowMind Brain

The FlowMind Brain is not one AI model.

It is not ChatGPT.

It is not Claude.

It is not Gemini.

It is not one Python file.

It is the combined decision layer formed by:

- canonical state
- dispatcher/control logic
- module contracts
- decision rules
- model calls
- provider selection
- validation
- scoring
- memory
- performance feedback
- monetization feedback

External AI models are replaceable reasoning or generation engines used by the Brain.

The FlowMind Brain owns the workflow logic.

A provider does not own the workflow.

Target principle:

FlowMind owns the decision.
External providers execute capabilities.

This means a future provider change should ideally affect an adapter or provider configuration, not force a redesign of the entire pipeline.

---

## 4. Provider Abstraction Principle

AI and media providers must be treated as replaceable execution providers wherever economically and technically reasonable.

Examples may include:

- language/reasoning models
- search and research providers
- trend/data providers
- image generation providers
- video generation providers
- TTS providers
- music/audio providers
- stock media providers
- render infrastructure
- analytics sources

No named provider is permanent architecture authority.

Provider-specific code should be isolated behind a capability contract where practical.

Target pattern:

FlowMind module
-> capability contract
-> provider adapter
-> external provider
-> normalized result
-> validation
-> downstream artifact

Examples:

Script Writer
-> text-generation capability
-> selected LLM provider
-> script artifact

Audio System
-> speech-generation capability
-> selected TTS provider
-> normalized audio artifact

Asset System
-> visual-generation or asset-resolution capability
-> selected provider
-> normalized asset artifact

The target architecture must allow provider substitution without rewriting unrelated modules.

Provider selection may eventually consider:

- output quality
- cost
- latency
- reliability
- language
- format
- commercial usage rights
- quota
- task suitability

Dynamic automatic provider routing is a future capability.

The architectural boundary should support it.

This document does not authorize building every provider adapter now.

---

## 5. Monetization-First Decision Principle

FlowMind is not optimized for maximum content volume.

It is optimized for economically useful content decisions.

The target system must increasingly evaluate opportunities through signals such as:

- audience demand
- competitive pressure
- expected attention
- retention potential
- advertiser value
- affiliate potential
- sponsor fit
- product fit
- content production cost
- expected return
- observed return

Early versions may use incomplete or proxy signals.

The long-term target is a closed decision loop:

market signal
-> opportunity decision
-> content
-> distribution
-> audience response
-> revenue response
-> learning
-> next decision

The objective is not:

make more videos.

The objective is:

allocate production effort toward content with the highest expected economic value under current evidence.

This does not mean every individual video must directly generate revenue.

Some content may serve:

- audience acquisition
- authority building
- funnel entry
- retargeting
- experimentation
- strategic learning

The system should distinguish these roles explicitly when sufficient data exists.

---

## 6. Feedback and Decision Memory

FlowMind should eventually retain structured evidence about:

- topic
- angle
- hook
- script structure
- visual strategy
- provider choices
- production cost
- publication timing
- thumbnail/title decisions
- impressions
- CTR
- retention
- watch time
- subscribers
- affiliate events
- leads
- sales
- revenue
- ROI

The purpose is not to create a generic memory database.

The purpose is to answer increasingly useful questions such as:

- Which topics create useful attention?
- Which hooks produce retention?
- Which content formats produce revenue?
- Which providers give the best quality-to-cost ratio?
- Which decisions repeatedly underperform?
- Which content characteristics correlate with business outcomes?
- What should be tested next?

Historical performance must be treated as evidence, not absolute truth.

The system must remain capable of exploration because market conditions change.

Decision memory is a target capability.

Its current runtime status must be established separately through repository and runtime evidence.

---

## 7. Autonomy Target

The long-term target is high operational autonomy.

The system should eventually be capable of:

- collecting signals
- generating candidate opportunities
- rejecting weak opportunities
- selecting a production target
- selecting suitable providers
- producing required artifacts
- validating output
- rendering content
- collecting performance data
- comparing predicted and actual performance
- improving future decisions

Human approval should remain available for:

- irreversible external actions
- publication when required by release policy
- high-risk claims
- high-cost actions
- major strategic changes
- situations where confidence is insufficient

Autonomy does not mean removing safeguards.

Autonomy means reducing unnecessary human intervention while preserving control at consequential boundaries.

---

## 8. Internal-First, Product-Capable Architecture

FlowMind is built first as an internal operating system for our own media production.

The first commercial proof must come from using the system ourselves.

The architecture should nevertheless avoid decisions that unnecessarily prevent later use as:

- managed content intelligence service
- internal business tool
- agency operating system
- licensed platform
- SaaS product

Productization is not part of the immediate implementation scope.

Future external commercialization may require substantial additional work including:

- authentication
- tenant isolation
- billing
- onboarding
- permissions
- UI
- observability
- support
- compliance
- security hardening
- customer-specific integrations

Those concerns must not be prematurely added to the current internal system.

Target principle:

build the internal intelligence so that later productization is possible without rebuilding the core decision logic from zero.

---

## 9. Design Baseline vs Target System

### Historical design baseline

At the time the original architecture was drafted, the system was described as having a rough 12-step execution skeleton and being capable of producing a local:

- final_video.mp4

That description is retained only as historical design context.

It must not be treated as current runtime proof.

Current implementation state must be established from current repo and runtime evidence.

### Target system

Target FlowMind v2.2 is:

- 12 modules
- 7 layers
- 27 capabilities preserved
- artifact-based
- dispatcher-controlled
- provider-abstracted
- director-led
- review-gated
- monetization-aware
- feedback-driven
- designed for increasing autonomy

The migration principle is:

evolve the verified execution backbone rather than rewriting the entire system without evidence.

If current runtime evidence shows that an older backbone assumption is no longer valid, runtime evidence wins.

---

## 10. Mapping: 27 Capabilities -> 12 Modules

| 27-module capability group | Implemented in v2.2 | Module |
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

Provider abstraction, business scoring, decision memory, and performance feedback are cross-cutting architecture concerns.

They do not require separate top-level modules merely to exist conceptually.

---

## 11. Final Module Structure

The Priority column below describes architectural importance for the target system.

It does not define the current implementation order.

| No. | Module | Layer | Main responsibility | Key output | Priority |
|---:|---|---|---|---|---|
| 1 | Opportunity & Validation | Strategy | Market opportunity, evidence, audience pain, angle, business potential, risk | opportunity_brief.json + source/evidence section | Critical |
| 2 | Hook & Retention Architect | Editorial Brain | Hook, retention map, first retention heatmap | hook_pack.json + retention_map.json | High |
| 3 | Script Writer | Editorial Brain | Voice-over script | script.txt + script_meta.json | Medium |
| 4 | Script QA & Validation | Editorial Brain | Editorial QA + fact/risk QA | script_qa.json | High |
| 5 | Director Engine | Director Brain | Visual and emotional direction | director_plan.json | Critical |
| 6 | Shot Planner / Scene Splitter | Director Brain | Split scenes into shots | shot_list.json | Critical |
| 7 | Visual Concept & Pacing | Director Brain | Style, motion rules, pacing, anti-slideshow logic | visual_concept.json + visual_pacing_plan.json | Critical |
| 8 | Overlay & Text Planner | Director Brain | On-screen emphasis, numbers, callouts | overlay_plan.json | High |
| 9 | Asset System | Asset System | Asset requirements, provider execution, resolving, format/license QA | asset_requirements.json + resolved_assets.json | Medium |
| 10 | Audio System | Audio System | Voice strategy, provider execution, audio planning, render, loudness QA | audio_plan.json + audio_render.json + audio_loudness_report.json | Medium |
| 11 | Assembly & Renderer | Production | Timeline, final render, technical render QA | final_video.mp4 + final_render_report.json | Medium |
| 12 | Human Review & Quality Scorer | Review & Improvement | Automatic scoring + human review + biggest blocker | video_quality_score.json + human_review_verdict.json | High |

---

## 12. Director Brain Architectural Priority

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

## 13. Future Director Brain MVP Definition of Done

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

## 14. Retention Heatmap

Retention Heatmap is not a separate module in target architecture v2.2.

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

Do not create a separate Retention Heatmap module in the v2.2 target structure.

---

## 15. Non-Negotiable Target Architecture Rules

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
16. No external AI provider becomes permanent architecture authority.
17. Provider-specific behavior should remain behind a stable capability boundary where practical.
18. Do not rebuild capabilities that can be reliably purchased from stronger external providers without a verified strategic reason.
19. FlowMind must preserve ownership of decision logic, state, validation, and feedback.
20. Monetization data must inform future decisions when reliable data becomes available.
21. More content is not automatically better; production effort must increasingly follow expected economic value.
22. A provider replacement must not require rewriting unrelated modules.
23. Productization concerns must not pollute the internal MVP before commercial evidence exists.
24. Human approval remains available at irreversible, high-risk, or low-confidence boundaries.

These are target architecture constraints.

They do not define the current work step.

---

## 16. Deferred Target Scope

The following capabilities are intentionally outside the immediate target architecture path unless separately authorized by the current operational authority:

- full Opportunity Engine automation
- full external trend scraping
- automatic multi-provider routing
- automated provider benchmarking
- automated cost-quality optimization across providers
- YouTube upload
- Telegram integration
- publish package
- thumbnail automation
- full business ROI automation
- full decision-memory optimization
- autonomous reinforcement or self-modification
- customer-facing SaaS
- multi-tenant infrastructure
- billing
- customer onboarding
- runner rewrite
- dispatcher rewrite
- creation of empty module folders without implementation value

Deferred scope does not mean permanently forbidden.

It means these items must not become active merely because they appear in target architecture.

Provider abstraction itself is not deferred.

Automatic provider routing is deferred until current production evidence justifies it.

Current authorization must come from the verified authority chain.

---

## 17. Architectural Sequencing Note

The target architecture expects several areas to become major long-term value drivers:

- Opportunity & Validation
- Hook & Retention
- Director Brain
- quality review
- provider abstraction
- performance feedback
- monetization feedback

This expectation is architectural, not operational.

It must not be interpreted as:

- the current project step
- automatic permission to implement Director Brain
- automatic permission to build monetization automation
- permission to add multiple providers immediately
- permission to change renderer behavior
- permission to bypass authority/source reconciliation
- permission to skip runtime verification

When FLOWMIND_ACTIVE_MAP.md authorizes production implementation, the operational plan must select work based on current evidence and ROI.

Architecture suggests direction.

The Active Map selects current work.

---

## 18. Relationship With Current Operational Authority

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
- provider abstraction
- FlowMind Brain principles
- monetization and feedback direction
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

## 19. Final Summary

FlowMind v2.2 target is:

- 12 modules
- 7 layers
- 27 capabilities preserved
- FlowMind-controlled decision intelligence
- replaceable external AI providers
- stable capability contracts
- artifact-based
- dispatcher-controlled
- director-led
- review-gated
- monetization-aware
- feedback-driven
- designed for increasing autonomy
- internal-first
- product-capable later
- no premature SaaS complexity
- no premature upload automation
- no blind motion
- no second runtime contour

FlowMind is the brain above external execution providers.

It should own:

- decisions
- state
- orchestration
- validation
- learning signals
- business objectives

It should buy or call commodity capabilities when external systems can provide them better.

Director Brain remains an important target quality driver.

Opportunity selection and monetization feedback become equally important long-term intelligence areas.

None of these principles automatically define the current next action.

Current implementation work must always come from the verified current operational authority.

Target architecture defines destination.

Active Map defines where we work now.

Runtime evidence defines what actually exists.

Business outcomes determine whether the system creates value.

End.