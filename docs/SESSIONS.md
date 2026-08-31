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
