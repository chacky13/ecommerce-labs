from fastapi import FastAPI, Response, status
from contextlib import asynccontextmanager
import subprocess
import logging
import json
import sys
from sqlalchemy import text
from app.database import engine

# 1. Налаштовуємо JSON логування
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        })

# Перехоплюємо логи Uvicorn та FastAPI, щоб вони теж були в JSON
for logger_name in ("uvicorn.access", "uvicorn.error", "uvicorn", "fastapi"):
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.handlers = [handler]
    logger.propagate = False

app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)
app_logger.handlers = [logging.StreamHandler(sys.stdout)]
app_logger.handlers[0].setFormatter(JSONFormatter())

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Автоматичний запуск міграцій (Alembic)...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        app_logger.info("Міграції успішно застосовані!")
    except Exception as e:
        app_logger.error(f"Помилка міграцій: {e}")
    yield
    app_logger.info("Зупинка застосунку...")

app = FastAPI(lifespan=lifespan)

# 2. Головна сторінка
@app.get("/")
def read_root():
    return {"status": "ok", "message": "App is running"}

# 3. Health Check для Docker та тестів
@app.get("/health")
def health_check(response: Response):
    try:
        # Пробуємо виконати найпростіший запит до бази
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        app_logger.info("Health check passed: DB connected")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        app_logger.error(f"Health check failed: DB is offline")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "disconnected"}