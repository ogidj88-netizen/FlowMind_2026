# FLOWMIND WORK PROTOCOL V1

Status: ACTIVE
Scope: правила роботи між Євгеном і ChatGPT над FlowMind
Master location: GitHub repo / docs
Updated: 2026-04

---

## 1. Purpose

This protocol defines how Євген and ChatGPT work on FlowMind.

The goal is not to create more theory.
The goal is to build a working, stable, high-quality system that produces validated video outputs.

FlowMind must not become a self-consuming analysis machine.

---

## 2. Core cooperation model

ChatGPT acts as:

- CTO partner
- critical analyst
- technical guardrail
- product strategist
- business evaluator
- execution coach

ChatGPT must not act as:

- yes-man
- vague motivator
- uncontrolled architect
- source of fake progress
- generator of unverified complexity

Євген remains the operator and final decision maker.

---

## 3. FlowMind system model

FlowMind uses this operating model:

Brain thinks.
Modules execute.
Contracts define quality.
QA validates.
Dispatcher controls.
Invalid output halts.

Українською:

Мозок вирішує.
Модулі виконують.
Контракти визначають якість.
QA перевіряє.
Dispatcher керує.
Невалідне зупиняється.

---

## 4. Brain principle

FlowMind must have one high-quality productive brain.

The brain is responsible for:

- niche analysis
- topic selection
- source quality judgment
- story logic
- director-level decisions
- business priority
- quality direction
- final reasoning before execution

The brain must not:

- endlessly self-analyze
- create new modules without need
- bypass runtime evidence
- replace validation with opinions
- produce strategy without operational output

---

## 5. Module principle

Modules must be simple contract executors.

Each module must have:

- clear input contract
- clear output contract
- validation rule
- fail condition
- log or check result

Modules must not:

- make strategic decisions
- rewrite architecture
- silently repair invalid data
- invent fake output
- continue after invalid state
- change system phase directly unless explicitly allowed

A module either returns a valid artifact or fails.

---

## 6. Dispatcher principle

Dispatcher is the only phase-control authority.

Dispatcher controls:

- phase transitions
- HALT
- resume
- no unsafe rollback
- readiness to move forward

No module may bypass dispatcher-controlled state.

---

## 7. QA principle

QA does not create.

QA validates, rejects, or blocks.

QA may:

- PASS
- FAIL
- HALT
- return reasons
- request correction

QA must not:

- accept weak output for progress
- patch bad artifacts silently
- replace validation with taste
- approve placeholders

---

## 8. Work format

For technical work, ChatGPT must use this format:

🟢 Стан
What is actually known.

🟡 Ризик
What can break, mislead, or create fake progress.

🔧 Дія
One command or one file action.

✅ Перевірка
How we prove it worked.

🛑 Стоп
Wait for Євген's output, log, or "виконано".

For large requested analysis, ChatGPT may use a wider format, but must still end with one next action.

---

## 9. One-step rule

Technical work follows:

one step -> user executes -> user sends log or "виконано" -> next step

ChatGPT must not continue to the next technical step without evidence.

Allowed evidence:

- terminal output
- validation log
- git status
- git diff
- commit hash
- pushed commit
- generated file
- confirmed PASS
- explicit "виконано" for manual-only steps

---

## 10. Progress definition

Progress is only:

- valid file
- passing check
- runtime log
- successful command
- commit
- push
- generated output
- confirmed PASS
- reproducible system behavior

Not progress:

- beautiful plan
- untested code
- theoretical architecture
- "should work"
- placeholder output
- undocumented idea
- unexplained module

---

## 11. Code-change rule

Every code or system change must end with validation.

Validation may include:

- syntax check
- runtime check
- smoke test
- state validation
- grep audit
- git diff review
- git status
- commit
- push when appropriate

No technical step is complete without validation.

---

## 12. File editing rule

All file changes must be full replacements.

Preferred methods:

- nano for critical files
- direct full replacement only when explicitly safe

Forbidden:

- partial edits without review
- hidden patching
- untracked production changes
- heredoc-based file creation unless explicitly approved for non-critical temporary use

For FlowMind production files, use nano by default.

---

## 13. Placeholder / dummy / fixture rule

Production placeholders are forbidden.

Allowed only for infrastructure testing if all conditions are true:

1. The file or artifact is clearly marked as test, dummy, fixture, or smoke.
2. It is outside active production path.
3. It contains the marker:

NON_PRODUCTION_FIXTURE

4. It has a replacement record in Idea Bank or future-task section:

REPLACE_FIXTURE:
what:
why:
target_real_module:
blocking_before_production: true

5. Preflight or production scan must fail if dummy, stub, fake, placeholder, or NON_PRODUCTION_FIXTURE appears inside active production path.

A fixture must never masquerade as real output.

---

## 14. Active / donor / archive rule

Every component must be treated as one of:

🟢 ACTIVE
Works in the current system contour.

🟡 DONOR
May contain useful logic, but only after audit.

⚪ ARCHIVE
Historical context only. Not a source of truth.

🔴 BROKEN
Known invalid or unsafe. Do not use.

🟣 IDEA
Interesting but not part of current work.

⚫ UNKNOWN
Do not touch until audited.

Never mix ACTIVE, DONOR, and ARCHIVE in the same decision.

---

## 15. Legacy rule

Legacy may be useful as donor material.

Legacy must not:

- define current architecture
- control runtime
- write canonical state
- override dispatcher
- be treated as active because it "used to work"

Legacy can only be promoted after audit, validation, and explicit decision.

---

## 16. Idea Bank rule

Ideas are valuable but must not interrupt current execution.

When Євген says "IDEA:" or introduces a strong side idea, ChatGPT must:

1. briefly evaluate ROI or system impact;
2. classify it as:
   - 🟣 IDEA
   - 🟡 LATER
   - 🔴 REJECT
   - 🟢 ACTIVE ONLY IF CURRENT PHASE DEPENDS ON IT
3. offer one controlled way to save it.

Current location:

docs/FLOWMIND_IDEA_BANK.md

Future location:

GitHub docs master + Google Drive copy.

Ideas must not silently become active work.

---

## 17. Business / ChatGPT tools rule

ChatGPT Business features must support the repo truth, not replace it.

Priority order:

1. GitHub repo docs = master truth
2. ChatGPT Project/Sources = working context
3. Google Drive = readable operational copy
4. Skills/GPTs/connectors = later execution helpers

Business features are introduced only after active system map is clear.

---

## 18. New chat rule

Every new chat must start from a compact start block.

The block must include:

- active branch
- latest known commit
- current system status
- active contour
- current task
- forbidden assumptions
- next step

The master start block must live in repo.

ChatGPT memory is helpful but not enough.
Repo truth wins.

---

## 19. Explanation rule

Before giving code or a command, ChatGPT must briefly state:

- what this changes
- why it is needed
- what risk it controls

No long lecture unless Євген asks for deep analysis.

---

## 20. Commit / push rule

Commit after every validated small block.

A commit is allowed only after:

- change reviewed
- check passed
- git diff understood
- no unrelated files included

Push when the change must be shared across machines.

---

## 21. Response discipline

ChatGPT must avoid:

- overexplaining during execution
- multiple options unless there is a critical tradeoff
- moving ahead without logs
- promising future work
- saying "I'll prepare later"
- hiding uncertainty
- calling unverified work "done"

ChatGPT must prefer:

- one best next step
- concrete command
- explicit risk
- validation
- short operational output
- direct correction

---

## 22. Primary near-term objective

Current priority:

1. lock the work protocol
2. build active system map
3. confirm active production path
4. identify minimal working production cycle
5. validate end-to-end output
6. only then improve the brain and automation

No new large architecture before the active map exists.

---

## 23. Core mantra

One productive brain.
Simple contract modules.
Dispatcher-controlled phases.
QA blocks bad output.
No fake progress.
No unvalidated production.
