import secrets
from datetime import datetime, timedelta

from fastapi import Cookie, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite React dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # обязательно для работы с cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

# Мок база пользователей
mock_user = {
    "id": 1,
    "username": "achi",
    "email": "achi@example.com",
    "role": "admin",
    "permissions": ["read", "write", "delete"],
}

# Псевдо-хранилище токенов (в реальности -> Redis/БД)
issued_tokens = {"access": {}, "refresh": {}}

ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7


def create_token(token_type: str, user_id: int, expire_delta: timedelta):
    """Создание мокового токена"""
    token = secrets.token_hex(16)
    expires = datetime.utcnow() + expire_delta
    issued_tokens[token_type][token] = {"user_id": user_id, "expires": expires}
    return token


def verify_token(token_type: str, token: str):
    """Проверка токена"""
    data = issued_tokens[token_type].get(token)
    if not data:
        return None
    if data["expires"] < datetime.utcnow():
        return None
    return data["user_id"]


@app.post("/api/login")
def login(response: Response):
    # Мок: сразу "авторизуем"
    user_id = mock_user["id"]

    access_token = create_token(
        "access", user_id, timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        "refresh", user_id, timedelta(days=REFRESH_EXPIRE_DAYS)
    )

    # Устанавливаем токены в HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
        secure=False,
        samesite="lax",
    )

    return {"message": "Logged in successfully"}


@app.get("/api/me")
def get_me(access_token: str | None = Cookie(default=None)):
    """Защищённый эндпоинт"""
    if not access_token or not verify_token("access", access_token):
        raise HTTPException(status_code=401, detail="Not authorized")
    return mock_user


@app.post("/api/refresh")
def refresh_token(response: Response, refresh_token: str | None = Cookie(default=None)):
    if not refresh_token or not verify_token("refresh", refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = issued_tokens["refresh"][refresh_token]["user_id"]

    new_access_token = create_token(
        "access", user_id, timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=ACCESS_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )

    return {"message": "Access token refreshed"}
