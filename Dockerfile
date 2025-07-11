FROM python:3.11-slim

# Установка зависимостей
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]
