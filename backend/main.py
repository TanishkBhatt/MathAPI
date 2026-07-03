from fastapi import FastAPI, Request
from backend.routes import (
    home
)
from backend.routes.auth import (
    auth
)
from backend.routes.api.v1 import (
    explanation,
    examples,
    questions,
    formulae,
    topics
)
from backend.routes.contribute import (
    question,
    example
)

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from backend.utils.limiter import (
    limiter,
    limiting_response
)

# DOCS METADATA TAGS
tags_metadata = [
    {
        "name": "Home",
        "description": "Health check and help route."
    },
    {
        "name": "Auth",
        "description": "Authentication endpoints for obtaining the API key."
    },
    {
        "name": "Contribute",
        "description": "Admin-only endpoints for contributing new content (questions) to the database. Requires a valid `admin_token`."
    },
    {
        "name": "Get API",
        "description": "Core data retrieval endpoints for serving mathematical assets. Requires a valid `api_key` (100 requests per hour limit)"
    }
]

description = "A `RESTful API Services` designed for students and developers pursuing mathematics and related fields. Provides structured access to topic explanations, step-by-step worked examples, practice questions and concise formulae sheets of topics across various branches mathematics."

# INITIALIZING THE APP
app = FastAPI(
    title="MathAPI",
    description=description,
    version="1.0.0",
    summary="Mathematics Education API Services",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# INCLUDING ROUTERS
app.include_router(home.app)
app.include_router(auth.app)

app.include_router(topics.app)
app.include_router(explanation.app)
app.include_router(examples.app)
app.include_router(questions.app)
app.include_router(formulae.app)

app.include_router(question.app)
app.include_router(example.app)

# APPLYING LIMITING
app.state.limiter = limiter
app.add_exception_handler(
        RateLimitExceeded, 
        _rate_limit_exceeded_handler    # type: ignore
    )
app.add_middleware(SlowAPIMiddleware)

# CUSTOM LIMIT EXCEEDED HANDLER
@app.exception_handler(RateLimitExceeded)
async def custom_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return limiting_response()