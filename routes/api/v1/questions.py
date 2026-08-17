from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.questions import GetQuestionsResponse
from models.components.helpers import Difficulty, QuestionType
from utils.database import get_db
from controllers.api.v1.questions import get_questions
from utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/questions",
    response_model=GetQuestionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Practice Questions",
    description="Retrieves multiple-choice practice questions for a specific mathematics topic. Supports optional filtering by difficulty level and question type. Requires a valid `api_key` for access.",
    response_description="List of multiple-choice questions with options, difficulty metadata, expected time limits, hints, and solution sources."
)

@limiter.limit("100/hour")

async def questions(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve questions for. Must match a valid `topic_id` from the `/get-topics` endpoint.",
            examples=["quadratic-equations"]
        ),
        limit: int = Query(
            10,
            ge=1,
            description="Maximum number of questions to return."
        ),
        difficulty: Difficulty | None = Query(
            None,
            description="Filter questions by difficulty level. Valid values: `Beginner`, `Intermediate`, `Advanced`."
        ),
        question_type: QuestionType | None = Query(
            None,
            description="Filter questions by type category. Valid values: `Conceptual`, `Numerical`, `To Prove`, `Word Problem`, `Case Based`, `Higher Order Thinking Skills`."
        ),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_questions(database, api_key, topic_id, limit, difficulty, question_type)