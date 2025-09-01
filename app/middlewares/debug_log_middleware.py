from fastapi import Request
from starlette.responses import Response
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

    # Перехватываем тело ответа
    resp_body = b""
    if hasattr(response, "body_iterator"):
        body_iterator = response.body_iterator
        new_iterator = []
        async for chunk in body_iterator:
            resp_body += chunk
            new_iterator.append(chunk)
        response.body_iterator = iter(new_iterator)  # чтобы клиент получил ответ

    elif hasattr(response, "body") and response.body:
        resp_body = response.body

    if isinstance(resp_body, memoryview):
        resp_body = resp_body.tobytes()
    if isinstance(resp_body, bytes):
        resp_body = resp_body.decode("utf-8", errors="ignore")

    # Заголовки ответа
    logger.info("RESPONSE HEADERS:")
    for k, v in dict(response.headers).items():
        logger.info(f"  {k}: {v}")

    # Тело ответа
    try:
        parsed = json.loads(resp_body)
        formatted_response = json.dumps(parsed, indent=2, ensure_ascii=False)
    except Exception:
        formatted_response = resp_body[:2048] if resp_body else "<empty>"

    logger.info("RESPONSE BODY:")
    for line in formatted_response.splitlines():
        logger.info(f"  {line}")

    return response
