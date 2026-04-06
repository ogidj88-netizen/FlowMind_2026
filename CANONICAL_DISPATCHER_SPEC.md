# CANONICAL DISPATCHER SPEC

Останнє оновлення: 2026-04-06
Статус: ACTIVE CONTROL SPEC
Призначення: активний контракт canonical control layer для FlowMind cashflow-mode

---

## 1. РОЛЬ

Canonical Dispatcher — це єдиний активний control brain системи.

Він:
- читає PROJECT_STATE.json
- перевіряє валідність стану
- визначає дозволений перехід фази
- виконує контроль переходу
- блокує незаконні переходи
- фіксує HALT / resume / approval-related transitions
- зберігає оновлений стан через захищений state layer

Dispatcher НЕ є production-модулем.
Dispatcher НЕ генерує контент.
Dispatcher НЕ є legacy launcher.
Dispatcher керує маршрутом і цілісністю control flow.

---

## 2. SINGLE SOURCE OF TRUTH

Єдине джерело правди для active control contour:

`projects/<PROJECT_ID>/PROJECT_STATE.json`

Canonical dispatcher не використовує ExecutionManifest.json як runtime source of truth.

---

## 3. ACTIVE CONTROL CORE

Активний canonical control core складається з:

- `engine/canonical_dispatcher.py`
- `engine/state_validator.py`
- `engine/state_store.py`

Ці файли формують базу одного активного control contour.

---

## 4. ACTIVE ENTRYPOINTS

Офіційні active entrypoints для canonical dispatcher:

- `tools/dispatcher.sh` — shell entrypoint
- `tools/dispatcher_cli.py` — CLI implementation layer
- `tools/check_dispatcher.sh` — validation entrypoint

---

## 5. STATE MODEL

Canonical dispatcher працює через поле:

`phase`

а не через:
- `status`
- `current_phase` legacy runtime
- station-completion model типу `S1_DONE`, `S2_DONE`, etc.

---

## 6. CANONICAL PHASES

Поточна canonical phase model:

- `TOPIC`
- `SCRIPT`
- `SCENES`
- `ASSETS`
- `ASSEMBLY`
- `QA`
- `READY_FOR_UPLOAD`
- `UPLOADED`
- `ARCHIVED`
- `HALT`

---

## 7. GUARDED TRANSITIONS

Dispatcher дозволяє тільки явно визначені переходи між фазами.

Dispatcher зобов’язаний:
- забороняти no-op transitions
- забороняти незаконні переходи
- забороняти unsafe rollback after protected phases
- вимагати обов’язкові runtime conditions before guarded transitions

Приклади guard logic:
- `ASSEMBLY -> QA` тільки якщо існує `artifacts.final_video_path`
- `QA -> READY_FOR_UPLOAD` тільки якщо `qa_passed = true`
- `READY_FOR_UPLOAD -> UPLOADED` тільки якщо `approved_for_upload = true`

---

## 8. HALT / RESUME RULE

Dispatcher може:
- перевести стан у `HALT`
- записати `halt_reason`
- записати `resume_hint`
- дозволити resume тільки в дозволені canonical phases

Resume із `HALT` дозволений тільки через canonical dispatcher rules.

---

## 9. STATE DISCIPLINE

Canonical state layer зобов’язаний:
- валідовувати top-level PROJECT_STATE structure
- валідовувати manifest payload inside state
- контролювати immutable vs mutable fields
- блокувати несанкціоновані runtime mutations
- зберігати state тільки через захищений state-store path

---

## 10. LEGACY SEPARATION

Наступні файли НЕ входять в active canonical control contour:

- `main.py`
- `dispatcher/engine.py`
- `dispatcher/engine_v16.py`

Вони є legacy / retired artifacts і не повинні використовуватись як активні control entrypoints.

---

## 11. NOT ALLOWED

Заборонено:
- відновлювати legacy dispatcher flow
- змішувати `ExecutionManifest.json` runtime flow з `PROJECT_STATE.json` flow
- змішувати legacy statuses зі canonical phases
- створювати новий parallel control brain
- вводити новий root entrypoint без сильної практичної потреби
- називати legacy launcher canonical dispatcher

---

## 12. CURRENT PRACTICAL RULE

Під час Phase 2 система не потребує нової вигаданої архітектури control layer.

Система потребує:
- control-layer alignment
- removal of legacy control ambiguity
- one active dispatcher contour
- one active command surface

---

## 13. TARGET

Поточна ціль canonical dispatcher layer:

Стати єдиним активним control brain для FlowMind cashflow-mode
без legacy ambiguity, без parallel control logic, без подвійної state model.
