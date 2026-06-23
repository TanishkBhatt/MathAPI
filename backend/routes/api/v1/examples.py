from fastapi import APIRouter, status, Depends, Query
from typing import Any
from pymongo import MongoClient
from backend.models.api.v1.examples import GetExamplesResponse
from backend.utils.database import get_db
from backend.controllers.api.v1.examples import get_examples

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/examples",
    response_model=GetExamplesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Worked Examples",
    description="Fetches step-by-step worked examples for a specific mathematics topic. Each example includes the question, key observation, concepts and formulae used, detailed solution steps, final answer, and interpretation. Authenticated requests (with a valid `auth_token` param) can request up to any number of examples; unauthenticated requests are limited to a maximum of 2 examples.",
    response_description="List of worked examples with full step-by-step solutions and explanations."
)
def examples(
    auth_token: str|None = None,
    topic_id: str = Query(
        ...,
        description="Unique identifier of the mathematics topic to retrieve examples for. Must match a valid `topic_id` from the `/get-topics` endpoint.",
        examples=["quadratic-equation"]
    ),
    limit: int = Query(
        2,
        ge=1,
        description="Maximum number of examples to return. Authenticated users can set this to any positive integer; unauthenticated requests are capped at 2 regardless of this value."
    ),
    db: MongoClient = Depends(get_db)
) -> dict[str, Any]:
    return get_examples(auth_token, db, topic_id, limit)