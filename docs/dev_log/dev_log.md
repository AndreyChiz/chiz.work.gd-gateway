```sh
uv init --app
uv add fastapi --extra standard
uv add gunicorn
uv run fatspi dev
# uv run fastapi run 
```

# Деплой докер

```sh

cd /home/www/chiz.work.gb-backend
docker build -t chiz_api_gateway .
```

```sh
docker run -d --name chiz_api_gateway \
  -p 8001:8001 \
  --restart unless-stopped \
  -v /home/www/log/chiz.work.gd:/app/logs \
  chiz-backend
```
