# Базовый образ
FROM python:3.9-slim

# Установка зависимостей
RUN pip install flask gunicorn

# Рабочая директория
WORKDIR /app

# Копирование файлов
COPY app.py .

# Порт приложения
EXPOSE 5000

# Команда запуска
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]