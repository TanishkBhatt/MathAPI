import hashlib
import os
from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter

from config import settings


def _get_storage_uri() -> str:
    if settings.RATE_LIMIT_STORAGE_URI:
        return settings.RATE_LIMIT_STORAGE_URI
    if os.getenv("VERCEL"):
        return settings.DB_CONNECTION_URL
    return "memory://"


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def get_api_key(request: Request) -> str:
    api_key = request.headers.get("x-api-key") or request.query_params.get("api_key")
    if api_key:
        digest = hashlib.sha256(api_key.encode()).hexdigest()[:32]
        return f"key:{digest}"
    return f"ip:{get_client_ip(request)}"


limiter = Limiter(
    key_func=get_api_key,
    storage_uri=_get_storage_uri(),
    headers_enabled=True,
    swallow_errors=True,
)


def limiting_response(
        request: Request | None = None,
        exc: Exception | None = None
    ) -> JSONResponse:

    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Rate Limit Exceeded."
        },
        headers=headers
    )
