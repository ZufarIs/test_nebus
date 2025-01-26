FROM python:3.11-slim

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для данных и назначаем права
RUN mkdir -p /app/data
RUN chmod 777 /app/data

# Копируем все файлы приложения
COPY . .

# Создаем пользователя и назначаем права
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

# Инициализируем БД при старте контейнера
CMD ["sh", "-c", "python run.py"] 
