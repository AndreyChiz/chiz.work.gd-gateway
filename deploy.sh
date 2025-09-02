#!/bin/bash
set -e

# -------------------------------
# Настройки
# -------------------------------
# PROJECT_DIR="/home/www/src/chiz/gate_way"
PROJECT_DIR="."
IMAGE_NAME="chiz_api_gateway"
CONTAINER_NAME="chiz_api_gateway"
HOST_PORT=8001
CONTAINER_PORT=8001
LOG_DIR="$PROJECT_DIR/logs"

# -------------------------------
# Подготовка логов
# -------------------------------
mkdir -p "$LOG_DIR"

# -------------------------------
# Сборка образа с тегом latest
# -------------------------------
echo "Сборка Docker образа $IMAGE_NAME:latest"
docker build -t $IMAGE_NAME:latest "$PROJECT_DIR"

# -------------------------------
# Остановка старого контейнера (если есть)
# -------------------------------
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Остановка старого контейнера $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# -------------------------------
# Запуск нового контейнера
# -------------------------------
echo "Запуск нового контейнера $CONTAINER_NAME"
docker run -d \
    --name $CONTAINER_NAME \
    -p $HOST_PORT:$CONTAINER_PORT \
    --restart unless-stopped \
    -v "$LOG_DIR":/app/logs \
    $IMAGE_NAME:latest

echo "Деплой завершён! Образ: $IMAGE_NAME:latest"
