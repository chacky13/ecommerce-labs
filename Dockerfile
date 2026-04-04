# Використовуємо офіційний легкий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Встановлюємо системні залежності (потрібні для деяких бібліотек)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файл із залежностями
COPY requirements.txt .

# Встановлюємо бібліотеки Python
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .

# Команда для запуску нашого додатку
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]