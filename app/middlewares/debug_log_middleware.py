from fastapi import Request
from starlette.responses import Response, StreamingResponse
import logging
import json

logger = logging.getLogger("gunicorn.access")


async def debug_log_middleware(request: Request, call_next):
    # --- Логируем запрос ---
    logger.info(f"REQUEST: {request.method} {request.url}")

    logger.info("REQUEST HEADERS:")
    for k, v in dict(request.headers).items():
        logger.info(f"  {k}: {v}")

    # Тело запроса
    body = await request.body()
    if body:
        if isinstance(body, memoryview):
            body = body.tobytes()
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="ignore")
        try:
            parsed = json.loads(body)
            formatted_body = json.dumps(parsed, indent=2, ensure_ascii=False)
        except Exception:
            formatted_body = body[:2048]  # первые 2КБ, если не JSON

        logger.info("REQUEST BODY:")
        for line in formatted_body.splitlines():
            logger.info(f"  {line}")

    # --- Обрабатываем ответ ---
    response: Response = await call_next(request)

    # --- Копируем тело ответа ---
    resp_body = b""
    async for chunk in response.body_iterator:
        resp_body += chunk

    # Заголовки ответа
    logger.info("RESPONSE HEADERS:")
    for k, v in dict(response.headers).items():
        logger.info(f"  {k}: {v}")

    # Тело ответа (логируем копию)
    text_body = resp_body.decode("utf-8", errors="ignore") if resp_body else ""
    try:
        parsed = json.loads(text_body)
        formatted_response = json.dumps(parsed, indent=2, ensure_ascii=False)
    except Exception:
        formatted_response = text_body[:2048] if text_body else "<empty>"

    logger.info("RESPONSE BODY:")
    for line in formatted_response.splitlines():
        logger.info(f"  {line}")

    # Возвращаем оригинальный ответ клиенту
    return StreamingResponse(
        iter([resp_body]),
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
