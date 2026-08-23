from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter

# FETCHING API_KEY WITH CLIENT-IP FALLBACK FOR ANONYMOUS TRAFFIC
def get_api_key(request: Request) -> str:
    api_key = request.query_params.get("api_key")
    if api_key:
        return api_key
    if request.client and request.client.host:
        return f"anonymous:{request.client.host}"
    return "anonymous"

# LIMITER OBJECT
limiter = Limiter(key_func=get_api_key)

# CUSTOM LIMIT EXCEEDED HANDLER FUNCTION
def limiting_response(
        request: Request | None = None,
        exc: Exception | None = None
    ) -> JSONResponse:

    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "API_KEY Rate Limit Exceeded."
        },
        headers=headers
    )
