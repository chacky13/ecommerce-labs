import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ми беремо URL бази зі змінної оточення DATABASE_URL.
# Якщо такої змінної немає (як у тебе зараз на локалці), використовуємо SQLite (файл ecommerce.db)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Параметр connect_args потрібен тільки для SQLite, щоб уникнути помилок з потоками
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()