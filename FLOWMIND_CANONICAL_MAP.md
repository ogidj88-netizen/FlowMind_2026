## 12. RUNTIME / DISPATCHER SPLIT (LOCKED)

### Поточний підтверджений стан

У `cashflow-mode` одночасно існують **дві окремі системи керування**.

---

### A. Legacy Runtime Layer

Підтверджено:

- `main.py` існує
- `main.py` викликає:
  - `dispatcher/engine.py --halt`
  - `dispatcher/engine.py --resume`
  - `dispatcher/engine.py --advance`
- `dispatcher/engine.py` працює через `ExecutionManifest.json`
- legacy runtime використовує стару фазову модель типу:
  - `CREATED`
  - `S1_DONE`
  - `S2_DONE`
  - `S5_DONE`
  - `S6_DONE`
  - `S7_DONE`
  - `S8_DONE`
  - `S9_DONE`
  - `S10_DONE`

### Legacy runtime verdict

Legacy runtime **існує**, але не є основою нового canonical dispatcher layer.

---

### B. Canonical Dispatcher Layer

Підтверджено:

- `docs/CANONICAL_MANIFEST_SPEC.md`
- `engine/state_validator.py`
- `engine/state_store.py`
- `engine/canonical_dispatcher.py`
- `tools/run_dispatcher_checks.py`
- `tools/check_dispatcher.sh`
- `tools/dispatcher_cli.py`
- `tools/dispatcher.sh`

Canonical dispatcher layer працює через:

- `PROJECT_STATE.json`

Canonical dispatcher layer використовує нову фазову модель:

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

### Canonical dispatcher verdict

Canonical dispatcher layer **побудований, протестований і підтверджений**, але поки що працює як:

> standalone stable control layer

а не як вшита заміна legacy runtime.

---

### C. Що заборонено

До окремого migration plan заборонено:

- вважати `dispatcher/engine.py` canonical dispatcher нового контуру
- вважати `dispatcher/engine_v16.py` живим canonical dispatcher
- напряму підміняти `main.py` на новий dispatcher
- змішувати `ExecutionManifest.json` і `PROJECT_STATE.json`
- змішувати фази `S1_DONE/S2_DONE/...` з фазами `TOPIC/SCRIPT/SCENES/...`
- вважати legacy runtime і canonical dispatcher однією системою

---

### D. Dispatcher / Runtime Final Decision

Поточне канонічне рішення таке:

1. Legacy runtime layer існує окремо.
2. Canonical dispatcher layer існує окремо.
3. Пряма міграція між ними ще не затверджена.
4. Будь-яка інтеграція можлива лише після окремого audit + migration plan.

---

### E. Operational Truth

На поточному етапі правильне формулювання таке:

- `main.py` = legacy runtime entrypoint
- `dispatcher/engine.py` = legacy runtime dispatcher layer
- `engine/canonical_dispatcher.py` = new canonical dispatcher control layer
- `tools/dispatcher_cli.py` / `tools/dispatcher.sh` = canonical local dispatcher entrypoints
- `tools/check_dispatcher.sh` = canonical local dispatcher validation entrypoint

---

### F. Locked rule

До окремого рішення про migration:

> НЕ інтегрувати новий dispatcher у legacy runtime напряму.
> НЕ оголошувати legacy runtime новим canonical dispatcher.
> НЕ рефакторити старий dispatcher-шар “по дорозі”.
