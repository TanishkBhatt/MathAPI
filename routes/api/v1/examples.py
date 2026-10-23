from fastapi import APIRouter, Request, Response, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.examples import GetExamplesResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.examples import get_examples
from utils.helpers import get_request_api_key
from utils.limiter import get_client_ip, limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/examples",
    response_model=GetExamplesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Worked Examples",
    description="Fetches step-by-step worked examples for a specific mathematics topic. Each example includes the question, key observation, concepts and formulae used, detailed solution steps, final answer and interpretation. Requires a valid API key via the `X-API-Key` header or `api_key` query parameter (100 requests per hour per API key across all Get API routes).",
    response_description="List of worked examples with full step-by-step solutions and explanations.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Missing, invalid or expired API key."
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No examples found for the given `topic_id`."
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

async def examples(
        request: Request,
        response: Response,
        api_key: str | None = Depends(get_request_api_key),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve examples for. Must match a valid `topic_id` from the `/api/v1/topics` endpoint.",
            examples=["quadratic-equations"]
        ),
        limit: int = Query(
            2,
            ge=1,
            description="Maximum number of examples to return."
        ),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_examples(database, api_key, topic_id, limit)
