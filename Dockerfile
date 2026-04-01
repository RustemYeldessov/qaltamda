# Используем официальный легкий образ Python
FROM python:3.11-slim

# Запрещаем Python писать файлы .pyc на диск и разрешаем выводить логи в консоль без задержек
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для работы с Postgres (если понадобится позже)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное
COPY . .

# Запуск через uvicorn (предполагаем, что главный файл main.py и объект FastAPI называется app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]