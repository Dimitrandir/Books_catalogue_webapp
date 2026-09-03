# Лог на сесиите

Този файл се обновява в края на всяка работна сесия по проекта — какво е
свършено, какво е текущото състояние, и каква е следващата стъпка. Целта е
следващата сесия (или следващият Claude Code разговор) да може бързо да се
ориентира докъде сме стигнали, без да препрочита цялата история.

Нов запис се добавя най-отдолу, в обратен хронологичен ред няма нужда —
просто append.

Формат на всеки запис:

```
## YYYY-MM-DD

**Свършено:**
- ...

**Текущо състояние:**
- ...

**Следваща стъпка:**
- ...

**Отворени въпроси / бележки:** (по желание)
- ...
```

---

## 2026-08-31

**Свършено:**
- Прегледани всички файлове в проекта: `CLAUDE.md`, `docs/DATA_MODEL.md`,
  `README.md`, `requirements.txt`, `.env.example`.
- Създаден този файл (`docs/SESSIONS.md`) за проследяване на прогреса
  между сесии.

**Текущо състояние:**
- Проектът е само на ниво планиране/документация. Няма още Django
  project скеле — липсва `manage.py`, липсват `catalog`/`loans`/`scanner`
  apps, няма database connection, няма models.py.
- `requirements.txt` е дефиниран (Django, psycopg2-binary, python-dotenv,
  django-storages[s3], Pillow, django-htmx, anthropic, requests).
- `.env.example` е дефиниран с плейсхолдъри за Django, PostgreSQL,
  Cloudflare R2 и Anthropic API.
- Пълният модел на данните е фиксиран в `docs/DATA_MODEL.md` (Book, Copy,
  Loan, Author, Genre, Publisher, Location, Condition, Person).
- Проектната директория не е git repo все още.

**Следваща стъпка:**
- Точка 1 от "Ред на разработка" в `CLAUDE.md`: Django project setup +
  връзка към PostgreSQL (локално или dev instance).
- След това: `catalog` app с models + Django admin регистрация
  (включително seed на "Добро" в `Condition`).

**Отворени въпроси / бележки:**
- Няма още решение за конкретен PostgreSQL instance (локален Docker vs.
  managed dev instance) — за изясняване в следваща сесия.
- `git init` не е направен — да се обмисли в началото на следващата сесия.

---

## 2026-08-31 (продължение)

**Свършено:**
- Git repo инициализиран (`master` branch), направен initial commit с
  документацията/конфигурацията (без `files.zip` — той е дублиращ бекъп
  архив на вече тракнати файлове, оставен извън git).
- Локален PostgreSQL 16 намерен на машината; свързахме се с потребителска
  роля `stora_usr` (същата, използвана в другите проекти на потребителя).
  Създадена база `family_library` с owner `stora_usr`.
- Поправен несъответстващ pin в `requirements.txt` (`Django>=5.0,<6.0` →
  `Django>=5.0`) — venv-ът вече имаше Django 6.1 инсталиран, а CLAUDE.md
  иска последна стабилна версия.
- Инсталирани всички зависимости от `requirements.txt` в `.venv`, плюс
  `dj-database-url` (добавен в requirements) за чист parsing на
  `DATABASE_URL`.
- Създаден Django project `config/` (`django-admin startproject` първо
  случайно хвана системен Django 4.2.11 от `/usr/bin/django-admin` вместо
  venv-ния Django 6.1 — коригирано чрез `python -m django startproject`
  след изтриване на грешния скелет).
- `config/settings.py` пренаписан: чете `.env` през `python-dotenv`,
  `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS` от env vars, `DATABASES` през
  `dj_database_url.parse(DATABASE_URL)`, добавени `django.contrib.postgres`
  и `django_htmx` (app + middleware) в `INSTALLED_APPS`.
- Създадени трите apps: `catalog`, `loans`, `scanner` (все още без
  реални models — само скелето от `startapp`).
- Реален `.env` файл създаден локално (gitignored) с генериран
  `DJANGO_SECRET_KEY` и работещ `DATABASE_URL` за `family_library`.
- Проверено end-to-end: `manage.py check`, `manage.py migrate` (приложи
  admin/auth/contenttypes/sessions миграциите към `family_library`), и
  `manage.py runserver` — `/admin/login/` отговори с HTTP 200.
- Втори commit с целия scaffold (config + catalog/loans/scanner apps).

**Текущо състояние:**
- Django проектът е напълно функционален локално: свързан е с реална
  PostgreSQL база (`family_library`, роля `stora_usr`), admin login
  страницата работи, apps-ите съществуват но без models.
- `manage.py` командите трябва да се пускат през venv-ния Python
  (`source .venv/bin/activate && python manage.py ...` или директно
  `.venv/bin/python manage.py ...`) — системният `django-admin` в PATH
  сочи към различна (по-стара) Django инсталация, затова да НЕ се ползва
  голият `django-admin` в тази среда.
- Git repo е инициализиран, 2 commit-а на `master`.

**Следваща стъпка:**
- Точка 2 от "Ред на разработка" в `CLAUDE.md`: models.py за `catalog`
  app (`Author`, `Genre`, `Publisher`, `Location`, `Condition`, `Book`,
  `Copy`) по `docs/DATA_MODEL.md`, плюс Django admin регистрация.
- После: `loans` app models (`Person`, `Loan`).
- После: migrations + seed на "Добро" в `Condition` (data migration или
  `get_or_create`, default сочещ по `name` а не по твърд `pk`).

**Отворени въпроси / бележки:**
- `DJANGO_ALLOWED_HOSTS`/`DEBUG` са настроени за local dev (localhost,
  127.0.0.1, DEBUG=True) — да се преразгледат при деплой.
- R2/Anthropic API credentials в `.env` са все още празни — не е нужно
  докато не стигнем до upload на корици (стъпка 6) и scanner app
  (стъпка 7).

---

## 2026-08-31 (продължение 2)

**Свършено:**
- Оправен `CLAUDE.md`, който на диска се беше объркал форматирано (headers/
  code fences/списъци бяха сплескани в plain text с накъсани line breaks) —
  съдържанието е същото, само маркдаунът е възстановен. Добавена е и нова
  секция "Стил на общуване" от потребителя: отговори кратко и по същество,
  без излишни любезности.
- `catalog/models.py`: добавени всички справочни модели (`Author`, `Genre`,
  `Publisher`, `Location`, `Condition` — с `unique=True` на `name` и
  подредба по `name`), плюс `Book` (M2M към `Author`/`Genre`, FK към
  `Publisher` nullable, `cover_image` ImageField nullable/blank за upload
  по-късно) и `Copy` (FK към `Book`/`Location`/`Condition`, `condition`
  default през `default_condition()` — `get_or_create(name='Добро')`, т.е.
  сочи по `name`, не по твърд `pk`, както изисква `docs/DATA_MODEL.md`).
- `catalog/admin.py`: регистрирани всички модели — общ `ReferenceAdmin` за
  петте справочни модела, `BookAdmin` с `filter_horizontal` за M2M-нетата и
  inline за `Copy`, отделен `CopyAdmin`.
- `makemigrations catalog` → прегледана `0001_initial.py` преди `migrate`
  (следвайки конвенцията в `CLAUDE.md`) → приложена към `family_library`.
- Sanity-test през `manage.py shell`: създадени и изтрити тестови Author/
  Book/Location/Copy записи, потвърдено че `Copy.condition` default пада
  на "Добро" правилно.

**Текущо състояние:**
- `catalog` app вече има пълния набор модели от `docs/DATA_MODEL.md` (без
  `Person`/`Loan`, които са в бъдещия `loans` app). Admin интерфейсът е
  напълно функционален за тях.
- Все още няма custom views/templates — само Django admin.

**Следваща стъпка:**
- Точка от плана: `loans` app models (`Person`, `Loan`) + admin
  регистрация, по `docs/DATA_MODEL.md`.
- След това: основни custom изгледи (списък с книги, детайли, търсене/
  филтриране) — точка 4 от "Ред на разработка" в `CLAUDE.md`.

**Отворени въпроси / бележки:**
- Не е създаден Django superuser все още — ще трябва за реален достъп до
  `/admin/` (`python manage.py createsuperuser`).

---

## 2026-08-31 (продължение 3)

**Свършено:**
- `loans/models.py`: `Person` (справочен модел, `name` unique, `__str__`
  връща `name`) и `Loan` (FK към `catalog.Copy` и `loans.Person`,
  `date_given` DateField, `date_returned` nullable/blank — текущо "на заем"
  състояние = последен `Loan` за `Copy` с `date_returned IS NULL`, per
  `docs/DATA_MODEL.md`). `Loan.__str__` показва статус ("на заем"/"върната").
- `loans/admin.py`: `PersonAdmin` + `LoanAdmin` с `autocomplete_fields` за
  `copy`/`person` (изисква `search_fields` в `CopyAdmin`/`PersonAdmin`,
  вече налични).
- `makemigrations loans` → прегледана `0001_initial.py` (dependency към
  `catalog.0001_initial`) → приложена към `family_library`.
- Sanity-test през shell: създаден/върнат тестов `Loan`, проверено че
  `date_returned` update-ва статуса в `__str__`, тестовите данни изтрити.

**Текущо състояние:**
- И двата основни app-а (`catalog`, `loans`) вече имат пълния модел на
  данните от `docs/DATA_MODEL.md`. Admin е напълно функционален за CRUD
  на всичко: Author/Genre/Publisher/Location/Condition/Book/Copy/Person/Loan.
- `scanner` app е все още празен (само `startapp` скелето) — идва по-късно
  (стъпка 7 от плана).
- Все още няма custom views/templates отвъд Django admin.

**Следваща стъпка:**
- Точка 4 от "Ред на разработка" в `CLAUDE.md`: основни custom изгледи —
  списък с книги, детайли за книга, търсене/филтриране (PostgreSQL
  full-text search през `django.contrib.postgres.search`, вече в
  `INSTALLED_APPS`).
- Преди това вероятно си струва `createsuperuser` + малко seed данни за да
  има какво да се показва в списъка.

**Отворени въпроси / бележки:**
- Пак: няма superuser все още.

---

## 2026-08-31 (продължение 4)

**Свършено:**
- Потребителят вече е създал Django superuser.
- Точка 4 от плана: основни custom изгледи в `catalog`:
  - `book_list` — грид с корици, GET-базирана търсачка + филтри (Genre,
    Author, Publisher, Location, наличност), пагинация (24/страница).
    Търсене: PostgreSQL full-text (`SearchVector`/`SearchRank` върху
    `title`+`summary`, config `'simple'` — без stemming, работи и за
    български текст) `OR` icontains по `authors__name`.
  - `book_detail` — инфо за книгата + таблица с всички `Copy` (локация,
    състояние, текущ статус на заем, пълна история на заемания).
  - `catalog/urls.py` нов, включен в `config/urls.py` на root; admin
    остава на `/admin/`.
- HTMX: филтър формата и пагинацията правят `hx-get` към същия list view;
  view-ът различава `request.htmx` (django-htmx middleware) и връща само
  partial (`_book_results.html`) вместо цялата страница — без пълен
  reload при търсене/филтриране/пагинация.
- `config/settings.py`: добавени `MEDIA_URL`/`MEDIA_ROOT` (локален диск за
  сега — R2 идва в стъпка 6), `TEMPLATES.DIRS` за общ `templates/base.html`,
  и `LANGUAGE_CODE`/`TIME_ZONE` сменени от `en-us`/`UTC` на `bg`/
  `Europe/Sofia` (открито при ръчния тест — датите излизаха на английски,
  напр. "Aug. 1, 2026" вместо "01 Август 2026").
- Открит и оправен логически бъг в availability филтъра по време на
  ръчното тестване: първоначалната имплементация на "Дадени на заем"
  изискваше **всички** екземпляри на книгата да са на заем (заради
  `exclude(copies__in=...)` семантиката на Django за many-to-many), вместо
  по-интуитивното "поне един екземпляр в момента на заем". Оправено с
  отделен `_on_loan_copies()` helper и симетрична `filter()` логика и за
  двата случая (available/on_loan).
- Ръчно тествано в браузър с временни seed данни (2 книги, 2 автора, 2
  локации, 1 заем): списък, детайли, search по заглавие/автор/резюме,
  всеки филтър поотделно, htmx behavior (network requests потвърждават
  ajax swap, не full navigation). Seed данните изтрити след теста —
  базата `family_library` е чиста.

**Текущо състояние:**
- Функционален MVP: Django admin за CRUD + custom UI за преглед/търсене/
  филтриране на книги. Няма още UI за заемане/връщане (loans действия) —
  само преглед на статус в детайлите. Няма upload на корица извън admin.
- Визуалният дизайн е нарочно минимален inline CSS в `templates/base.html`
  — истинският дизайн предстои по-късно с `frontend-design` skill-а
  (както е записано в CLAUDE.md), сегашният е само функционален.

**Следваща стъпка:**
- Точка 5 от "Ред на разработка" в `CLAUDE.md`: `loans` app UI за
  заемане/връщане на книга (маркира `Copy` като даден на `Person` →
  създава `Loan`, после връщане → сетва `date_returned`).

**Отворени въпроси / бележки:**
- Все още няма реални данни в базата (само схемата) — потребителят ще
  въвежда истинските книги/локации/хора през admin.

---

## 2026-08-31 (продължение 5)

**Свършено:**
- Точка 5 от плана: UI за заемане/връщане на книга, вграден в
  `book_detail`:
  - `loans/forms.py`: `LendForm` (ModelForm за `Loan`, полета `person` +
    `date_given` с `<input type="date">`, default = днес).
  - `loans/views.py`: `lend_copy(copy_id)` — ако `Copy` няма отворен заем,
    създава нов `Loan`; `return_loan(loan_id)` — сетва `date_returned` на
    текущия отворен `Loan`. И двата `@require_POST`, връщат само
    обновения `<tr>` (`catalog/_copy_row.html`).
  - `catalog/_copy_row.html` нов partial (споделен между `book_detail` и
    loans views) — показва локация/състояние/статус + inline форма
    (lend или "Върни" бутон, в зависимост от статуса) + история.
  - `loans/urls.py` нов, включен в `config/urls.py`.
  - HTMX: формите правят `hx-post` с `hx-target="#copy-row-{pk}"` и
    `hx-swap="outerHTML"` — редът се обновява без пълен reload.
- Открит и оправен бъг по време на ръчното тестване: `prefetch_related`
  на `copy.loans` в `_copy_with_current_loan` кешираше историята на
  заемания ПРЕДИ да се създаде новият `Loan`, така че току-що създаденият
  запис не се появяваше в историята веднага след lend action (показваше
  "—" вместо реалния запис). Оправено чрез премахване на prefetch-а за
  single-copy заявките — приемливо на този мащаб (семейна библиотека,
  не хиляди records).
- Ръчно тествано в браузър с временни seed данни: lend → return → lend
  отново с друг човек; потвърдено през network requests, че всичко минава
  през HTMX ajax (не full page navigation), и че историята се натрупва
  правилно с най-новия запис най-отгоре (`Loan.Meta.ordering = ['-date_given']`).
  Seed данните изтрити след теста.

**Текущо състояние:**
- Пълен CRUD + бизнес flow вече работи през custom UI: преглед, търсене,
  филтриране, заемане, връщане. Django admin остава за managing на
  справочните модели (Author/Genre/Publisher/Location/Condition/Person)
  и bulk редакция.
- Дизайнът е все още само функционален inline CSS — истинският визуален
  дизайн предстои по-късно (frontend-design skill, per CLAUDE.md).

**Следваща стъпка:**
- Точка 6 от "Ред на разработка": upload на снимки на корица + връзка
  към Cloudflare R2 (`django-storages`). В момента `cover_image` се
  качва на локалния диск (`MEDIA_ROOT`) само през Django admin — трябва
  R2 credentials в `.env` (все още празни) плюс storage backend
  конфигурация в `settings.py`.
- Преди това вероятно си струва да провериш дали потребителят вече има
  Cloudflare R2 bucket/credentials готови, или трябва да се създадат.

**Отворени въпроси / бележки:**
- R2 credentials (`AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/
  `AWS_STORAGE_BUCKET_NAME`/`AWS_S3_ENDPOINT_URL`) в `.env` са все още
  празни — трябва потребителят да ги предостави преди стъпка 6.

---

## 2026-09-01

**Свършено:**
- Потребителят стартира `manage.py runserver` без активиран `.venv` →
  `ModuleNotFoundError: No module named 'dj_database_url'`. Причина:
  системният `python3`/`python` (`/usr/bin/python3`) е напълно отделна
  инсталация от `.venv`-ния Python — няма нито Django 6.1, нито
  зависимостите от `requirements.txt`. Same root cause като по-рано
  открития `django-admin` проблем. PyCharm-ският run config вече е
  правилно настроен към `.venv` (`.idea/misc.xml`), но директно
  стартиране през терминал изисква `source .venv/bin/activate` първо.
- Между другото в `requirements.txt` се беше появил ред `dj-config-url`
  (несвързан, грешно име, вероятно опит за fix по време на дебъгването) —
  премахнат от `requirements.txt`, пакетът и деинсталиран от `.venv`
  (потвърдено неизползван никъде в кода).
- Точка 3 от "Изгледи / екрани" в `CLAUDE.md`: **ръчна** форма за
  добавяне на нова книга (АИ разпознаването изрично отложено за
  следваща стъпка, по избор на потребителя):
  - `catalog/forms.py`: `BookForm` (title, authors/genres M2M, publisher,
    year, summary, cover_image — избор само измежду съществуващи
    справочни записи, без inline създаване, спазвайки конвенцията
    "справочните модели се управляват само през admin") + `CopyForm`
    (location, condition — вече предпопълнен на "Добро" по default).
  - `catalog/views.py::book_create` — записва `Book` + създава първия
    `Copy` в един POST, после `redirect` към `book_detail`.
  - `catalog/templates/catalog/book_form.html` нов, плюс "+ Добави книга"
    бутон в `book_list.html` header-а.
- Ръчно тествано в браузър (през JS form-fill, тъй като accessibility
  tree на browser tool-а се truncate-ваше насред формата — не е проблем
  в приложението): успешно създаване на книга с всички полета попълнени,
  редирект към детайлите показва всичко коректно записано (автор, жанр,
  издателство, година, резюме, първи Copy с "Добро"); празна форма →
  валидационни грешки на български ("Това поле е задължително" — благодарение
  на `LANGUAGE_CODE='bg'`), без създаване на запис. Тестовите данни
  изтрити след проверката.

**Текущо състояние:**
- И четирите основни custom екрана от `CLAUDE.md` вече съществуват:
  списък, детайли, добавяне (ръчно), заемане/връщане. Django admin остава
  за справочните модели.
- `scanner` app е все още напълно празен — следва по избор на потребителя.

**Следваща стъпка:**
- Потребителят избра ред: първо да довършим ръчния add-flow (готово), а
  после `scanner` app — АИ разпознаване на корица (Claude API vision) +
  Open Library/Google Books обогатяване, интегрирано като предварително
  попълване на същата `book_form.html` форма (снимка → предложени данни →
  преглед/редакция → запис, никога auto-save, per CLAUDE.md).
- Ще трябва `ANTHROPIC_API_KEY` в `.env` (в момента празен) —
  Claude Code сесиите тичат под платен Anthropic акаунт на потребителя,
  но за extraction-а от снимка на корица приложението ще прави собствени
  API извиквания и ще му трябва отделен ключ в `.env`.

**Отворени въпроси / бележки:**
- Все още няма реален superuser login тест през браузъра (само shell
  sanity checks) — не е блокиращо, но не е зле да се провери в началото
  на следваща сесия.
- R2 credentials за cover upload все още липсват — не пречат на
  scanner работата по същество (може да проектираме flow-а и да пазим
  cover локално докато R2 се конфигурира).

---

## 2026-09-01 (продължение)

**Свършено:**
- Потребителят посочи UX проблем: native `<select multiple>` за
  authors/genres в `book_form.html` е почти неизползваем на телефон
  (изисква ctrl/cmd+click за multi-select). Обсъдени 3 варианта
  (чекбоксове / чекбоксове+филтър / HTMX chips) — потребителят избра
  **HTMX chips/tag picker**.
- Имплементирано: `catalog/templates/catalog/_tag_picker.html` (chips +
  search input) и `_tag_search_results.html` (резултати от търсенето),
  нови views `author_search`/`genre_search` (`icontains` по `name`, до 10
  резултата, browse-all при празна заявка), URL-и добавени. `book_form.html`
  вече рендва полетата ръчно вместо `.as_p`, за да инжектира picker-а
  точно на мястото на authors/genres. `~20 реда vanilla JS` (`tagPickerAdd`
  в `base.html`) без нова JS зависимост.
- Причина за избора пред чекбоксове: мащабируемост (списъкът с автори
  расте неограничено с времето) + синергия със scanner стъпката, където
  ще трябва подобен search/match механизъм за автори, предложени от АИ.
- Открит и оправен бъг по време на ръчното тестване: search input-ът
  нямаше `name="q"` и беше вложен в `<form>` — htmx по подразбиране
  сериализира ЦЯЛАТА заобикаляща форма при GET заявка без `hx-include`,
  така че въведеният текст никога не стигаше до `request.GET['q']`
  (винаги връщаше unfiltered browse-all резултата, независимо какво е
  въведено). Оправено с `name="q"` + `hx-include="this"` (за да не изтича
  и останалото съдържание на формата в query string-а на всяко
  натискане на клавиш).
- Допълнителен UX фикс, открит при тест на бързо добавяне на 2 жанра
  последователно: след добавяне на chip резултатите просто се изчистваха
  и не се презареждаха (programmatic `.focus()` не re-fire-ва браузърното
  `focus` събитие, ако полето вече е фокусирано → htmx не презарежда).
  Оправено с explicit `htmx.trigger(searchInput, 'keyup')` след всяко
  добавяне — сега може да добавиш няколко елемента подред без да
  прекъсваш/предизвикваш ново търсене.
- Ръчно тествано в браузър с mobile viewport (375×812): филтрирано
  търсене, добавяне на 2 автора и 2 жанра последователно, dedup при
  повторен клик на вече избран елемент, премахване на chip (×), успешен
  submit със записани relations, и re-populate на chips при неуспешна
  валидация на друго поле (title/location празни → авторът остава
  избран). Тестовите данни изтрити.

**Текущо състояние:**
- Формата за добавяне на книга вече е напълно tap-friendly. Останалите
  екрани (списък, детайли, заемане/връщане) не ползват multi-select
  никъде другаде, така че не се нуждаят от промяна.

**Следваща стъпка:**
- `scanner` app — АИ разпознаване на корица (Claude API vision) + Open
  Library/Google Books обогатяване, интегрирано в същата `book_form.html`
  форма (снимка → предложени данни → преглед/редакция → запис). Ще
  трябва `ANTHROPIC_API_KEY` в `.env` (все още празен).

**Отворени въпроси / бележки:**
- Same as before — R2 credentials и `ANTHROPIC_API_KEY` все още липсват
  в `.env`.

---

## 2026-09-01 (продължение 2)

**Свършено:**
- Потребителят поиска по-лесен избор на дата ("да стане календарче") за
  `date_given` в "Дай на заем" формата — native `<input type="date">`
  вариира силно между браузъри/платформи (wheel picker на iOS и т.н.).
- Заменено с custom vanilla-JS calendar popup: readonly текстово поле
  (`class="date-input"`, ISO стойност) + `datePickerOpen`/`datePickerRender`
  в `base.html` — месечен грид на български (Пн–Нд, имена на месеците),
  навигация назад/напред, highlight на днес и избраната дата, клик на ден
  → попълва ISO стойност и затваря; клик извън затваря; повторен клик на
  полето toggle-ва отваряне/затваряне. Django приема ISO формат директно
  (`%Y-%m-%d` е първи в global `DATE_INPUT_FORMATS`, потвърдено — bg
  locale няма собствен override).
- Приложено само за `loans/forms.py::LendForm.date_given` — единственото
  date поле извън Django admin в момента.
- Ръчно тествано в браузър: отваряне/затваряне (toggle + outside-click),
  навигация месец назад/напред, избор на ден, коректен highlight на today/
  selected при повторно отваряне, пълен submit flow (заемане с дата 15
  август вместо днес — записа се вярно). Тестовите данни изтрити.

**Текущо състояние:**
- И двата "trouble spots" от UX ревюто на потребителя (multi-select
  list-box и date input) вече са заменени с custom widgets, консистентни
  по стил и поведение (същия vanilla-JS подход, без нови dependencies).

**Следваща стъпка:**
- `scanner` app — АИ разпознаване на корица (Claude API vision) + Open
  Library/Google Books обогатяване. Ще трябва `ANTHROPIC_API_KEY` в `.env`.

**Отворени въпроси / бележки:**
- R2 credentials и `ANTHROPIC_API_KEY` все още липсват в `.env`.

---

## 2026-09-01 (продължение 3)

**Свършено:**
- Потребителят посочи, че admin-only политиката за Author/Genre/Publisher
  забавя вкарването на книги твърде много. Обсъдено кратко (сложност,
  компромис с конвенцията) — потребителят потвърди съзнателното
  отклонение от `CLAUDE.md` и поиска нормализация + case-insensitive
  dedup при create.
- Проверено и потвърдено: case-insensitive търсене на кирилица вече
  работеше правилно без промяна — Postgres locale е `en_US.UTF-8`,
  Django `icontains` компилира до `UPPER(name) LIKE UPPER(...)`, а
  Postgres `UPPER()` коректно casefold-ва кирилица под тази locale
  (тествано директно в SQL и през Django ORM).
- Открити и изчистени остатъчни тестови reference записи (author/genre/
  publisher) от предишни сесии, пропуснати при по-раншно cleanup.
- Имплементирано inline create:
  - `catalog/views.py`: `_normalize_name` (trim + collapse whitespace) +
    `_tag_quick_create` helper, `get_or_create(name__iexact=..., defaults=...)`
    за dedup (запазва оригиналната casing на първия въведен запис).
    `_tag_search` вече връща `exact_match` флаг, за да не предлага "+"
    когато записът вече съществува.
  - Author/Genre (tag-picker): `_tag_search_results.html` показва бутон
    "+ Добави „X"" при липса на точно съвпадение; `tagPickerCreate` в
    `base.html` POST-ва към нов quick-create endpoint и добавя резултата
    директно като chip.
  - Publisher (plain dropdown, не tag-picker): нов "+" бутон до select-а;
    `inlineSelectCreate` прави `prompt()` за име, POST-ва, добавя `<option>`
    и го избира — по-лека реализация от tag-picker, защото Publisher е
    single-value.
  - `CLAUDE.md` обновен: `Location`/`Condition`/`Person` остават
    admin-only; `Author`/`Genre`/`Publisher` вече могат и inline.
- Ръчно тествано в браузър: create на нов автор през "+" (chip се появява
  веднага), повторен POST със същото име в различен регистър/whitespace
  потвърждава dedup (връща същия `id`, запазена оригинална casing),
  publisher "+" добавя/избира нова опция, пълен submit записва книгата
  коректно с inline-създадените записи. Тестовите данни изтрити.

**Текущо състояние:**
- Добавянето на книга вече е значително по-бързо — не се налага
  прекъсване към admin за нов автор/жанр/издателство. Location/Condition/
  Person остават admin-only (по-рядко се добавят нови).

**Следваща стъпка:**
- `scanner` app — АИ разпознаване на корица (Claude API vision) + Open
  Library/Google Books обогатяване. Ще трябва `ANTHROPIC_API_KEY` в
  `.env`. Естествен fit: АИ ще предлага имена на автори, а вече имаме
  quick-create + case-insensitive dedup механизъм, който да ползва.

**Отворени въпроси / бележки:**
- R2 credentials и `ANTHROPIC_API_KEY` все още липсват в `.env`.

---

## 2026-09-02

**Свършено:**
- Потребителят направи собствена промяна в моделите (`Book.authors`/
  `genres` вече `blank=True`) и мигрира сам (2 миграции: 0002 добави
  излишен `null=True` на M2M, 0003 го маха — потвърдено чрез
  `makemigrations --check` че всичко е синхронизирано, нищо неприложено).
  Закомитнато отделно с ясна бележка, че е направено от потребителя.
- Даден е `ANTHROPIC_API_KEY`, записан в `.env` (само локално, gitignored).
- Изградена `scanner` app — АИ разпознаване на корица, точка 7 от плана:
  - **Дизайн решение**: вместо отделен "scan" екран, разпознаването е
    вградено директно в `catalog:book_create` формата. Снимката се избира
    веднъж в стандартното `cover_image` поле; бутон "Разпознай от
    снимката" я праща за анализ през `fetch`, резултатите prefill-ват
    формата client-side (title/year/summary + author chips + publisher
    select), обикновен submit пази книгата. Избягва проблема с "файлът не
    може да се prefill-не в `<input type=file>` от URL" — снимката просто
    си остава избрана в полето, не се качва два пъти.
  - `scanner/claude_client.py`: `extract_cover_info()` — Pillow resize до
    1024px + re-encode JPEG (по-малък payload, нормализира формата от
    камерата), Claude API извикване с `tool_choice` forcing структуриран
    JSON `{title, authors, publisher, isbn}` (по-надеждно от prompt-based
    free-text JSON parsing). Модел: `claude-sonnet-5`.
  - `scanner/open_library.py`: `enrich(isbn, title, author)` — ISBN lookup
    с fallback на title+author search, плюс отделна заявка към
    `/works/*.json` за резюме (description не идва directly от search
    resultsите). Връща `{summary, year}`.
  - `scanner/views.py`: `scan_cover` POST endpoint свързва двете, resolve-ва
    authors/publisher през същия `get_or_create(name__iexact=...)` dedup
    pattern като catalog quick-create (reuse на `catalog.views._normalize_name`).
  - `templates/base.html`: `scanCoverStart()` — reuse на `tagPickerAdd`/
    `selectSetOption` за prefill.
  - `book_form.html`: cover_image полето преместено най-отгоре (логичен
    ред: снимка → разпознаване → останалите полета се появяват попълнени).
- **Тестване (частично, заради липса на Anthropic credit баланс):**
  - `claude_client.extract_cover_info()` тестван с реален API ключ и
    синтетично тестово изображение → authentication работи коректно,
    грешката е billing-related ("Your credit balance is too low"), НЕ
    код проблем; `ScanError` handling улавя я правилно.
  - `open_library.enrich()` тестван самостоятелно с реална книга ("Under
    the Yoke" / Иван Вазов) → намери година (1912) и резюме коректно.
  - `scan_cover` view тестван end-to-end през Django test client с
    mock-нат `claude_client.extract_cover_info` → author/publisher
    resolution + JSON форма коректни, idempotent create потвърден.
  - Frontend JS тестван в браузър с mock-нат `window.fetch`: успешен
    случай (всички полета + author chip + publisher option се появяват
    коректно), server error (показва се в status реда), липсваща снимка
    (ясно съобщение "Първо избери снимка").
  - Всички тестови данни (author/publisher/location) изчистени след теста.
- Git история: 2 отделни commit-а — един за потребителската model промяна
  (без Claude co-author таг, тъй като кодът не е мой), един за scanner
  feature-а.

**Текущо състояние:**
- `scanner` app е напълно имплементиран и кодово тестван, но **никога не
  е викан с реален успешен Claude API отговор** — акаунтът няма credit
  balance. Целият pipeline (Claude extraction → Open Library enrichment →
  author/publisher resolution → frontend prefill) е верифициран на части,
  но не end-to-end с истинска снимка на корица.
- Всички други части от плана в `CLAUDE.md` вече са готови: models,
  admin, списък/търсене/филтри, детайли, заемане/връщане, ръчно добавяне
  (с inline quick-create + custom calendar), и сега scanner UI-то.

**Следваща стъпка:**
- Потребителят трябва да добави credit/billing в Anthropic конзолата.
  След това: пълен end-to-end тест с реална снимка на книга (най-добре
  няколко различни корици — включително кирилица, различни издателства,
  книги без ISBN на корицата) за да се провери реалното качество на
  разпознаването и на Open Library enrichment-а.
- Точка 8 от плана: деплой на Render/Railway (остава последна).
- R2 credentials за cover storage все още липсват в `.env` (точка 6 —
  засега cover_image се пази на локален диск, работи функционално, но
  не е production-ready storage).

**Отворени въпроси / бележки:**
- Ако Claude vision понякога връща частично объркани резултати (напр.
  грешен автор при преводна литература) — DATA_MODEL.md изрично
  предупреждава за това; текущият UI вече го адресира чрез "прегледай и
  редактирай преди запис" flow, но си струва да се внимава при реалното
  тестване.
- R2/production storage все още за по-късно.

---

## 2026-09-02 (продължение)

**Свършено:**
- Потребителят посочи, че на българските книги ISBN обикновено не е на
  предната корица (пази се отзад/на копирайт страницата) — само
  заглавие/автор/издателство се виждат реално.
- Премахнат ISBN изцяло от scanner flow-а: `claude_client.TOOL_SCHEMA`
  вече няма `isbn` поле; `open_library.enrich()` опростен да минава само
  през title+author search (ISBN lookup path и свързаният `_by_isbn`/
  `_extract_year` код изтрити напълно, не оставени като dead code);
  `scanner/views.py` вече не подава isbn към enrich. `docs/DATA_MODEL.md`
  обновен да отразява опростения flow.
- Ре-тествано end-to-end (mock-нат Claude response) — работи коректно.

**Текущо състояние:**
- `scanner` app непроменен функционално, само по-опростен/по-точен за
  реалните български корици.

**Следваща стъпка:**
- Пак: чакаме Anthropic credit balance за пълен end-to-end тест с реална
  снимка. После точка 8 (деплой).

---

## 2026-09-02 (продължение 2)

**Свършено:**
- Потребителят зареди Anthropic credit, но получи "ANTHROPIC_API_KEY не е
  конфигуриран" — причината: dev сървърът му работеше непрекъснато от
  преди `.env` промяната (env vars се четат само веднъж при старт;
  Django autoreloader следи `.py`, не `.env`). Рестартирах процеса му
  (killed стар PID, стартиран нов на същия порт 8000) — потвърдено
  `ANTHROPIC_API_KEY` вече се зарежда. Тестван реален Claude vision call
  със синтетично тестово изображение → **успешен** (`Pod Igoto` / `Ivan
  Vazov` / `Hermes Publishing` разпознати коректно) — потвърдено, че
  credit balance-ът вече работи.
- **Важен урок за бъдещи сесии**: ако потребителят промени `.env` докато
  сървърът му вече работи, трябва restart на процеса — само редакция на
  `.py` файл auto-reload-va.
- Потребителят поиска бутон за редакция на книга (липсваше). Добавен
  `catalog:book_edit`:
  - `book_edit` view reuse-ва `BookForm` с `instance=book` — `ModelForm.save()`
    прави clear+set на M2M-нетата коректно (add/remove на автори/жанрове
    работи, не само добавя).
  - `book_form.html` вече поддържа create/edit през `is_edit` флаг:
    различен heading/back-link/бутон текст; "Първи екземпляр" (CopyForm)
    секцията се показва само при create — копия се управляват отделно
    (admin / lend-return UI при детайлите), не се пипат при edit на книга.
  - "✎ Редактирай" бутон в `book_detail.html` header-а.
- Ръчно тествано: form prefill коректен (всички полета + author/genre
  chips + publisher), запис на промяна отразява веднага, премахване на
  author chip при edit коректно маха M2M връзката. Тествано на отделен
  порт (8123), без да се пипат реалните данни на потребителя вече в
  базата (видяхме реален `Person` "Цеци" — потребителят вече ползва
  приложението за истина).

**Текущо състояние:**
- Screen 3 от `CLAUDE.md` вече покрива и create, и edit на книга.
  `scanner` app потвърдено работи с реален Claude API + credit.

**Следваща стъпка:**
- Точка 8 от плана: деплой на Render/Railway.
- R2 credentials за production cover storage все още липсват в `.env`.

**Отворени въпроси / бележки:**
- Потребителят вече има реални данни в базата (books/persons/etc.) —
  занапред тестовете трябва да са още по-внимателни да не пипат/трият
  нещо реално; предпочитание към отделен тестов порт вместо потребителския
  8000, и селективен cleanup (само това, което самите тестове създават).

---

## 2026-09-02 (продължение 3)

**Свършено:**
- Потребителят сам написа бутон за изтриване на книга, но не работеше.
  Намерени 2 бъга в неговия код: (1) `redirect(request, 'catalog:book_list')`
  — `redirect()` не приема `request` като първи аргумент; (2) GET клонът
  render-ваше `book_list.html` без никакъв context, а бутонът беше обикновен
  `<a href>` (винаги GET), затова кликването тихо показваше празна страница
  вместо да трие каквото и да е.
- Поправено: `book_delete` вече е `@require_POST`-only; бутонът в
  `book_detail.html` е POST форма с `onsubmit` confirm() диалог
  (предупреждава, че изтриването каскадно маха и всички `Copy`/`Loan`
  записи към книгата — потвърдено през `on_delete=CASCADE` веригата в
  моделите). Добавен `.header-actions`/`.button-danger` CSS в `base.html`.
- Ръчно тествано: create на тестова книга → delete → confirm → редирект
  към списъка; потвърдено през shell, че Book+Copy наистина са изтрити
  (cascade работи). Тестови reference записи изчистени, реалните данни
  на потребителя недокоснати.

**Текущо състояние:**
- Delete вече работи коректно. И четирите CRUD операции за `Book`
  (create/read/update/delete) вече са налични в custom UI-то.

**Следваща стъпка:**
- Точка 8 от плана: деплой на Render/Railway. R2 credentials за
  production cover storage все още липсват в `.env`.

---

## 2026-09-02 (продължение 4)

**Свършено:**
- Потребителят не разбираше логиката на `Copy` (екземпляри) и посочи
  реален gap: нямаше UI начин да добавиш втори `Copy` към вече
  съществуваща `Book` (напр. дубликат намерен в друга къща) — `book_create`
  винаги прави точно 1 `Copy` при създаване, после само admin.
- Обсъдени 2 свързани случая: (1) знаеш книгата вече е в каталога, просто
  намираш още едно физическо копие → нужен бутон "Добави екземпляр";
  (2) сканираш корица на книга, която вече съществува в каталога (не си
  спомнял) → системата трябва да предупреди и предложи "добави екземпляр"
  вместо да създаде дублиращ `Book`. Потребителят се съгласи да
  адресираме (1) сега, (2) — при следващото реално добавяне през сканиране.
- Имплементирано (1): `catalog/views.py::copy_add` + нов темплейт
  `copy_form.html` (малка форма, reuse на `CopyForm`) — POST-ва нов `Copy`
  към съществуващ `Book`, редирект обратно към детайлите. "+ Добави
  екземпляр" бутон в `book_detail.html`.
- Ръчно тествано: книга с 1 екземпляр → добавен втори на различна
  локация → и двата се показват коректно с независим lend/return статус.
  Тестовите данни изчистени.

**Текущо състояние:**
- `Copy` управлението вече е пълно през custom UI: create (при добавяне
  на книга), add additional (нов екран), lend/return (вече съществуваше).
  Delete на `Copy` остава само през admin (рядко нужно, не е поискано).

**Следваща стъпка:**
- Случай (2) отгоре: duplicate detection при добавяне/сканиране на книга
  (проверка по заглавие/автор преди create, UI избор "добави екземпляр
  вместо нова книга") — да се адресира на следващото реално добавяне
  през scanner, за да го тестваме с реален use case.
- Точка 8 от плана: деплой на Render/Railway. R2 credentials все още
  липсват в `.env`.

---

## 2026-09-02 (продължение 5)

**Свършено:**
- Директно адресирахме duplicate-detection случая (по-рано отложен):
  потребителят поиска проверка при запис дали заглавието вече съществува.
  Обсъдени 2 варианта — блокиращо потвърждение vs. само предупреждение;
  потребителят избра **само предупреждение** (не блокира submit), защото
  легитимно могат да съществуват 2 различни книги със същото заглавие.
- Имплементирано: `catalog:title_check` view (GET, `title__iexact`
  сравнение, изключва текущата книга при edit през hidden `exclude` поле
  с `book.pk`) + partial `_title_check.html`. `BookForm.title` widget вече
  носи `hx-get`/`hx-trigger` (keyup delay 400ms) атрибути, целящи
  `#title-check-result` div под полето в `book_form.html`.
  `hx-include="this, [name=exclude]"` — приложен наученият урок от
  по-ранния tag-picker бъг (без него нужно щеше да изтече цялата форма в
  query string-а на всяко натискане на клавиш).
- Ако има съвпадение, показва се жълт warning box с линкове "виж" /
  "добави екземпляр вместо това" (сочи право към вече съществуващия
  `copy_add` екран).
- Ръчно тествано: съществуващо заглавие (различен регистър) → warning се
  появява живо; уникално заглавие → нищо; edit на книга със собственото ѝ
  заглавие → правилно НЕ се маркира (self-exclude работи). Тестови данни
  изчистени.

**Текущо състояние:**
- И двата duplicate-detection случая от по-рано вече са адресирани:
  ръчно добавяне на екземпляр (copy_add) + warning при дублиращо
  заглавие. Остава да видим как се държи в комбинация с реалния scanner
  flow при следващото сканиране на книга (дали warning-ът се появява и
  когато заглавието идва от АИ разпознаването, не само от ръчно писане).

**Следваща стъпка:**
- Точка 8 от плана: деплой на Render/Railway. R2 credentials все още
  липсват в `.env`.

**Отворени въпроси / бележки:**
- Warning-ът сравнява само по заглавие (не и автор) — приемлив компромис
  по избор на потребителя, но има шанс за false positive при чиста
  случайност на заглавието.

---

## 2026-09-03

**Свършено:**
- Потребителят реши, че приложението е готово за точка 8 от плана:
  деплой. Уточнени 3 решения преди да пипаме нещо извън локалния код:
  1. GitHub repo — потребителят ще създаде празно repo ръчно и ще даде
     линка (вместо `gh` CLI login flow, което не е инсталирано).
  2. Cover storage в production — **Railway Volume** засега (просто
     mount в dashboard-а), R2 остава за по-late, ако потрябва.
  3. Railway account — потребителят ще влезе през GitHub login.
- Направена production-readiness подготовка в кода:
  - `whitenoise` за static files (Django admin CSS/JS не се сервира от
    самия Django при `DEBUG=False`) — `STATIC_ROOT` +
    `CompressedManifestStaticFilesStorage` през новия Django `STORAGES`
    setting.
  - `SECURE_PROXY_SSL_HEADER` (Railway терминира TLS на edge, проксира
    plain HTTP навътре), `SECURE_SSL_REDIRECT`/`SESSION_COOKIE_SECURE`/
    `CSRF_COOKIE_SECURE` вързани към `DEBUG`, нов `CSRF_TRUSTED_ORIGINS`
    env-driven setting.
  - `MEDIA_ROOT` вече чете `MEDIA_ROOT` env var (fallback чрез `or`, не
    dict `.get(key, default)` — важно, защото празен-но-присъстващ env
    var connect се третира различно от липсващ; `.get` с default само
    покрива липсващия случай) — в production ще сочи към mount path-а на
    прикачен Railway Volume, локално default си остава `BASE_DIR/media`.
  - `gunicorn` + `whitenoise` добавени в `requirements.txt`.
  - Нов `Procfile`: единен `web` процес прави
    `migrate --noinput && collectstatic --noinput && gunicorn ...` на
    всеки boot — по-портативно от Heroku-style `release:` process type,
    който Railway не поддържа сигурно.
  - `.env`/`.env.example` обновени с новите vars.
- Ръчно тествано локално: `manage.py check`, `collectstatic` (169 файла,
  чисто), пълната Procfile команда под истински `gunicorn` с
  `DEBUG=False` — HTTP 200 на `/` и `/admin/login/`, admin CSS се
  сервира от whitenoise коректно, SSL redirect се задейства само без
  `X-Forwarded-Proto` header (симулира точно Railway edge поведението).
  Обикновен `manage.py runserver` (DEBUG=True) продължава да работи
  непроменено.

**Текущо състояние:**
- Кодът е готов за деплой. Няма още git remote, няма Railway проект.
  Чакаме от потребителя: (1) URL на празното GitHub repo, за да добавим
  remote и push-нем; (2) достъп/потвърждение в Railway dashboard-а за
  създаване на проект, Postgres plugin, Volume mount, и env vars.

**Следваща стъпка:**
1. Потребителят дава GitHub repo URL → добавяме remote, push-ваме
   `master` branch.
2. Създаване на Railway проект от GitHub repo (auto-deploy при всеки
   push), Postgres plugin (нова production база — отделна от локалната
   `family_library`), Volume mount за `MEDIA_ROOT`.
3. Env vars в Railway dashboard-а: `DJANGO_SECRET_KEY` (нов, различен от
   локалния), `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` (Railway
   домейна), `DJANGO_CSRF_TRUSTED_ORIGINS` (https://<домейн>),
   `DATABASE_URL` (auto от Postgres plugin-а), `MEDIA_ROOT` (Volume mount
   path), `ANTHROPIC_API_KEY`.
4. След първия deploy: `createsuperuser` на production (през Railway's
   run/shell функционалност).

**Отворени въпроси / бележки:**
- R2 остава документирано в `CLAUDE.md` като по-solid дългосрочен план
  за cover storage — Volume е съзнателен bootstrap избор, не финално
  решение.
