from fastapi import APIRouter, Request, Response, status, Depends
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.daily_challenge import DailyChallengeResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.api.v1.daily_challenge import get_daily_challenge
from utils.helpers import get_request_api_key
from utils.limiter import get_client_ip, limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/daily-challenge",
    response_model=DailyChallengeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Daily Challenge Problems",
    description="Retrieves 3 daily challenge problems — one Beginner, one Intermediate and one Advanced. The same set is served to all users on a given day; a new set is assigned if none exists for today. Requires a valid API key via the `X-API-Key` header or `api_key` query parameter (100 requests per hour per API key across all Get API routes).",
    response_description="3 challenge questions with one per difficulty level.",
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

@limiter.shared_limit("100/hour", scope="get_api")
@limiter.shared_limit("300/hour", scope="get_api_ip", key_func=get_client_ip)

async def daily_challenge(
        request: Request,
        response: Response,
        api_key: str | None = Depends(get_request_api_key),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_daily_challenge(database, api_key)
