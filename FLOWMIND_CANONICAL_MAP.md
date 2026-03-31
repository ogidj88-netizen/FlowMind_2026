# FLOWMIND CANONICAL MAP

Останнє оновлення: 2026-03-31
Статус документа: КАНОНІЧНА МАПА СИСТЕМИ
Призначення: єдина точка звірки реального стану FlowMind

---

## 1. ПРАВИЛА СТАТУСІВ

- ПІДТВЕРДЖЕНО = модуль або шар фізично існує і має сильні ознаки реального використання
- ЧАСТКОВО = щось існує, але завершення або підключення не підтверджене
- LEGACY / ЗМІШАНО = старий або паралельний шар, який може плутати архітектуру
- НЕ ПІДТВЕРДЖЕНО = немає достатніх фактів вважати модуль готовим

---

## 2. ГОЛОВНИЙ ВИСНОВОК

FlowMind зараз НЕ є повністю завершеним продакшн-пайплайном.

Поточний реальний стан:
- є живий entrypoint;
- є dispatcher;
- є manifest-дисципліна;
- є фазовий JSON-contract pipeline;
- немає підтвердження повного runtime для генерації медіа, upload і Telegram.

---

## 3. ЖИВЕ ЯДРО (ПІДТВЕРДЖЕНО)

| Елемент | Статус | Коментар |
|---|---|---|
| main.py | ПІДТВЕРДЖЕНО | Єдиний entrypoint |
| dispatcher/engine.py | ПІДТВЕРДЖЕНО | Живий dispatcher |
| ExecutionManifest.json | ПІДТВЕРДЖЕНО | Основа запуску проектів |
| PHASE ORDER S1→S2→S5→S6→S7→S8→S9→S10 | ПІДТВЕРДЖЕНО | Зафіксовано в dispatcher |
| projects/* | ПІДТВЕРДЖЕНО | Є багато реальних manifest/project артефактів |

---

## 4. PRODUCTION-LAYER (ЧАСТКОВО, АЛЕ ЖИВИЙ)

| Етап | Статус | Реальний зміст |
|---|---|---|
| S1_strategy | ЧАСТКОВО | Генерує JSON-стратегію |
| S2_script | ЧАСТКОВО | Генерує JSON-скрипт |
| S5_assets | ЧАСТКОВО | Генерує assets contract |
| S6_visual | ЧАСТКОВО | Генерує visual contract |
| S7_audio | ЧАСТКОВО | Генерує audio contract |
| S8_assembly | ЧАСТКОВО | Генерує assembly contract |
| S9_thumbnail | ЧАСТКОВО | Генерує thumbnail contract |
| S10_qa | ЧАСТКОВО | Потребує окремої перевірки, але входить у ланцюг |

Висновок:
production/ = реальний робочий контрактний pipeline,
але НЕ підтверджений як повна бойова медіа-генерація.

---

## 5. ENGINE-LAYER (LEGACY / ПЕРЕХІДНИЙ)

| Елемент | Статус | Коментар |
|---|---|---|
| engine/module_runner.py | LEGACY / ПЕРЕХІДНИЙ | Працює лише з S1 і S2 |
| engine/modules/s1_strategy.py | LEGACY / STUB | Прямо позначений як Stub v1 |
| engine/modules/s2_script.py | LEGACY / ПЕРЕХІДНИЙ | Є, але не канонічний повний pipeline |

Висновок:
engine/ не є повним живим ядром системи.

---

## 6. CASHFLOW-LAYER (НЕ ПІДТВЕРДЖЕНО ЯК RUNTIME)

| Елемент | Статус | Коментар |
|---|---|---|
| cashflow/modules/topic | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/script | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/audio | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/scene | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/visual | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/thumbnail | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/qa | НЕ ПІДТВЕРДЖЕНО | Папка пуста |
| cashflow/modules/upload | НЕ ПІДТВЕРДЖЕНО | Папка пуста |

Висновок:
cashflow/ зараз не є живим runtime-шаром.

---

## 7. АРТЕФАКТНИЙ ДОКАЗ

Приклад:
projects/FM_AUDIO_TEST містить:
- ExecutionManifest.json
- S1_strategy.json
- S2_script.json
- S5_assets.json
- S6_visual.json
- S7_audio.json
- S8_assembly.json
- S9_thumbnail.json
- S10_qa.json

Це підтверджує, що контрактний ланцюг реально проганявся end-to-end.

---

## 8. НЕ ПІДТВЕРДЖЕНО

| Елемент | Статус | Коментар |
|---|---|---|
| PROJECT_STATE.json як live runtime | НЕ ПІДТВЕРДЖЕНО | Пошук не знайшов |
| Telegram runtime | НЕ ПІДТВЕРДЖЕНО | Пошук не знайшов |
| Upload runtime | НЕ ПІДТВЕРДЖЕНО | Поки немає доказу |
| Реальний media render | НЕ ПІДТВЕРДЖЕНО | Є assembly contract, але не доведено бойовий рендер |
| Повний IronCore stack у коді | НЕ ПІДТВЕРДЖЕНО | Є master prompt, але не реальний audited runtime |

---

## 9. ПОТОЧНА ПОЗИЦІЯ

Поточний етап:
АУДИТ ЗАВЕРШЕНО — ЗАФІКСОВАНО РЕАЛЬНИЙ СТАН

Наша ціль далі:
1. не чіпати живе ядро навмання;
2. відділити contract pipeline від реальної media-production;
3. вирішити, що канон: добудова production-layer чи контрольована міграція.

---

## 10. ГОЛОВНЕ ПРАВИЛО НАДАЛІ

Жоден модуль не вважається завершеним, поки не підтверджено:
- код існує;
- він реально підключений;
- він виконує не лише запис JSON-контракту, а потрібну фактичну функцію.
---

## 11. SPLIT-BRAIN ПРОБЛЕМА (НОВИЙ ФАКТ)

У системі виявлено розрив між entrypoint і phase executor.

### Підтверджено:
- `main.py` викликає `dispatcher/engine.py`
- `dispatcher/engine.py` у перевіреному вигляді містить manifest/state логіку, але не показаний як явний executor фаз
- `dispatcher/engine_v16.py` містить логіку:
  - вибір `module_path` через `PHASE_MAP`
  - `run_module(module_path, project_id)`
  - `update_phase(project_id, next_phase)`

### Висновок:
Найімовірніше, `dispatcher/engine_v16.py` є реальним phase executor,
але `main.py` досі спрямований на `dispatcher/engine.py`.

### Ризик:
Це створює split-brain архітектуру:
- один файл виглядає як entry dispatcher
- інший файл виглядає як реальний executor

### Правило:
До моменту явного виправлення маршруту запуску
ЗАБОРОНЕНО:
- чистити legacy-шари
- переносити production-модулі
- змінювати pipeline-структуру

Спочатку треба:
1. зафіксувати канонічний dispatcher
2. тільки потім переводити main.py на єдиний маршрут
---

## 12. MANIFEST / DISPATCHER BREAKPOINT

Під час аудиту підтверджено:

### manifest_engine/engine.py
Містить тільки:
- compute_hash
- _write_json_locked
- create_immutable_manifest

Тобто цей модуль зараз відповідає тільки за:
- створення manifest
- locked write
- hash

### Критична невідповідність
dispatcher/engine_v16.py імпортує:
- load_manifest
- update_phase

Але в manifest_engine/engine.py цих функцій у перевіреному коді немає.

### Висновок
engine_v16.py не може вважатися робочим канонічним dispatcher у поточному стані.

### Правило
ЗАБОРОНЕНО:
- переводити main.py на engine_v16.py
- вважати engine_v16.py живим dispatcher
- робити рефакторинг dispatcher-шару до завершення аудиту dispatcher/engine.py
