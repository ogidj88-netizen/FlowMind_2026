# FLOWMIND — SHOT SCHEMA v1

## 1. Purpose

Shot Schema defines the canonical output of Director Engine.

It is the ONLY valid format for:
- scene decomposition
- visual planning
- asset search input
- assembly timeline

No engine may bypass or modify this structure.

---

## 2. Global Rules

- Every script MUST be fully converted into shots
- No abstract scenes allowed
- Every shot must be:
  - time-bound
  - visually resolvable
  - executable with real assets

- Director defines intent ONLY
- Asset Engine resolves reality

---

## 3. Shot Object Structure

Each video is a list of shots.

### Shot object:

{
  "shot_id": "string",

  "timing": {
    "start": float,
    "end": float,
    "duration": float
  },

  "scene_role": "hook | build | payoff | transition",

  "visual": {
    "asset_type": "video | image",
    "query": "string",
    "style": "string",
    "motion": "static | zoom_in | zoom_out | pan | parallax",
    "priority": "primary | secondary"
  },

  "text_overlay": {
    "enabled": true,
    "content": "string",
    "style": "default | highlight | warning",
    "position": "center | top | bottom"
  },

  "audio_intent": {
    "sfx": ["string"],
    "music_energy": int
  },

  "constraints": {
    "no_repeat": true,
    "style_lock": true
  }
}

---

## 4. Timing Rules

- All timing is derived from audio (post-generation)
- duration MUST equal (end - start)
- No overlapping shots allowed
- No empty timeline gaps allowed

---

## 5. Visual Rules

- Query MUST be realistic (searchable in stock APIs)
- No abstract or fantasy-only prompts
- Style must match global style_lock

Examples:

VALID:
- "car driving night city rain"
- "close up stressed driver traffic"

INVALID:
- "emotional collapse of financial system visualized as storm of money"

---

## 6. Motion Rules

Allowed motions:
- static
- zoom_in
- zoom_out
- pan
- parallax

No custom motion definitions allowed.

---

## 7. Audio Intent Rules

- SFX is optional but required for:
  - text appearance
  - transitions
  - emphasis moments

- music_energy scale:
  1 = calm
  5 = neutral
  10 = intense

---

## 8. PASS Conditions

Director output is valid if:
- 100% script coverage
- all shots have timing
- all queries are realistic
- hook contains minimum 3 shot changes
- hook contains minimum 2 text overlays

---

## 9. FAIL Conditions

Director output is rejected if:
- missing timing
- abstract queries
- missing hook dynamics
- impossible shots
- style inconsistency

---

## 10. Enforcement

- Asset Engine MUST reject invalid queries
- QA Engine MUST reject weak hook structure
- Assembly MUST NOT run without valid shot schema

---

## 11. Conclusion

Shot Schema is the backbone of FlowMind visual pipeline.

Without it:
- system becomes chaotic
- assets become random
- videos lose structure

With it:
- Director becomes deterministic
- Asset Engine becomes reliable
- Assembly becomes stable
