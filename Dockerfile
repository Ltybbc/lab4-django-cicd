# Используем легкий образ Python
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Команда запуска (укажи свою, например, gunicorn или manage.py)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]