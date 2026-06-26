from fastapi import FastAPI
from backend.routes import (
    home,
    auth,
    contribute
)
from backend.routes.api.v1 import (
    get_topics,
    explanation,
    examples,
    questions
)

# DOCS METADATA TAGS
tags_metadata = [
    {
        "name": "Home",
        "description": "Health check and service status endpoints for verifying API connectivity."
    },
    {
        "name": "Auth",
        "description": "Authentication endpoints for obtaining and managing API access tokens."
    },
    {
        "name": "Get API",
        "description": "Core data retrieval endpoints for mathematics topics, explanations, examples, and practice questions. Authenticated access unlocks higher rate limits and additional filtering capabilities."
    },
    {
        "name": "Contribute",
        "description": "Admin-only endpoints for contributing new content (examples and questions) to the database. Requires a valid `admin_token` for authorization."
    }
]

description = "A RESTful API service designed for students and developers pursuing mathematics and related fields. Provides structured access to topic explanations, step-by-step worked examples, and practice questions of topics across various branches of elementary mathematics."

# INITIALIZING THE APP
app = FastAPI(
    title="MathAPI",
    description=description,
    version="1.0.0",
    summary="Mathematics Education API",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# INCLUDING ROUTERS
app.include_router(home.app)
app.include_router(auth.app)
app.include_router(contribute.app)

app.include_router(get_topics.app)
app.include_router(explanation.app)
app.include_router(examples.app)
app.include_router(questions.app)