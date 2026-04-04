# Стейдж 1: Збірка залежностей (Builder)
FROM python:3.11-alpine as builder

WORKDIR /app
# Встановлюємо системні бібліотеки для компіляції psycopg2 та інших
RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Стейдж 2: Фінальний легкий образ (Runner)
FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache libpq

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]