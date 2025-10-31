#!/bin/bash
set -e

# # 🔹 Читаем версию из pyproject.toml
# VERSION=$(grep -E '^version\s*=' pyproject.toml | sed 's/version\s*=\s*"\(.*\)"/\1/')
# NAME=$(grep -E '^name\s*=' pyproject.toml | sed 's/name\s*=\s*"\(.*\)"/\1/')

# # 🔹 Формируем тег образа
# IMAGE_NAME="${NAME}:${VERSION}"
echo "⚠️ Using image: $IMAGE_NAME"
echo "⚠️ Рroject: $PROJECT_NAME"

export IMAGE_NAME


export COMPOSE_PROJECT_NAME="$PROJECT_NAME"
docker compose up --build -d

echo "✅ Docker-compose started successfully. Containers running in background."
