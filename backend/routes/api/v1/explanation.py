from fastapi import APIRouter, status, Depends, Query
from typing import Any
from pymongo import MongoClient
from backend.models.api.v1.explanation import ExplanationResponse
from backend.utils.database import get_db
from backend.controllers.api.v1.explanation import explain_topic

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/explanation",
    response_model=ExplanationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Topic Explanation",
    description="Retrieves a detailed explanation for a specific mathematics topic by its unique topic ID. The response includes the definition, origin, real-world applications, step-by-step explanation sections, relevant formulae, and linked learning sources. Optionally includes up to 2 worked examples and up to 3 practice questions.",
    response_description="Comprehensive explanation object with optional embedded examples and practice questions."
)
def explain(
    api_key: str|None = None,
    topic_id: str = Query(
        ...,
        description="Unique identifier of the mathematics topic to retrieve. Must match a valid `topic_id` from the `/get-topics` endpoint.",
        examples=["quadratic-equation"]
    ),
    include_examples: bool = Query(
        True,
        description="Whether to include up to 2 worked examples for the topic in the response."
    ),
    include_questions: bool = Query(
        True,
        description="Whether to include up to 3 practice questions for the topic in the response."
    ),
    db: MongoClient = Depends(get_db)
) -> dict[str, Any]:
    return explain_topic(db, api_key, topic_id, include_examples, include_questions)
