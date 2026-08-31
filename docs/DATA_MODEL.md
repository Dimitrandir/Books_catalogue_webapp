# Модел на данните

## Справочни модели (dropdown, управляват се само през Django admin)

Всеки от тях е прост модел с поле `name` (unique) и `__str__` връщащ `name`.

### Author
- `name` (CharField)

### Genre
- `name` (CharField)

### Publisher
- `name` (CharField)

### Location
- `name` (CharField) — например "Пловдив", "София", "с. Козарево"

### Condition
- `name` (CharField) — например "Добро", "Ново", "Износено", "Повредено"
- Записът "Добро" трябва да съществува винаги (seed чрез data migration или
  `get_or_create`); `Copy.condition` има default сочещ towards този запис
  по `name`, не по твърд `pk`.

### Person
- `name` (CharField) — хора, на които обичайно се дават книги назаем

## Основни модели

### Book
Представлява заглавие (произведение), не физически екземпляр.

- `title` (CharField)
- `authors` (ManyToManyField → Author)
- `genres` (ManyToManyField → Genre)
- `publisher` (ForeignKey → Publisher, null=True)
- `year` (IntegerField, null=True) — година на издание
- `summary` (TextField, blank=True) — резюме, може да се попълни от АИ/API
- `cover_image` (ImageField, качва се към Cloudflare R2 storage)

### Copy
Представлява конкретен физически екземпляр от Book.

- `book` (ForeignKey → Book)
- `location` (ForeignKey → Location)
- `condition` (ForeignKey → Condition, default → запис "Добро")

Забележка: ако имаме 2 еднакви книги в различни къщи (или дубликат в
същата къща), това са 2 отделни `Copy` записа сочещи към една и съща `Book`.

### Loan
История на заемания на конкретен физически екземпляр.

- `copy` (ForeignKey → Copy)
- `person` (ForeignKey → Person)
- `date_given` (DateField)
- `date_returned` (DateField, null=True, blank=True)

Забележка: пазим цялата история (не само последното заемане) — множество
`Loan` записа могат да сочат към един и същ `Copy` във времето.
Текущо "на заем" състояние = последен `Loan` за даден `Copy` с
`date_returned IS NULL`.

## Връзки — обобщение

```
Author  ──M2M──┐
                ├──> Book ──FK──> Publisher
Genre   ──M2M──┘      │
                       │ (1:N)
                       ▼
                     Copy ──FK──> Location
                       │     └──FK──> Condition
                       │ (1:N)
                       ▼
                     Loan ──FK──> Person
```

## Търсене

PostgreSQL full-text search върху `Book.title`, `Author.name`,
`Book.summary` чрез `django.contrib.postgres.search`
(`SearchVector` + `SearchQuery`/`SearchRank`). Филтриране допълнително по
`Genre`, `Publisher`, `Location`, `Condition` — стандартни Django ORM
filter-и през query params в изгледа за търсене.

## АИ разпознаване на корица (scanner app) — поток

1. Потребител качва снимка на корица.
2. Снимката се изпраща към Claude API (vision) с prompt да върне JSON:
   `{title, authors: [...], publisher, isbn}`.
3. Ако има `isbn` или `title`+`authors` — заявка към Open Library API
   (или Google Books API като fallback) за: резюме, година, по-качествена
   корица.
4. Резултатът се показва на потребителя в форма за преглед/редакция.
5. Едва след потвърждение от потребителя се създава/обновява `Book` запис.

Никога автоматичен запис без преглед — АИ разпознаването може да сгреши
автор/издание, особено при преводна литература или по-стари издания.
