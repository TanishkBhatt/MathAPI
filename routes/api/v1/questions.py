from fastapi import APIRouter, Request, Response, status, Depends, Query
from typing import Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.questions import GetQuestionsResponse
from models.components.helpers import Difficulty, QuestionType
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.questions import get_questions
from utils.helpers import get_request_api_key
from utils.limiter import get_client_ip, limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/questions",
    response_model=GetQuestionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Practice Questions",
    description="Retrieves multiple-choice practice questions for a specific mathematics topic. Supports optional filtering by difficulty level and question type. Requires a valid API key via the `X-API-Key` header or `api_key` query parameter (100 requests per hour per API key across all Get API routes).",
    response_description="List of multiple-choice questions with options, difficulty metadata, expected time limits, hints and solution sources.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Missing, invalid or expired API key."
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No questions found for the given `topic_id`."
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

@limiter.shared_limit("100/hour", scope="get_api")
@limiter.shared_limit("300/hour", scope="get_api_ip", key_func=get_client_ip)

async def questions(
        request: Request,
        response: Response,
        api_key: str | None = Depends(get_request_api_key),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve questions for. Must match a valid `topic_id` from the `/api/v1/topics` endpoint.",
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
