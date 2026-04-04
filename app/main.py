from fastapi import FastAPI, Response, status
from contextlib import asynccontextmanager
import subprocess
import logging
import json
import sys
from sqlalchemy import text
from app.database import engine

class JSONFormatter(logging.Formatter):
    def format(self, record):

        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }, ensure_ascii=False)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())

logging.root.handlers = [handler]
logging.root.setLevel(logging.INFO)

for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
    l = logging.getLogger(logger_name)
    l.handlers = [handler]
    l.propagate = False

app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Автоматичний запуск міграцій (Alembic)...")
    try:

        subprocess.run("alembic upgrade head", shell=True, check=True)
        app_logger.info("Міграції успішно застосовані!")
    except Exception as e:
        app_logger.error(f"Помилка міграцій: {e}")
    yield
    app_logger.info("Зупинка застосунку...")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "App is running"}


@app.get("/health")
def health_check(response: Response):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        app_logger.info("Health check passed: DB connected")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        app_logger.error(f"Health check failed: DB is offline")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "disconnected"}