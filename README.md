# chiz.work.gd-gateway 🚀

![Status](https://img.shields.io/badge/status-in%20development-yellow)

**chiz.work.gd-gateway** — это API Gateway, построенный на FastAPI и Python. Он управляет маршрутизацией запросов, авторизацией и интеграцией с внутренними сервисами.  

> ⚠️ Проект в разработке. Некоторые функции могут быть недоступны или изменяться без предупреждения.

---

## 💡 Основные возможности
- Роутинг запросов к внутренним микросервисам
- Авторизация и аутентификация через Bearer Token
- Логирование и мониторинг запросов
- Простая интеграция с Docker и Kubernetes

---

## 🛠 Технологии
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

---

## ⚙️ Установка и запуск

1. Клонируйте репозиторий:

```sh
git clone https://github.com/AndreyChiz/chiz.work.gd-gateway.git
cd chiz.work.gd-gateway
uv init --app
uv add fastapi --extra standard
uv add gunicorn
uv run fatspi dev
# uv run fastapi run
```
