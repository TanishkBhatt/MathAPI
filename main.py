from fastapi import FastAPI, Request
from routes import (
    home
)
from routes.auth import (
    auth
)
from routes.api.v1 import (
    explanation,
    examples,
    questions,
    formulae,
    topics,
    sources,
    daily_challenge,
    random_question
)

from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from utils.limiter import (
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
    docs_url=None   # Disable default docs
)

# CUSTOMIZATIONS
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,    # type: ignore
        title="MathAPI Docs"
    )

# INCLUDING ROUTERS
app.include_router(home.app)
app.include_router(auth.app)

app.include_router(topics.app)
app.include_router(explanation.app)
app.include_router(examples.app)
app.include_router(questions.app)
app.include_router(formulae.app)
app.include_router(sources.app)
app.include_router(daily_challenge.app)
app.include_router(random_question.app)

# CORS MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APPLYING LIMITING
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# CUSTOM LIMIT EXCEEDED HANDLER
@app.exception_handler(RateLimitExceeded)
async def custom_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return limiting_response()