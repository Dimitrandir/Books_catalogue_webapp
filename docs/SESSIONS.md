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
