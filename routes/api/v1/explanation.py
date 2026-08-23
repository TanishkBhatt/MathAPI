from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.explanation import ExplanationResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.explanation import explain_topic
from utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/explanation",
    response_model=ExplanationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Topic Explanation",
    description="Retrieves a detailed explanation for a specific mathematics topic by its unique topic ID. The response includes the definition, origin, real-world applications and step-by-step explanation sections. Optionally includes related formulae, up to 2 worked examples, 3 Beginner-level practice questions and learning sources via the include flags. Requires a valid `api_key` for access (100 requests per hour per API key).",
    response_description="Comprehensive explanation object with optional embedded formulae, worked examples, practice questions and learning sources.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Missing, invalid or expired API key."
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No explanation found for the given `topic_id`."
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "model": ErrorResponse,
            "description": "Hourly request limit of 100 exceeded for this API key."
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Database connection failed."
        }
    }
)

@limiter.limit("100/hour")

async def explain(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication", examples=["mathapi_key_4f2ab9c81d0e_Xk7mQ2pT9vLwRn3yJd8sFgH1cE_exp=1782144000"]),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve. Must match a valid `topic_id` from the `/api/v1/topics` endpoint.",
            examples=["quadratic-equations"]
        ),
        include_formulae: bool = Query(
            False,
            description="Whether to include all formulae related to that topic in the response."
        ),
        include_examples: bool = Query(
            False,
            description="Whether to include 2 worked examples for the topic in the response."
        ),
        include_questions: bool = Query(
            False,
            description="Whether to include 3 Beginner-level practice questions for the topic in the response."
        ),
        include_sources: bool = Query(
            False,
            description="Whether to include learning sources for the topic in the response."
        ),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await explain_topic(database, api_key, topic_id, include_formulae, include_examples, include_questions, include_sources)
