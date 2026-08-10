from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter

# FETCHING API_KEY
# Requests without an API key are NOT rate-limited here: they fail
# authentication anyway, and must not consume a shared bucket that would
# later produce 429 responses for valid API keys.
def get_api_key(request: Request) -> str | None:
    return request.query_params.get("api_key")

# LIMITER OBJECT
limiter = Limiter(key_func=get_api_key)

# CUSTOM LIMIT EXCEEDED HANDLER FUNCTION
def limiting_response() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "API_KEY Rate Limit Exceeded."
        }
    )