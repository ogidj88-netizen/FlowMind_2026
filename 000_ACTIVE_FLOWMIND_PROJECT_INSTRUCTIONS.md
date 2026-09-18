# 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS

Status: HIGHEST PRIORITY ACTIVE PROJECT SOURCE
Project: FlowMind / Imagine What If

## 1. Purpose

This file defines the highest-priority operating rules for ChatGPT work on FlowMind.

Its purpose is to prevent:

- context drift
- architecture drift
- stale-document authority
- legacy reactivation
- trusting files by filename instead of content
- building functionality that does not belong to the agreed FlowMind target

If another uploaded Project Source conflicts with this file, this file wins.

---

## 2. Product target authority

FLOWMIND_WORKING_TARGET.md defines:

- what FlowMind is intended to become
- the canonical target shape
- system intent
- scope boundaries
- what belongs and does not belong in the target system

FLOWMIND_WORKING_TARGET.md is trusted for product target and system intent.

It is NOT proof that any runtime component is currently implemented or working.

Before proposing architecture, modules, integrations, providers, or major technical changes, ChatGPT must check alignment with FLOWMIND_WORKING_TARGET.md.

If a proposal does not directly support the agreed target, it must not become active work.

---

## 3. Current operational context

The active current operational context is:

CHAT_START_BLOCK_FLOWMIND_CURRENT.md

It describes the last confirmed working state, active contour, current blockers, and current next action.

It must not override newer direct runtime evidence from the current audit.

---

## 4. Mandatory FILE CONTENT VERIFICATION GATE

Before ChatGPT recommends that any file is:

- added to Project Sources
- treated as TRUSTED
- used as architecture authority
- used as runtime authority
- used to modify another authority document
- promoted from legacy or unverified status
- used as the basis for implementation

ChatGPT MUST first verify the actual contents of that exact file.

Filename, path, age, reputation, or a reference from another document is NOT sufficient evidence.

### Required verification

For every candidate authority file, ChatGPT must:

1. locate the exact file;
2. read its actual current contents;
3. identify its declared status and scope;
4. identify what phase or historical state it describes;
5. check whether its "current next action" is still current;
6. compare it with:
   - this file;
   - FLOWMIND_WORKING_TARGET.md;
   - CHAT_START_BLOCK_FLOWMIND_CURRENT.md;
   - relevant current repo evidence;
   - relevant current terminal/runtime evidence;
7. detect contradictions, stale assumptions, legacy instructions, or duplicated authority;
8. classify it as exactly one of:
   - TRUSTED
   - FROZEN LEGACY
   - UNVERIFIED

Only after this verification may ChatGPT recommend adding or using the file as active authority.

---

## 5. Fail-closed rule

If ChatGPT cannot read enough of a file to verify its contents:

Status = UNVERIFIED.

If two authority documents conflict and the conflict cannot be resolved from current evidence:

STOP.

Do not guess.
Do not silently reconcile.
Do not choose the file with the more convincing filename.
Do not continue implementation on top of unresolved authority.

The next action must be to obtain evidence and resolve the conflict.

---

## 6. No filename trust

The following assumptions are explicitly forbidden:

- "ACTIVE" in a filename means the file is active
- "CURRENT" means the file is current
- "CANONICAL" means the file is canonical
- "TRUSTED" means the file is trusted
- a newer-looking version number means the file is authoritative
- a file is trusted because another document references it
- a file is trusted because it exists in Project Sources
- a file is trusted because it exists in the GitHub repository

Content and verified authority determine trust.

Names do not.

---

## 7. Product alignment gate

Before any technical or architectural recommendation, ChatGPT must be able to answer:

1. What part of FLOWMIND_WORKING_TARGET.md does this action support?
2. Is this action inside the current active phase?
3. Does it create a second active contour?
4. Does it mix active, legacy, donor, archive, or unverified material?
5. Does it directly improve at least one of:
   - output quality
   - runtime stability
   - release speed
   - monetization potential

If these questions cannot be answered clearly:

STOP.

Do not proceed.

---

## 8. Project Sources rule

Project Sources are working context for ChatGPT.

They are NOT automatically source of truth merely because they are uploaded.

A file may enter active Project Sources only after content verification when it is intended to influence active decisions.

Legacy/archive files must not influence active decisions.

Secrets, credentials, .env files, API keys, or equivalent secret configuration must never be used as architecture authority or uploaded as active Project Sources.

---

## 9. Source synchronization rule

GitHub repository remains the durable project master.

Project Sources provide ChatGPT working context.

When an active authority document is changed in GitHub:

- its Project Source copy must be updated before ChatGPT relies on the new version;
- ChatGPT must not assume that the Project Source copy and repo copy are identical;
- version/content mismatch must be treated as UNVERIFIED until checked.

---

## 10. Legacy / archive block

The following files or concepts must not be treated as active authority unless explicitly re-audited and promoted:

- MASTER_PROMPTS_v2_FULL.txt
- CHAT_START_BLOCK.txt
- old FLOWMIND_MODULE_STATUS.md
- old FLOWMIND_FIX_BACKLOG.md
- old IronCore v3.5 references
- old horror rules
- old Telegram / YouTube / TikTok provider plans
- old migration-era architecture
- retired runtime contours

Legacy may be read for historical context only.

It must not silently return to active authority.

---

## 11. Authority roles

This file:
controls ChatGPT operating discipline and anti-drift rules.

FLOWMIND_WORKING_TARGET.md:
controls product target and intended system shape.

CHAT_START_BLOCK_FLOWMIND_CURRENT.md:
records the last confirmed operational checkpoint.

Current repo + runtime evidence:
prove what actually exists and works.

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md and trust-boundary documents:
may classify authority only after their own contents and freshness have been verified.

No document may grant itself permanent authority merely by declaring itself authoritative.

---

## 12. Current mode

Current mode:

SYSTEM MAP MODE

Current objective:

Audit and clean FlowMind authority, Project Sources, trust boundaries, and active system map before resuming production development.

---

## 13. Forbidden now

Until the authority/source audit is complete:

- do not tune video quality
- do not add YouTube upload
- do not add Telegram integration
- do not add TikTok crossposting
- do not add new provider integrations
- do not activate engine/module_runner.py
- do not execute engine/modules/*
- do not create a second runtime contour
- do not trust unverified documents
- do not redesign modules based on stale documents
- do not add files to Project Sources without content verification

---

## 14. Current next action

Audit existing Project Sources and authority documents one by one.

For every file:

READ
→ VERIFY CONTENT
→ CHECK FRESHNESS
→ CHECK CONFLICTS
→ CLASSIFY
→ KEEP / REMOVE / UPDATE

Do not resume production implementation until the authority chain is internally consistent.

---

## 15. One-step rule

Work proceeds:

one step
→ evidence
→ user says "виконано" or provides output
→ next step

Do not jump ahead.

End.
