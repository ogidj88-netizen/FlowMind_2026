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
- which file-edit protocol is mandatory

This file is the current operating anchor.

It does not replace the target architecture.

Destination map:

- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

Integration map:

- FLOWMIND_CURRENT_TO_TARGET_INTEGRATION_MAP.md

File edit protocol:

- FLOWMIND_FILE_EDIT_PROTOCOL.md

Implementation decision:

- FLOWMIND_DIRECTOR_BRAIN_MVP_INTEGRATION_DECISION.md

---

## 2. Mandatory file edit protocol

All file modifications in FlowMind must follow:

- FLOWMIND_FILE_EDIT_PROTOCOL.md

Mandatory rule:

Full file replacement only.

Allowed edit methods:

1. nano
2. direct cat input using cat > path/to/file

Forbidden:

- heredoc
- cat << EOF
- cat <<'EOF'
- partial edits
- patch-style edits
- sed -i
- apply_patch
- append-only changes with >>
- unclear "change this section" instructions
- modifying a file without providing full replacement content

Assistant rule:

When the assistant asks the user to modify a file, the assistant must provide:

- exact file path
- exact command
- full replacement content
- save instructions
- verification command after user confirms completion

If the assistant fails to provide full replacement content for a file change, stop and correct the instruction before continuing.

---

## 3. Current confirmed state

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

## 4. Current operating mode

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

Updated runtime finding:

visual_pacing_plan.json already supports beat-level rendering through the existing visual pacing preview tool.

Production final render currently renders scene-level output.

Current technical focus:

Visual Pacing Preview -> Production Render Bridge

Goal:

Reduce PowerPoint/slideshow feeling in the final video by moving from scene-level render behavior toward beat-level / shot-aware production output.

---

## 5. Target architecture

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

## 6. Current implementation target

Current implementation target:

Director Brain MVP via Visual Pacing -> Production Render Bridge

Included:

- Module 5 — Director Engine
- Module 6 — Shot Planner / Scene Splitter
- Module 7 — Visual Concept & Pacing
- Module 11 — Assembly & Renderer bridge for beat-level / shot-aware output

Near-term technical target:

- use existing visual_pacing_plan.json beat structure
- preserve current dispatcher / runner
- avoid new DIRECTOR phase
- avoid a second runtime contour
- make production render visibly benefit from beat-level pacing

Optional after MVP:

- Module 8 — Overlay & Text Planner

MVP output expectation:

- director_plan.json when introduced
- shot_list.json when introduced
- visual_pacing_plan.json
- production render bridge
- new final render
- manual review result

---

## 7. Definition of Done for Director Brain MVP

Director Brain MVP is accepted only if:

1. director_plan.json is not generic and contains concrete visual intent when introduced.
2. shot_list.json contains timing, purpose, visual description, and motion instruction when introduced.
3. visual_pacing_plan.json is actually used by the render path or by a production-safe bridge.
4. unjustified static segments above 12 seconds are reduced.
5. shot / beat changes are meaningful, not random.
6. charts, dense cards, and infographics do not become less readable.
7. manual review scores the video as less PowerPoint-like by at least +2/10.
8. if the video is not visibly better, the MVP is not accepted even if all JSON files are valid.

---

## 8. Confirmed implementation findings

Confirmed executor surface:

- engine/executors/scenes_executor.py creates scenes/scenes.json
- engine/executors/assembly_executor.py creates assembly/assembly_plan.json
- engine/executors/visual_pacing_executor.py creates visual_pacing/visual_pacing_plan.json
- engine/executors/final_render_executor.py creates final_render/final_video.mp4 and final_render/final_render_report.json
- tools/render_visual_pacing_preview.py creates final_render/final_video_visual_pacing_preview.mp4 and final_render/visual_pacing_preview_report.json

Confirmed runtime finding:

- production final render currently renders 9 scene-level segments
- visual pacing preview renders 84 beat-level segments
- visual pacing preview applies motion_profile and visual_action
- visual pacing preview is not production output
- visual pacing preview does not update PROJECT_STATE
- visual pacing preview does not approve upload

Implication:

The next implementation should not start with a full Director Engine rewrite.

The next implementation should focus on turning the proven visual pacing preview behavior into a production-safe render bridge.

---

## 9. Forbidden now

Do not:

- create 12 empty module folders
- rewrite the runner
- rewrite the dispatcher
- add a new DIRECTOR phase
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
- modify any file without full replacement content
- use heredoc
- use partial edits

---

## 10. Commit rule

Commit only after the full meaningful work block is complete and validated.

Current uncommitted documentation block contains:

1. FLOWMIND_DIRECTOR_BRAIN_MVP_INTEGRATION_DECISION.md
2. FLOWMIND_FILE_EDIT_PROTOCOL.md
3. FLOWMIND_CURRENT_WORK_ANCHOR.md

Before commit:

- inspect files
- run required checks
- inspect git status
- commit once
- push once

---

## 11. Current next action

After this full replacement of FLOWMIND_CURRENT_WORK_ANCHOR.md:

1. verify anchor contains the file edit protocol reference
2. verify decision file still exists
3. verify file edit protocol exists
4. run preflight
5. commit the documentation / protocol block if checks pass

---

## 12. Stop rule

Stop if:

- the next action creates a second runtime contour
- the next action activates legacy modules
- the next action touches upload
- the next action rewrites runner/dispatcher before integration proof
- the next action creates fake progress without improving output
- the target architecture and current anchor conflict
- any file edit is requested without full replacement content
- any heredoc or partial edit is proposed

End.
