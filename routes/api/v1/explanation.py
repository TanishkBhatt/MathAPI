from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.explanation import ExplanationResponse
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
    description="Retrieves a detailed explanation for a specific mathematics topic by its unique topic ID. The response includes the definition, origin, real-world applications, step-by-step explanation sections, relevant formulae, and linked learning sources. Optionally includes up to 2 worked examples and up to 3 practice questions. Requires a valid `api_key` for access.",
    response_description="Comprehensive explanation object with optional embedded examples and practice questions."
)

@limiter.limit("100/hour")

async def explain(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve. Must match a valid `topic_id` from the `/get-topics` endpoint.",
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
            description="Whether to include 3 practice questions for the topic in the response."
        ),
        include_sources: bool = Query(
            False,
            description="Whether to include learning sources for the topic in the response."
        ),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await explain_topic(database, api_key, topic_id, include_formulae, include_examples, include_questions, include_sources)