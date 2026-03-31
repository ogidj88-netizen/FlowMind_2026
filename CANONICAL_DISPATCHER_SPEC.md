# CANONICAL DISPATCHER SPEC

Останнє оновлення: 2026-03-31
Статус: TARGET SPEC
Призначення: канонічний контракт центрального мозку FlowMind

---

## 1. РОЛЬ

Canonical Dispatcher — це центральний мозок системи.

Він:
- читає стан проєкту
- визначає дозволений наступний крок
- запускає потрібний модуль
- оновлює стан
- блокує незаконні переходи
- зупиняє систему при помилці

Dispatcher НЕ генерує контент.
Dispatcher НЕ виконує production-логіку сам.
Dispatcher тільки керує маршрутом.

---

## 2. SINGLE SOURCE OF TRUTH

Єдине джерело правди:
`projects/<PROJECT_ID>/ExecutionManifest.json`

Dispatcher читає і оновлює тільки його.

---

## 3. ОБОВʼЯЗКОВІ ПОЛЯ MANIFEST

Мінімальний канонічний набір полів:

- project_id
- manifest_version
- status
- mode
- created_at
- updated_at
- halt_reason
- last_completed_stage
- next_allowed_stages
- rules
- artifacts
- manifest_hash

---

## 4. КАНОНІЧНА МОДЕЛЬ СТАНУ

Dispatcher працює через поле:

`status`

Не через:
`current_phase`

---

## 5. КАНОНІЧНІ СТАТУСИ

- CREATED
- S1_DONE
- S2_DONE
- S5_DONE
- S6_DONE
- S7_DONE
- S8_DONE
- S9_DONE
- S10_DONE
- HALTED
- FAILED

---

## 6. КАНОНІЧНІ STATIONS

- S1 Strategy
- S2 Script
- S5 Assets
- S6 Visual
- S7 Audio
- S8 Assembly
- S9 Thumbnail
- S10 QA

---

## 7. ПРАВИЛО МОЗКУ

Dispatcher не йде по сліпому ланцюгу.

Dispatcher:
- читає status
- читає rules
- перевіряє artifacts
- визначає, який етап дозволений
- запускає тільки дозволений модуль
- блокує все незаконне

---

## 8. КОМАНДИ DISPATCHER

Потрібні команди:

- create
- advance
- rerun
- halt
- resume
- status

---

## 9. ПРАВИЛА ADVANCE

advance дозволений тільки якщо:
- попередній обов’язковий етап завершений
- потрібні артефакти існують
- немає halt/failed блокування
- наступний статус входить у список allowed transitions

---

## 10. ПРАВИЛА HALT

Dispatcher переводить проект у HALTED якщо:
- модуль повернув non-zero exit code
- відсутній обов’язковий артефакт
- status transition незаконний
- manifest невалідний

---

## 11. ПРАВИЛА SUCCESS

Етап вважається успішним тільки якщо:
- модуль завершився без помилки
- створений очікуваний артефакт
- manifest успішно оновлений
- зафіксований новий status

---

## 12. ПРАВИЛА МІГРАЦІЇ

Dispatcher будується під нову чисту систему,
але нумерація станцій має залишатися сумісною
з уже наявними артефактами та contract-pipeline.

Тому:
- S1, S2, S5, S6, S7, S8, S9, S10 — канонічні
- нова логіка не повинна ламати існуючу нумерацію без окремого migration-plan

---

## 13. ЩО ЗАБОРОНЕНО

ЗАБОРОНЕНО:
- кілька dispatcher-ів як рівноправні
- current_phase як друга модель стану
- прямий перезапис manifest без locked writer
- запуск наступного етапу без перевірки артефакту попереднього
- змінювати нумерацію станцій без окремого migration-plan

---

## 14. ЦІЛЬ

Після реалізації Canonical Dispatcher має стати
єдиним центром керування нової чистої системи.
