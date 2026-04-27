# FLOWMIND CANONICAL ARCHITECTURE V1

Status: CANONICAL TARGET ARCHITECTURE
Scope: цільова архітектура FlowMind
Master location: GitHub repo / docs
Updated: 2026-04

---

## 1. Purpose

Цей документ фіксує, як FlowMind має бути побудований у канонічному вигляді.

Це не фактична карта поточного стану repo.

Цей документ відповідає на питання:

- яка правильна структура системи;
- хто приймає рішення;
- які модулі виконують роботу;
- де стоять перевірки;
- де потрібна участь Євгена;
- яка послідовність роботи системи;
- що вважається першим реальним milestone.

---

## 2. Core model

FlowMind будується навколо однієї центральної моделі:

Brain Core приймає рішення.
Модулі виконують контракти.
QA блокує погане.
Dispatcher керує фазами.
Євген погоджує тільки критичні точки.

Пояснення термінів:

- Brain Core — центральний мозок системи.
- Module — модуль-виконавець.
- Contract — правила входу, виходу і якості для модуля.
- QA — перевірка якості.
- Dispatcher — керує переходами між фазами.
- HALT — жорстка зупинка системи.
- PASS — артефакт пройшов перевірку.
- FAIL — артефакт не пройшов перевірку.
- Output — результат роботи модуля.
- Runtime — фактичне виконання системи.
- Milestone — контрольна ціль.

---

## 3. Main operating flow

Канонічна послідовність роботи FlowMind:

Ніша
→ Дослідження
→ Тема
→ Сценарій
→ Режисерський план
→ Візуали
→ Озвучка
→ Монтаж
→ QA
→ Погодження Євгеном
→ Публікація або архів

Коротка технічна схема:

Brain Core
→ Research Module
→ Topic Module
→ Script Module
→ Director Module
→ Assets Module
→ Voice Module
→ Assembly Module
→ QA Module
→ Human Approval
→ Upload / Archive

---

## 4. Brain Core

Brain Core — це єдиний продуктивний мозок системи.

Brain Core відповідає за:

- аналіз ніші;
- оцінку якості джерел;
- вибір теми;
- вибір кута подачі;
- сценарну логіку;
- режисерський задум;
- бізнес-пріоритет;
- ROI / impact оцінку;
- рішення зупинити систему через HALT;
- фінальну логіку перед виконанням.

Brain Core не має права:

- створювати нові модулі під час runtime без рішення;
- обходити контракти;
- обходити Dispatcher;
- приймати слабкий output заради прогресу;
- вигадувати факти;
- вигадувати джерела;
- нескінченно аналізувати без переходу до виконання;
- підміняти runtime-докази думками.

Brain Core може мати режими мислення, але це не окремі агенти:

- Research mode — режим дослідження.
- Topic mode — режим вибору теми.
- Script mode — режим сценарію.
- Director mode — режим режисерського рішення.
- QA reasoning mode — режим оцінки якості.
- Business mode — режим ROI / бізнес-оцінки.

Режими мислення не є окремими центрами керування.

---

## 5. Module rule

Модулі — це прості виконавці контрактів.

Кожен модуль має:

- input contract — що модуль отримує;
- output contract — що модуль має повернути;
- validation rule — як перевірити результат;
- fail condition — коли модуль має впасти;
- artifact path — де лежить результат;
- log/check result — доказ виконання.

Модуль повертає тільки один із двох результатів:

VALID_ARTIFACT

або:

FAIL + reason + resume_hint

Пояснення:

- VALID_ARTIFACT — валідний результат.
- reason — причина помилки.
- resume_hint — підказка, як продовжити після виправлення.

Модулі не мають права:

- приймати стратегічні рішення;
- змінювати архітектуру;
- вигадувати джерела;
- генерувати fake-output;
- silently repair — тихо виправляти невалідні дані;
- переходити між фазами напряму;
- обходити QA;
- обходити Dispatcher.

---

## 6. Dispatcher

Dispatcher — єдиний контролер фаз.

Dispatcher відповідає за:

- phase transition — перехід між фазами;
- HALT — зупинку системи;
- resume — відновлення після зупинки;
- заборону unsafe rollback — небезпечного відкату назад;
- readiness check — перевірку готовності до наступного етапу.

Жоден модуль не може самовільно змінювати фазу системи.

Усі переходи мають проходити через Dispatcher або через явно дозволений dispatcher-controlled шлях.

---

## 7. QA

QA — це блокувальний шар, а не творчий модуль.

QA перевіряє:

- схему файлів;
- повноту артефактів;
- якість джерел;
- фактичну коректність;
- якість сценарію;
- відповідність сценарію відео;
- наявність аудіо;
- наявність відео;
- відсутність black frames;
- відсутність placeholder/stub/fake output;
- готовність до наступної фази.

QA може повернути:

PASS
FAIL
HALT

QA не має права:

- тихо виправляти поганий результат;
- пропускати слабкий output заради прогресу;
- приймати fake-output;
- приймати production placeholder;
- замінювати перевірку смаком.

---

## 8. Human approval

Євген втручається тільки в критичних точках.

### Gate 1 — Niche / Base Data Approval

Контрольна точка на старті нової ніші.

Євген погоджує:

- нішу;
- аудиторію;
- напрям;
- контентну обіцянку;
- заборонені кути;
- правила джерел;
- базову бізнес-логіку;
- ROI-гіпотезу.

### Gate 2 — Final Preview / Video Approval

Контрольна точка перед публікацією.

Євген погоджує:

- preview / thumbnail;
- фінальне відео;
- назву;
- опис;
- package для публікації;
- upload decision.

### Gate 3 — Emergency HALT Review

Аварійна точка.

Євген втручається, якщо:

- система зупинилась через HALT;
- QA заблокував output;
- confidence низький;
- потрібне рішення: retry, fix, archive або stop.

---

## 9. Canonical phases

### Phase 0 — Niche Profile

Мета: створити робочий профіль ніші.

Input:

- broad niche idea — широка ідея ніші;
- business goal — бізнес-мета;
- target audience — цільова аудиторія.

Output:

- NICHE_PROFILE.json

Має містити:

- опис ніші;
- аудиторію;
- головний біль аудиторії;
- content promise — що відео обіцяють глядачу;
- source policy — правила джерел;
- forbidden angles — заборонені кути;
- monetization / ROI logic — бізнес-логіка;
- topic selection rules — правила вибору тем.

Validation:

- ніша достатньо конкретна;
- аудиторія зрозуміла;
- біль аудиторії чіткий;
- джерела визначені;
- ROI-гіпотеза є.

Human approval:

- required.

---

### Phase 1 — Research Pack

Мета: зібрати докази, джерела і сигнали попиту.

Input:

- NICHE_PROFILE.json

Output:

- RESEARCH_PACK.json

Має містити:

- authoritative sources — авторитетні джерела;
- web evidence — докази з інтернету;
- social demand signals — сигнали попиту з Reddit / YouTube / Trends / пошуку;
- source credibility notes — оцінку довіри до джерел;
- contradiction notes — суперечності;
- risk notes — ризики.

Validation:

- немає unsupported claims — непідтверджених тверджень;
- джерела простежувані;
- є сигнал попиту;
- слабкі джерела позначені;
- clickbait не приймається як доказ.

Human approval:

- not required by default.
- required only if confidence is low.

---

### Phase 2 — Topic Selection

Мета: вибрати найкращу тему з research pack.

Input:

- NICHE_PROFILE.json
- RESEARCH_PACK.json

Output:

- TOPIC_BRIEF.json

Має містити:

- selected topic — обрана тема;
- why now — чому зараз;
- audience pain — біль аудиторії;
- emotional hook — емоційний гачок;
- evidence summary — короткий доказовий підсумок;
- uniqueness angle — унікальний кут;
- risk score — оцінка ризику;
- expected video promise — що відео дасть глядачу.

Validation:

- тема має попит;
- тема має джерела;
- тема не generic — не банальна;
- є video potential — потенціал для відео;
- є emotional hook;
- не базується на fake evidence.

Human approval:

- not required by default.

---

### Phase 3 — Script

Мета: створити сильний сценарій.

Input:

- TOPIC_BRIEF.json

Output:

- SCRIPT.md або SCRIPT.json

Має містити:

- hook — стартовий гачок;
- escalation — наростання;
- proof points — доказові точки;
- story flow — логіку історії;
- payoff — цінний висновок;
- ending — фінал;
- viewer value — користь для глядача.

Validation:

- немає непідтверджених фактів;
- немає filler — води;
- hook сильний;
- логіка не ламається;
- duration target витримано;
- джерела не спотворені;
- сценарій не звучить як generic AI text.

Human approval:

- optional during calibration.
- not required after stable quality.

---

### Phase 4 — Director Plan

Мета: перетворити сценарій на виробничий план.

Input:

- SCRIPT

Output:

- DIRECTOR_PLAN.json

Має містити:

- scene list — список сцен;
- shot intent — задум кадру;
- visual rhythm — візуальний ритм;
- asset needs — потреби у візуалах;
- voice pacing — темп озвучки;
- b-roll requirements — додаткові кадри;
- text overlay needs — текст на екрані;
- emotional arc — емоційна дуга.

Validation:

- кожен сегмент сценарію має visual intent;
- немає неможливих вимог;
- таймінг логічний;
- downstream modules можуть виконати план;
- не створює зайвої складності.

Human approval:

- not required.

---

### Phase 5 — Assets

Мета: зібрати або створити візуали.

Input:

- DIRECTOR_PLAN.json

Output:

- ASSET_PACK.json

Policy:

- stock-first на старті;
- AI augmentation тільки контрольовано;
- fake evidence заборонено;
- irrelevant visuals заборонено.

Validation:

- усі сцени мають assets;
- assets відповідають intent;
- немає repeated visual spam;
- немає broken file paths;
- є source/license metadata;
- немає production placeholders.

Human approval:

- not required unless visual confidence is low.

---

### Phase 6 — Voice

Мета: створити озвучку.

Input:

- SCRIPT

Output:

- voice audio file;
- VOICE_REPORT.json

Canonical provider:

- ElevenLabs через контракт.

Validation:

- audio file exists;
- файл не порожній;
- duration у допустимому діапазоні;
- формат підходить для assembly;
- немає obvious truncation — явного обрізання.

Human approval:

- not required.

---

### Phase 7 — Assembly / Render

Мета: зібрати фінальне відео.

Input:

- SCRIPT
- DIRECTOR_PLAN.json
- ASSET_PACK.json
- voice audio file.

Output:

- final.mp4
- RENDER_REPORT.json

Canonical render path:

- FFmpeg зараз.
- Remotion later тільки після стабільного FFmpeg pipeline.

Validation:

- video exists;
- audio exists;
- duration valid;
- немає black frame failure;
- render completed;
- output path registered;
- state updated only through allowed path.

Human approval:

- not required.

---

### Phase 8 — Final QA

Мета: заблокувати слабкий або невалідний output.

Input:

- final video;
- all reports;
- state.

Output:

- QA_REPORT.json

Validation:

- factual consistency;
- source integrity;
- audio/video integrity;
- script-to-video alignment;
- placeholder scan;
- production readiness;
- state validity;
- no fake output.

Result:

- PASS → preview approval.
- FAIL → HALT.
- HALT → requires reason + resume_hint.

Human approval:

- only after QA PASS.

---

### Phase 9 — Preview / Package Approval

Мета: погодити публікаційний пакет.

Input:

- final video;
- thumbnail / preview;
- title;
- description;
- tags if available.

Output:

- approval decision.

Human approval:

- required.

---

### Phase 10 — Upload / Archive

Мета: опублікувати або заархівувати результат.

Input:

- approved final package.

Output:

- upload receipt або archive result.

Validation:

- upload success або archive success;
- metadata saved;
- state updated;
- no silent failure.

Human approval:

- required before upload until the system proves reliability.

---

## 10. Minimal working milestone

Перший реальний milestone:

topic → script → voice → video → QA PASS

Українською:

тема → сценарій → озвучка → відео → перевірка якості PASS

Upload не входить у перший milestone.

Milestone вважається виконаним тільки якщо:

- final video exists;
- QA PASS;
- no placeholders;
- state valid;
- результат можна повторити;
- є runtime log;
- є commit/push, якщо були зміни коду.

---

## 11. Niche model

FlowMind має бути універсальною системою з профілями ніш.

Не жорстко під одну нішу.

Кожна ніша має власний:

- NICHE_PROFILE.json
- source policy;
- audience model;
- topic rules;
- forbidden angles;
- monetization assumptions;
- quality rules.

Система не має бути переписана під кожну нову нішу.

Міняється профіль ніші, а не архітектура.

---

## 12. Source hierarchy

Master truth:

GitHub repo / docs

Operational copies можуть існувати в:

- ChatGPT Project / Sources;
- Google Drive;
- Business workspace.

Якщо є конфлікт:

repo docs win

Українською:

документи в repo мають вищу силу

---

## 13. Placeholder rule

Production placeholders, stubs, fake outputs, fake data, fake sources і fake validation заборонені.

Test fixtures дозволені тільки якщо:

- вони поза active production path;
- мають marker NON_PRODUCTION_FIXTURE;
- мають replacement rule;
- production/preflight scan блокує їх появу в active path.

Fixture — це тестовий артефакт для перевірки інфраструктури.
Він не може бути реальним production output.

---

## 14. Component status

Кожен компонент має один статус:

ACTIVE
DONOR
ARCHIVE
BROKEN
IDEA
UNKNOWN

Пояснення:

- ACTIVE — працює в поточному контурі.
- DONOR — можна взяти корисне після аудиту.
- ARCHIVE — історія, не джерело істини.
- BROKEN — відомо невалідне, не використовувати.
- IDEA — ідея, не активна робота.
- UNKNOWN — не чіпати без аудиту.

Неможна змішувати ACTIVE, DONOR і ARCHIVE в одному рішенні.

---

## 15. Business integration rule

ChatGPT Business, Skills, GPTs, Connectors і Google Drive структура вводяться тільки після:

1. canonical architecture exists;
2. active system map exists;
3. current repo state is classified;
4. minimal working path is defined.

Business tools support the system.
They do not replace repo truth.

Українською:

Інструменти Business допомагають системі, але не стають джерелом істини.

---

## 16. Canonical summary

Коротка схема:

Brain Core
  ↓
Research Module
  ↓
Topic Module
  ↓
Script Module
  ↓
Director Module
  ↓
Assets Module
  ↓
Voice Module
  ↓
Assembly Module
  ↓
QA Module
  ↓
Human Approval
  ↓
Upload / Archive

Українською:

Центральний мозок
  ↓
Дослідження
  ↓
Вибір теми
  ↓
Сценарій
  ↓
Режисерський план
  ↓
Візуали
  ↓
Озвучка
  ↓
Монтаж
  ↓
Перевірка якості
  ↓
Погодження Євгеном
  ↓
Публікація або архів

---

## 17. Non-goals for current stage

На поточному етапі не робимо:

- повний autopilot без людини;
- автоматичний upload;
- Remotion як основний render path;
- agent-зоопарк;
- Business workspace як source of truth;
- Skills до active system map;
- нові production modules без карти;
- складну оптимізацію до first milestone.

---

## 18. Final rule

FlowMind не має бути системою, яка постійно аналізує сама себе.

FlowMind має бути системою, яка:

1. думає якісно;
2. виконує просто;
3. перевіряє жорстко;
4. зупиняється при невалідності;
5. виробляє валідний output.
