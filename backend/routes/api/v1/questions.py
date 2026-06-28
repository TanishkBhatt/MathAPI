from fastapi import APIRouter, status, Depends, Query
from typing import Any, List
from pymongo import MongoClient
from backend.models.api.v1.questions import GetQuestionsResponse
from backend.models.components.helpers import Difficulty, QuestionType
from backend.utils.database import get_db
from backend.controllers.api.v1.questions import get_questions

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
def questions(
        api_key: str|None = None,
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve questions for. Must match a valid `topic_id` from the `/get-topics` endpoint.",
            examples=["quadratic-equation"]
        ),
        limit: int = Query(
            10,
            ge=1,
            description="Maximum number of questions to return. Requires a valid `api_key` to use."
        ),
        difficulty: Difficulty | None = Query(
            None,
            description="Filter questions by difficulty level. Valid values: `Beginner`, `Intermediate`, `Advanced`."
        ),
        question_type: QuestionType | None = Query(
            None,
            description="Filter questions by type category. Valid values: `Conceptual`, `Numerical`, `To Prove`, `Word Problem`, `Case Based`, `Higher Order Thinking Skills`."
        ),
        database: MongoClient = Depends(get_db)
    ) -> dict[str, Any]:
    return get_questions(database, api_key, topic_id, limit, difficulty, question_type)