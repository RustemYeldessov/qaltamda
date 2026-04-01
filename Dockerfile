FROM python:3.12-slim

# Настройки Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.3.3 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Устанавливаем системные зависимости для сборки (если пригодятся для БД)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Ставим сам poetry
RUN pip install "poetry==$POETRY_VERSION"

# Копируем только файлы зависимостей (для кэширования слоев)
COPY pyproject.toml poetry.lock* ./

# Устанавливаем библиотеки без создания venv (внутри контейнера это не нужно)
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код
COPY . .

# Запуск через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]