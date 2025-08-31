# Идентифифкация авторизации пользователя.

### Цель

- Связать приложение с фронтом, сделать мок ручки авторизации, настроить серверное окружение nginx+gunicorn+uvicorn
- oauth2 acces refresh токены в httponly.
Настроить логирование, логи вынести в /home/www/logs/backend/

### Задача

- post /api/login
- get /api/me
- post /api/refresh


### Требования

- gunicorn
- fastapi
- uvicorn
- systemd unit

Tags: Auth dunicorn uvicorn fastapi server


### Решение 
