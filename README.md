# Family Library

Уеб апликация за картотекиране на семейна библиотека, разпръсната в
няколко къщи/населени места. Django + PostgreSQL.

Пълният контекст на проекта (за Claude Code) е в `CLAUDE.md`.
Пълният модел на данните е в `docs/DATA_MODEL.md`.

## Стартиране (локално, стъпка по стъпка ще се допълни от Claude Code)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # попълни истинските стойности
```

Останалата настройка (Django проект скеле, models, migrations) предстои —
виж "Ред на разработка" в `CLAUDE.md`.
