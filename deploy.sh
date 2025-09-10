#!/bin/bash
set -e

# -------------------------------
# Настройки
# -------------------------------
PROJECT_DIR="."
IMAGE_NAME="chiz_api_gateway"
CONTAINER_NAME="chiz_api_gateway"
LOG_DIR="$PROJECT_DIR/logs"

# -------------------------------
# Подготовка логов
# -------------------------------
mkdir -p "$LOG_DIR"

# -------------------------------
# Сборка образа с тегом 
# -------------------------------
echo "Сборка Docker образа $IMAGE_NAME"
docker build -t $IMAGE_NAME "$PROJECT_DIR"

# -------------------------------
# Остановка старого контейнера (если есть)
# -------------------------------
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Остановка старого контейнера $CONTAINER_NAME"
    docker rm -f $CONTAINER_NAME
fi

# -------------------------------
# Запуск нового контейнера
# -------------------------------
echo "Запуск нового контейнера $CONTAINER_NAME"
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    --network host \
    -v "$LOG_DIR":/app/logs \
    $IMAGE_NAME

echo "Деплой завершён! Образ: $IMAGE_NAME"
