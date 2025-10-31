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

 ## ⚙️ Quick start for dev dev

 ```sh
# if postgres volume is exist, you need to run:
#sudo chmod 777 -R ./postgres   

 docker compose -f compose.dev.yml  up --build -d
 ```

 *for prod all in CICD*
