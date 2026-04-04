from fastapi import FastAPI
from contextlib import asynccontextmanager
import subprocess


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматичний запуск міграцій при старті
    print("Автоматичний запуск міграцій бази даних (Alembic)...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Міграції успішно застосовані!")
    except Exception as e:
        print(f"Помилка міграцій: {e}")

    yield  # Сервер працює


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "App is running"}