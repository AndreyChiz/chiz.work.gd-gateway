#!/bin/bash
set -e

# ------------------------------
# 🔹 Конфигурация окружения
# ------------------------------

# Читаем данные из pyproject.toml
NAME=$(grep -E '^name\s*=' pyproject.toml | sed 's/name\s*=\s*"\(.*\)"/\1/')
VERSION=$(grep -E '^version\s*=' pyproject.toml | sed 's/version\s*=\s*"\(.*\)"/\1/')
PROJECT_NAME=$(grep 'keywords' pyproject.toml | sed 's/.*\["\(.*\)"\].*/\1/')

# Остальные переменные
REGISTRY="reg.localhost"
DOCKER_USER="achi"
DOCKER_PASS="123"
HOST="localhost"
IMAGE_NAME="${PROJECT_NAME}-${NAME}:${VERSION}"
CONTAINER_NAME="${PROJECT_NAME}-backend-service-${NAME}"

# Экспортируем все переменные
export REGISTRY DOCKER_PASS DOCKER_USER IMAGE_NAME PROJECT_NAME CONTAINER_NAME HOST

# ------------------------------
# 🔹 Запуск пайплайна
# ------------------------------
echo "🚀 Starting development build pipeline..."
echo "📦 Host: $HOST"
echo "📦 Image: $IMAGE_NAME"
echo "📡 Registry: $REGISTRY"
echo "👤 Docker user: $DOCKER_USER"
echo "🧱 Container: $CONTAINER_NAME"

echo "1️⃣  Building image..."
bash scripts/build.sh

echo "2️⃣  Pushing to private registry..."
bash scripts/private_registry_push.sh

echo "3️⃣  Running containers..."
bash scripts/run.sh

echo "✅ All steps completed successfully!"
