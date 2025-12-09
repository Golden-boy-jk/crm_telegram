FROM python:3.11-slim AS base

# 1) Базовые настройки интерпретатора
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 2) Рабочая директория
WORKDIR /app

# 3) (опционально) системные зависимости, если понадобятся
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#  && rm -rf /var/lib/apt/lists/*

# 4) Установка Python-зависимостей
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5) Копируем остальной код
COPY . .

# 6) Непривилегированный пользователь
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser /app
USER appuser

# 7) Порт по умолчанию (Railway/Render часто прокидывают свой, но это не мешает)
ENV PORT=8000
EXPOSE 8000

# 8) Старт приложения
# Если захотим гонять Alembic при старте, можно будет обернуть в "sh -c"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
