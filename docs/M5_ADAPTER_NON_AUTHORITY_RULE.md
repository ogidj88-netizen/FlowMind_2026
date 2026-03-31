# M5 Adapter Non-Authority Rule

## Purpose

This document defines the non-authority rule for the read-only compatibility adapter in Migration v1.

The goal is to prevent adapter output from being misused as a replacement runtime state surface.

---

## Core rule

Adapter output is a derived artifact only.

It is not canonical state.

It is not a second runtime state store.

It is not a control surface.

It is not a dispatcher substitute.

---

## Canonical authority

Canonical authority remains exclusively with:

- canonical dispatcher logic
- canonical transition ownership
- canonical halt ownership
- canonical approval ownership
- canonical PROJECT_STATE.json as runtime source of truth

If adapter output differs from canonical state, canonical state wins immediately.

---

## Adapter limitation rule

Adapter output may be used only for:

- compatibility display
- compatibility reads
- downstream non-authoritative branching
- migration support behavior

Adapter output must not be used for:

- restoring runtime state
- replacing PROJECT_STATE.json
- replaying canonical decisions
- reconstructing dispatcher authority
- inferring write permissions
- treating derived compatibility data as canonical truth

---

## Persistence rule

If adapter payload is stored anywhere, that stored copy remains non-authoritative.

Persistence does not upgrade authority.

Caching does not upgrade authority.

Convenience does not upgrade authority.

Legacy usage does not upgrade authority.

---

## Anti-substitution rule

The following substitutions are forbidden:

1. adapter output in place of PROJECT_STATE.json
2. adapter payload in place of dispatcher-owned phase truth
3. adapter snapshot in place of canonical halt truth
4. adapter-derived approval interpretation in place of canonical approval truth
5. any operational flow where adapter data becomes the practical state authority

---

## Migration v1 statement

For Migration v1:

- canonical state remains canonical
- adapter output remains derived
- derived output never becomes authoritative
- legacy runtime remains downstream of canonical ownership

---

## Acceptance condition for M5

M5 may be considered prepared on docs level only if:

1. adapter output is explicitly called derived
2. adapter output is explicitly called non-authoritative
3. substitution of adapter for canonical state is explicitly forbidden
4. persistence is explicitly denied authority-upgrade semantics
5. canonical dispatcher ownership remains explicit

---

## Final statement

The adapter exists to reduce migration friction, not to create a parallel state system.

Any interpretation that upgrades adapter output into operational authority is invalid.
