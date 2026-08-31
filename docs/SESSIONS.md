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
