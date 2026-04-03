import subprocess
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Автоматичний запуск міграцій бази даних...")
    try:
        # Це те саме, що написати "alembic upgrade head" у терміналі
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Міграції успішно застосовані.")
    except Exception as e:
        print(f"Помилка міграцій: {e}")
    yield # Тут сервер працює і приймає запити

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "App is running"}