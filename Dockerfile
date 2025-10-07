# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src ./src

# Копируем .env, если есть
COPY .env ./src/config/.env

# Открываем порт для FastAPI
EXPOSE 8000

# Запуск приложения через uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 