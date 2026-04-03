# E-Commerce App - Lab 0

## Рівень 1 (Phase 1)
✅ **One-Command Build:** Тести запускаються командою `pytest`. Залежності зібрані в `requirements.txt` (`pip install -r requirements.txt`).
✅ **12-Factor App (Environment Variables):** Конфігурація бази даних зчитується зі змінних оточення.
Обов'язкові змінні для підключення PostgreSQL (див. `app/database.py`):
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
*(Якщо змінні відсутні, застосунок безпечно перемикається на локальний SQLite).*
✅ **Автоматичні міграції:** Використовується `Alembic`. Міграції застосовуються автоматично до бази даних під час старту FastAPI (через `lifespan`).