# E-commerce App (Lab 0 - Level 1)

## One-Command Build
Проєкт використовує `requirements.txt`. Тести запускаються однією командою:
`pytest`

## Конфігурація через середовище (Env Vars)
Застосунок використовує наступні змінні оточення:
* `DB_HOST`
* `DB_PORT`
* `DB_NAME`
* `DB_USER`
* `DB_PASSWORD`

## Автоматичне керування схемою БД
Проєкт використовує `alembic`. Під час старту застосунок (FastAPI lifespan) автоматично виконує команду `alembic upgrade head`, застосовуючи всі наявні міграції до бази даних.
