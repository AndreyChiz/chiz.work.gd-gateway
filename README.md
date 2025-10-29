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


---

 ## ⚙️ Установка и запуск <!--TODO: quick start -->

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
