from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.topics import GetAllTopicsResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.topics import get_topics
from utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/topics",
    response_model=GetAllTopicsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve All Available Topics",
    description="Fetches a comprehensive list of all mathematics topics available in the database. Each topic includes metadata such as difficulty level, branch classification, prerequisites, related topics, sub-topics, and counts of available learning resources (formulae, examples, questions and learning sources). Requires a valid `api_key` for access (100 requests per hour per API key).",
    response_description="List of all topics with detailed metadata and resource availability counts.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Missing, invalid or expired API key."
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

async def topics(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication", examples=["mathapi_key_4f2ab9c81d0e_Xk7mQ2pT9vLwRn3yJd8sFgH1cE_exp=1782144000"]),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_topics(database, api_key)
