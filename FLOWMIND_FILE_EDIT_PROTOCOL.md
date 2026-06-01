# FLOWMIND FILE EDIT PROTOCOL

Status: ACTIVE OPERATIONAL RULE  
Project: FlowMind / Imagine What If  
Mode: HARD FILE EDIT DISCIPLINE

---

## 1. Purpose

This file defines the mandatory file editing protocol for FlowMind work.

This protocol exists because partial edits, patch-style changes, unclear commands, append operations, and implicit modifications create operational risk.

All future file edits must follow this protocol.

---

## 2. Core rule

Every file modification must be done as a full file replacement.

No partial edits.

No patch-style edits.

No hidden edits.

No silent append.

No inline mutation.

No sed-based mutation.

No automatic partial rewrite.

---

## 3. Allowed edit methods

Allowed methods:

1. nano

Use:

cd ~/FlowMind_2026
nano path/to/file

Then replace the entire file content manually.

Save with:

Ctrl+O
Enter
Ctrl+X

2. Direct cat input

Use only this form:

cat > path/to/file

Then paste the full complete file content.

Finish with:

Ctrl+D

---

## 4. Forbidden edit methods

Forbidden:

- heredoc
- cat << EOF
- cat <<'EOF'
- python scripts that rewrite only parts of a file
- sed -i
- perl -pi
- awk in-place mutation
- apply_patch
- appending with >>
- partial replacement commands
- editing only one section unless the entire final file content is provided
- unclear "update this section" instructions

---

## 5. Assistant behavior rule

When the assistant asks the user to modify a file, the assistant must provide:

1. exact file path
2. exact command to open or create the file
3. full replacement content if content is being changed
4. explicit save instructions
5. verification command after the user confirms completion

The assistant must not say "change this part" or "add this section" unless it also provides the full final file content.

---

## 6. User execution rule

The user executes file changes manually.

The assistant provides precise commands and full replacement content.

The assistant must not assume that a file was modified until the user provides terminal output or says "виконано".

---

## 7. Production safety rule

Production files must not contain placeholders, stubs, fake outputs, dummy data, or TODO markers unless explicitly marked as non-production fixtures.

If a file is production-facing, the final full replacement content must be complete and operationally meaningful.

---

## 8. Commit rule

Do not commit after every small edit.

Commit only after a meaningful work block is complete and verified.

Before commit:

- inspect changed files
- run required checks
- inspect git status
- commit once
- push once

---

## 9. Stop rule

Stop immediately if the next proposed action requires:

- partial edit
- unclear file mutation
- heredoc
- patch
- append-only change
- modifying production code without full replacement content
- building on unknown file state

If this happens, rewrite the instruction as a full replacement workflow.

---

## 10. Final rule

For FlowMind:

Full replacement only.

No partial file edits.

No heredoc.

No fake progress.

End.
