from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.examples import GetExamplesResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.examples import get_examples
from utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/examples",
    response_model=GetExamplesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Worked Examples",
    description="Fetches step-by-step worked examples for a specific mathematics topic. Each example includes the question, key observation, concepts and formulae used, detailed solution steps, final answer and interpretation. Requires a valid `api_key` for access (100 requests per hour per API key).",
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

@limiter.limit("100/hour")

async def examples(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication", examples=["mathapi_key_4f2ab9c81d0e_Xk7mQ2pT9vLwRn3yJd8sFgH1cE_exp=1782144000"]),
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
