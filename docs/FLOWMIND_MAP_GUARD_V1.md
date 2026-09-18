# FLOWMIND MAP GUARD V1

Status: ACTIVE OPERATIONAL GUARD
Project: FlowMind / Imagine What If
Mode: SYSTEM MAP MODE

## 1. Purpose

Prevent FlowMind work from drifting away from the verified product target and current operational map.

This guard does not define product architecture.

This guard enforces alignment before technical work.

---

## 2. Required MAP CHECK

Before every technical or architectural answer, the assistant must show:

MAP CHECK
Active map:
Current step:
Allowed action:
Forbidden action:
Evidence:
Verdict:

If the assistant cannot fill this block from verified sources:

STOP.

Do not guess.

---

## 3. Verified authority chain

Use authority by role, not by filename prestige.

### Operating discipline

000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

Controls:

- anti-drift rules
- source verification rules
- current audit objective
- authority discipline

### Product intent

FLOWMIND_WORKING_TARGET.md

Controls:

- high-level product intent
- optimization principles
- scope discipline
- ROI / minimalism boundaries

### Detailed target architecture

FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

Controls:

- detailed target architecture
- 12-module destination
- target layers
- target module responsibilities

It is not runtime proof.

### Current operational map

FLOWMIND_ACTIVE_MAP.md

Controls:

- where we are now
- what work is allowed now
- what work is forbidden now
- current exit condition

### Runtime truth

Current repo and runtime evidence prove:

- what exists
- what runs
- what produces artifacts
- what is consumed downstream
- what actually passes validation

Documents do not substitute for runtime evidence.

---

## 4. Unverified authority rule

The following must NOT automatically control work unless individually audited and verified:

- FLOWMIND_ACTION_SEQUENCE_V1.md
- FLOWMIND_SYSTEM_MAP_V1.md
- FLOWMIND_CANONICAL_STRUCTURE.md
- FLOWMIND_REPO_TRUST_BOUNDARY_V1.md
- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- migration-era documents
- historical start blocks
- historical work anchors
- old module status documents
- old fix backlogs

A reference from another document is not enough.

Content must be verified.

---

## 5. Current default

Current mode:

SYSTEM MAP MODE

Current objective:

Complete authority and Project Sources reconciliation before production development resumes.

Current active step:

Audit one file at a time:

READ
→ VERIFY CONTENT
→ CHECK FRESHNESS
→ CHECK CONFLICTS
→ CLASSIFY
→ KEEP / REMOVE / UPDATE
→ VERIFY

---

## 6. Current forbidden work

Until authority reconciliation is complete:

- no Director Brain implementation
- no renderer changes
- no video-quality tuning
- no YouTube upload
- no Telegram integration
- no TikTok crossposting
- no new providers
- no runner rewrite
- no dispatcher rewrite
- no legacy module activation
- no second runtime contour
- no upload approval
- no READY_FOR_UPLOAD transition
- no implementation based on stale operational documents

---

## 7. Stop triggers

STOP if:

1. current operational step is unclear;
2. authority documents materially conflict;
3. source freshness is unknown;
4. a file is trusted only because of its filename or declared status;
5. the action does not match FLOWMIND_ACTIVE_MAP.md;
6. the action creates a second runtime contour;
7. the action activates legacy code;
8. active, donor, archive, legacy, or unverified material is mixed;
9. production placeholders or fake outputs are proposed;
10. current runtime evidence contradicts documentation;
11. implementation is proposed before the authority audit is complete.

---

## 8. File modification rules

All FlowMind file modifications must use full replacement.

Allowed:

1. nano
2. direct input:
   cat > path/to/file
   then paste full content and Ctrl + D

Forbidden:

- heredoc
- cat << EOF
- partial edits
- apply_patch
- sed -i
- append-only fixes
- hidden edits
- production placeholders

---

## 9. Git rules

Do not commit after every audited file.

During the authority audit:

- accumulate one meaningful audit block
- keep changes visible in git status
- validate each changed file
- run preflight before the final block commit

Before final commit:

1. inspect git diff
2. run relevant checks
3. run bash tools/preflight.sh
4. inspect git status
5. stage only intended files
6. commit one meaningful audit block
7. push once
8. verify clean status
9. synchronize changed authority files with Project Sources

---

## 10. Source synchronization rule

GitHub repository is the durable project master.

Project Sources are ChatGPT working context.

If an active authority file changes:

- GitHub and Project Sources must be synchronized;
- content mismatch means UNVERIFIED;
- internal upload suffixes such as (1) or (2) do not change logical identity if actual file content and canonical heading match.

---

## 11. Exit condition

This guard remains valid when:

1. every technical answer uses a verified MAP CHECK;
2. current operational work is taken from FLOWMIND_ACTIVE_MAP.md;
3. product direction is checked against verified product authority;
4. runtime claims are backed by runtime evidence;
5. stale documents cannot silently override current work;
6. authority conflicts cause STOP instead of guessing.

---

## 12. One-step rule

Work proceeds:

one file
→ audit
→ verdict
→ KEEP / REMOVE / UPDATE
→ verify
→ next file

No automatic jumping ahead.

End.
