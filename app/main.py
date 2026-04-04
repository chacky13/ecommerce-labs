from fastapi import FastAPI
from contextlib import asynccontextmanager
import subprocess

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Автоматичний запуск міграцій бази даних (Alembic)...")
    try:

        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Міграції успішно застосовані!")
    except Exception as e:

        print(f"⚠️ Помилка міграцій (ігноруємо для тестів): {e}")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "App is running"}

# --- ДОДАНО ДЛЯ LAB 3 ---
@app.get("/health")
def health_check():

    return {"status": "healthy"}