# FLOWMIND CURRENT WORK ANCHOR

Status: ACTIVE WORK ANCHOR  
Project: FlowMind / Imagine What If  
Mode: DIRECTOR BRAIN MVP PREPARATION  
Branch: cashflow-mode

---

## 1. Purpose

This file defines the current working position for FlowMind.

It answers:

- where we are now
- what we are doing next
- what is forbidden now
- what file defines the destination
- how the current skeleton connects to the target architecture

This file is the current operating anchor.

It does not replace the target architecture.

Destination map:

- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

Integration map:

- FLOWMIND_CURRENT_TO_TARGET_INTEGRATION_MAP.md

---

## 2. Current confirmed state

Active project:

- projects/P2026_TEST_001

Current known output:

- projects/P2026_TEST_001/final_render/final_video.mp4

Current state interpretation:

- the current skeleton can create a local final video
- the output is reviewable
- the system is not upload-ready
- QA is expected to block upload readiness
- current quality is not considered production YouTube quality

Upload remains closed.

---

## 3. Current operating mode

Current mode:

DIRECTOR BRAIN MVP PREPARATION

Meaning:

We are no longer doing broad system-map audit by default.

We are preparing the first quality-improvement vertical slice:

script
-> director_plan.json
-> shot_list.json
-> visual_pacing_plan.json
-> render
-> review

Goal:

Reduce PowerPoint/slideshow feeling in the final video.

---

## 4. Target architecture

Target architecture file:

- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

Target system:

- 12 modules
- 7 layers
- 27 capabilities preserved
- current skeleton remains execution backbone
- Director Brain is first implementation priority

Important interpretation:

The 12-module architecture is not a rewrite.

It is a destination map for evolving the current skeleton.

---

## 5. Current implementation target

Current implementation target:

Director Brain MVP

Included:

- Module 5 — Director Engine
- Module 6 — Shot Planner / Scene Splitter
- Module 7 — Visual Concept & Pacing

Optional after MVP:

- Module 8 — Overlay & Text Planner

MVP output expectation:

- director_plan.json
- shot_list.json
- visual_pacing_plan.json
- new final render
- manual review result

---

## 6. Definition of Done for Director Brain MVP

Director Brain MVP is accepted only if:

1. director_plan.json is not generic and contains concrete visual intent.
2. shot_list.json contains timing, purpose, visual description, and motion instruction.
3. visual_pacing_plan.json is actually used by the renderer.
4. unjustified static segments above 12 seconds are reduced.
5. shot changes are meaningful, not random.
6. charts, dense cards, and infographics do not become less readable.
7. manual review scores the video as less PowerPoint-like by at least +2/10.
8. if the video is not visibly better, the MVP is not accepted even if all JSON files are valid.

---

## 7. Forbidden now

Do not:

- create 12 empty module folders
- rewrite the runner
- rewrite the dispatcher
- activate engine/module_runner.py
- execute engine/modules/*
- add Telegram integration
- add YouTube upload
- add Pexels/Pixabay integration
- add new provider integrations
- open upload gate
- move to READY_FOR_UPLOAD
- approve upload
- create publish package
- create thumbnail automation
- build full Market Intelligence automation
- build all 12 modules at once
- commit after every small edit

---

## 8. Commit rule

Commit only after the full documentation block is complete and validated.

Current documentation block contains:

1. FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md
2. FLOWMIND_CURRENT_WORK_ANCHOR.md
3. FLOWMIND_CURRENT_TO_TARGET_INTEGRATION_MAP.md

After all three files exist:

- inspect files
- run preflight
- inspect git status
- commit once
- push once

---

## 9. Current next action

Create or update:

- FLOWMIND_CURRENT_TO_TARGET_INTEGRATION_MAP.md

Purpose:

Map the existing programmed skeleton to the target 12-module architecture.

This prevents rewriting the system or creating a second active contour.

---

## 10. Stop rule

Stop if:

- the next action creates a second runtime contour
- the next action activates legacy modules
- the next action touches upload
- the next action rewrites runner/dispatcher before integration proof
- the next action creates fake progress without improving output
- the target architecture and current anchor conflict

End.
