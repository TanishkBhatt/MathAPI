from fastapi import FastAPI
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
        "description": "Core data retrieval endpoints for serving mathematical assets. Requires a valid `api_key`."
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