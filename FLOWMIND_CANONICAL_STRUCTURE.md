# FLOWMIND CANONICAL STRUCTURE

Status: FROZEN LEGACY
Project: FlowMind / Imagine What If
Role: historical architecture checkpoint only

## 1. Purpose

This file is retained as historical evidence of an earlier FlowMind architecture model.

Earlier versions described:

- Topic Intelligence Lite
- Manifest / Dispatcher / Project State control model
- production module sequence
- QA
- Telegram approval
- upload and publication flow
- older lifecycle-state naming

This file no longer defines the current canonical architecture.

---

## 2. Why this file is frozen

Earlier versions contained architecture assumptions that are no longer current.

Examples include:

- Topic Intelligence Lite as canonical front layer
- Topic Queue as the only production-topic source
- Telegram approval as part of canonical lifecycle
- publication as part of the active canonical structure
- older lifecycle states such as:
  - TOPIC_SELECTED
  - SCRIPT_READY
  - SCENES_READY
  - ASSETS_READY
  - ASSEMBLY_READY
  - QA_PASSED
  - READY_FOR_REVIEW
  - TELEGRAM_APPROVED
  - SCHEDULED
  - PUBLISHED

These concepts must not override newer verified authority.

---

## 3. Current authority routing

For high-level product intent use:

- FLOWMIND_WORKING_TARGET.md

For detailed target architecture use:

- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

For current operational state use:

- FLOWMIND_ACTIVE_MAP.md

For control-plane semantics use:

- CANONICAL_DISPATCHER_SPEC.md

For authority classification use:

- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

For operating discipline use:

- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

For execution discipline use:

- docs/FLOWMIND_WORK_PROTOCOL_V1.md

Runtime truth requires current repo and runtime evidence.

---

## 4. Historical principles preserved

The following principles remain useful:

- one canonical control plane
- explicit phase transitions
- no module-level bypass of control authority
- artifacts must align with valid runtime state
- QA must gate unsafe progression
- publication must not bypass approval policy
- implementation details must not redefine architecture silently

These principles are now governed by newer verified authority.

This file itself does not grant architecture authority.

---

## 5. Obsolete architecture assumptions

Do not treat the following as current requirements merely because they appeared in previous versions:

- Telegram approval as mandatory architecture
- Topic Intelligence Lite as canonical production entry
- Topic Queue as exclusive topic authority
- old READY_FOR_REVIEW / TELEGRAM_APPROVED lifecycle
- SCHEDULED / PUBLISHED lifecycle model
- old module sequence
- old publication layer
- old manifest/state assumptions

Each of these requires current verification or explicit re-approval before use.

---

## 6. Prohibitions

Do not use this file to:

- define current target architecture
- determine current module order
- determine current phase names
- authorize Telegram integration
- authorize upload implementation
- define current topic-intelligence architecture
- determine current next action
- override CANONICAL_DISPATCHER_SPEC.md
- override FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md
- override newer runtime evidence

Do not resurrect old architecture from Git history without audit.

---

## 7. Historical-use rule

Previous versions may be used only for:

- architecture history
- tracing earlier design decisions
- identifying obsolete assumptions
- comparing old and current system models
- understanding why certain constraints were introduced

Historical value does not equal current authority.

---

## 8. Final classification

Classification:

FROZEN LEGACY

Current authority:

NONE

Historical value:

YES

Current architecture value:

NO

Current-next-action value:

NO

Runtime-proof value:

NO

End.
