# Используем базовый образ с Python и Poetry
FROM python:3.10-alpine

# Устанавливаем poetry
RUN pip install poetry

# Копируем файлы для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости
WORKDIR /app
RUN poetry install

# Копируем файлы приложения
COPY app /app

# Выполняем инициализацию базы данных
RUN poetry run python -c "from app import init_db; init_db()"

# Определение команды запуска приложения
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
