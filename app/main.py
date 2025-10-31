import secrets
from datetime import datetime, timedelta

from fastapi import Cookie, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from .middlewares.debug_log_middleware import debug_log_middleware
from fastapi.responses import JSONResponse


app = FastAPI(
    root_path="/api",
    docs_url="/docs",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "deepLinking": True,  # ссылки на конкретные эндпоинты
        "displayRequestDuration": True,  # показывать время запроса
    },
)

origins = [
    "http://10.60.170.51",
    "http://10.60.170.51:0",
    "http://localhost:5173",  # Vite React dev server
    "http://127.0.0.1:5173",
    "https://chiz.work.gd",  # продакшен фронт
]

# origins = ["*"

# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # обязательно для работы с cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(debug_log_middleware)


mock_users = [
    {
        "id": 5,
        "username": "achi",
        "email": "achi@example.com",
        "role": "admin",
        "permissions": ["read", "write", "delete"],
    },
    {
        "id": 2,
        "username": "zoo",
        "email": "zoo@zoo.com",
        "role": "user",
        "permissions": ["read", "write", "delete"],
    },
]

# Псевдо-хранилище токенов (в реальности -> Redis/БД)
issued_tokens = {"access": {123}, "refresh": {}}

ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7


def create_token(token_type: str, user_id: int, expire_delta: timedelta):
    """Создание мокового токена"""
    token = secrets.token_hex(16)
    expires = datetime.utcnow() + expire_delta
    issued_tokens[token_type][token] = {"sub": user_id, "expires": expires}
    return token


def verify_token(token_type: str, token: str):
    """Проверка токена"""
    data = issued_tokens[token_type].get(token)
    if not data:
        return None
    if data["expires"] < datetime.utcnow():
        return None
    return data["user_id"]


# @app.post("/login")
# def login(response: Response):
#     # Мок: сразу "авторизуем"
#     user_id = mock_users["id"]

#     access_token = create_token(
#         "access", user_id, timedelta(minutes=ACCESS_EXPIRE_MINUTES)
#     )
#     refresh_token = create_token(
#         "refresh", user_id, timedelta(days=REFRESH_EXPIRE_DAYS)
#     )

#     # Устанавливаем токены в HttpOnly cookie
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         max_age=ACCESS_EXPIRE_MINUTES * 60,
#         secure=False,
#         samesite="lax",
#     )
#     response.set_cookie(
#         key="refresh_token",
#         value=refresh_token,
#         httponly=True,
#         max_age=REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
#         secure=False,
#         samesite="lax",
#     )

#     return {"message": "Logged in successfully"}


@app.get("/user/me")
def get_me(id: int = 1):
    # ищем пользователя
    user = next((u for u in mock_users if u["id"] == id), None)
    if not user:
        return JSONResponse(content={"detail": "User not found"}, status_code=404)

    response = JSONResponse(content=user)
    response.headers["My_custom_wwwwww8"] = "suka"  # кастомный заголовок
    return response


@app.post("/auth/refresh")
def refresh_token(response: Response, refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    response.set_cookie(
        key="access_token",
        value="My_chiz_access_token",
        max_age=ACCESS_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )

    return {"message": "Access token refreshed"}


@app.post("/auth/register")
def register(response: JSONResponse):
    response = JSONResponse(content={"hey": "you1"})
    response.set_cookie(
        key="refresh_token",
        value="My_chiz_REFRESH_token",
        httponly=True,
        max_age=ACCESS_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )
    response.set_cookie(
        key="access_token",
        value="My_chiz_ACCESS_token",
        max_age=ACCESS_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )
    return response
