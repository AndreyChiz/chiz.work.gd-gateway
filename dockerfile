FROM python:3.12-slim

WORKDIR /app

# Копируем файлы проекта для UV
COPY pyproject.toml uv.lock ./

# Устанавливаем UV глобально (если нужно)
RUN python -m pip install --no-cache-dir uv

# Устанавливаем зависимости через uv
RUN uv sync

# Копируем код приложения
COPY ./app /app/app
COPY ./README.md /app/README.md

# Создаём папку для логов Gunicorn
RUN mkdir -p /app/logs

ENV PATH="/app/.venv/bin:$PATH"

# Gunicorn для продакшена
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8001", "--workers", "1", "--log-level", "debug", "--capture-output","--access-logfile", "/app/logs/access.log", "--error-logfile", "/app/logs/error.log"]