from fastapi import APIRouter, Request, Response, status, Depends
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.random_question import RandomQuestionResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.random_question import get_random_question
from utils.helpers import get_request_api_key
from utils.limiter import get_client_ip, limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/random-question",
    response_model=RandomQuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a Random Question",
    description="Retrieves a single random question from the entire pool — any topic, any difficulty, any type. Requires a valid API key via the `X-API-Key` header or `api_key` query parameter (100 requests per hour per API key across all Get API routes).",
    response_description="A single random question object.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Missing, invalid or expired API key."
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No questions available in the database."
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

async def random_question(
        request: Request,
        response: Response,
        api_key: str | None = Depends(get_request_api_key),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_random_question(database, api_key)
