# CANONICAL MANIFEST SPEC

Status: LOCKED
Branch: `cashflow-mode`
Scope: `FlowMind_2026`
Purpose: зафіксувати єдиний канонічний контракт manifest для Cashflow Mode перед реалізацією canonical dispatcher.

---

## 1. Основне рішення

У `cashflow-mode` **не існує окремого канонічного `EXECUTION_MANIFEST.json`**.

Єдине канонічне runtime-джерело правди:

- `PROJECT_STATE.json`

Canonical manifest існує як **immutable block** всередині:

- `PROJECT_STATE.json.manifest`

Це правило введено для того, щоб не створювати дві правди:
1. окремий manifest-файл
2. окремий runtime state-файл

У `cashflow-mode` це заборонено.

---

## 2. Жорсткий поділ відповідальності

### 2.1 Immutable zone — `manifest`
Блок `manifest` після створення **не змінюється**.

Dispatcher, bridge, runner, QA, upload, approval helpers:
- **не мають права** змінювати `manifest`
- **не мають права** дописувати нові поля всередину `manifest`
- **не мають права** “підчищати”, “нормалізувати” або “покращувати” `manifest` заднім числом

Єдиний спосіб змінити manifest:
- створити **нову версію** через `manifest_version + 1`

### 2.2 Mutable zone — runtime envelope
Змінними є лише runtime-поля верхнього рівня `PROJECT_STATE.json`, які описують:
- поточну фазу
- історію фаз
- approval status
- QA status
- halt state
- timestamps
- посилання на артефакти

---

## 3. Канонічна структура `PROJECT_STATE.json`

Нижче наведено **мінімально обов’язкову** канонічну структуру.

```json
{
  "project_id": "P2026_0001",
  "phase": "TOPIC",
  "phase_history": [],
  "updated_at": "2026-03-31T00:00:00Z",
  "halted": false,
  "halt_reason": null,
  "resume_hint": null,
  "approval_status": "PENDING",
  "approved_for_upload": false,
  "qa_passed": false,
  "artifacts": {},
  "manifest": {
    "manifest_id": "P2026_0001:v1",
    "manifest_version": 1,
    "manifest_hash": "sha256:<computed_from_manifest_payload>",
    "mode": "cashflow-mode",
    "niche": "Money Mistakes / Invisible Costs",
    "audience": "Global English",
    "content_language": "en",
    "primary_platform": "youtube",
    "topic": "Example topic",
    "working_title": "Example working title",
    "hook": "Example hook",
    "target_duration_sec": 480,
    "render_profile": "ffmpeg_stability_standard_v1_2",
    "stock_policy": "stock_first_no_repeat",
    "created_at": "2026-03-31T00:00:00Z",
    "locked": true
  }
}
```

---

## 4. Обов’язкові поля верхнього рівня

Наступні поля є **обов’язковими** в `PROJECT_STATE.json`:

- `project_id`
- `phase`
- `phase_history`
- `updated_at`
- `halted`
- `halt_reason`
- `resume_hint`
- `approval_status`
- `approved_for_upload`
- `qa_passed`
- `artifacts`
- `manifest`

---

## 5. Обов’язкові поля всередині `manifest`

Наступні поля є **обов’язковими**:

- `manifest_id`
- `manifest_version`
- `manifest_hash`
- `mode`
- `niche`
- `audience`
- `content_language`
- `primary_platform`
- `topic`
- `working_title`
- `hook`
- `target_duration_sec`
- `render_profile`
- `stock_policy`
- `created_at`
- `locked`

---

## 6. Правила незмінності

Після створення manifest:

- `manifest.locked` має бути `true`
- `manifest_hash` має відповідати фактичному payload блоку `manifest`
- будь-яка зміна будь-якого поля всередині `manifest` без підвищення `manifest_version` є порушенням канону
- canonical dispatcher у майбутньому має вважати таку зміну **corruption / drift**

---

## 7. Що має право змінювати dispatcher

Canonical dispatcher має право змінювати лише runtime envelope:

- `phase`
- `phase_history`
- `updated_at`
- `halted`
- `halt_reason`
- `resume_hint`
- `approval_status`
- `approved_for_upload`
- `qa_passed`
- `artifacts`

Dispatcher **не має права** змінювати:
- будь-що в `manifest`

---

## 8. Що не мають права робити модулі

Жоден модуль production-ланцюга не має права:

- створювати альтернативний manifest-файл як нову правду
- переписувати `PROJECT_STATE.json.manifest`
- міняти `phase` напряму в обхід dispatcher
- робити rollback фази після assembly, якщо це суперечить dispatcher rules
- “автоматично виправляти” manifest без явного version bump

---

## 9. Правило повторного запуску

Повторний запуск того самого `project_id` допускається тільки через:

- новий `manifest_version`

Тобто:
- `P2026_0001:v1` → початковий запуск
- `P2026_0001:v2` → офіційний rerun
- `P2026_0001:v3` → наступний rerun

Повторний запуск **без** version bump є порушенням канону.

---

## 10. Правило сумісності з legacy-станом

Якщо старий `PROJECT_STATE.json`:
- не має `manifest`
- має неповний `manifest`
- має mutable-поля всередині `manifest`
- має кілька джерел правди

то такий стан вважається:

- **legacy / non-canonical**

Його не можна мовчки приймати як валідний canonical state.

Для таких кейсів має існувати окремий migration path, а не “автодомальовування” на льоту.

---

## 11. Rule of one truth

У `cashflow-mode` діє правило:

> Один `PROJECT_STATE.json`  
> Один `manifest` усередині нього  
> Один dispatcher як єдиний власник runtime transitions

Це є базовою умовою для:
- стабільності
- відновлення після збоїв
- auditable orchestration
- відсутності прихованого drift

---

## 12. Що буде реалізовано далі на основі цього spec

Наступна реалізація canonical dispatcher повинна забезпечити:

1. strict load/save `PROJECT_STATE.json`
2. validation required fields
3. manifest immutability check
4. drift detection через `manifest_hash`
5. заборону phase mutation поза dispatcher
6. version-aware rerun logic
7. deterministic transition logging

---

## 13. Lock rule

Цей документ вважається **LOCKED** до окремого явного commit, який:
- змінює саме spec
- має окремий spec-focused message
- не маскує зміну spec всередині випадкових code edits

Рекомендований формат майбутніх змін:
- `spec: update canonical manifest contract`
- `spec: revise manifest immutability rules`

---

## 14. Final canonical statement

Для `FlowMind_2026 / cashflow-mode` канон такий:

- `PROJECT_STATE.json` = runtime single source of truth
- `PROJECT_STATE.json.manifest` = immutable canonical manifest
- dispatcher = єдиний власник runtime transition logic
- rerun = тільки через `manifest_version + 1`
- будь-яка інша схема вважається non-canonical

---

**LOCKED**
