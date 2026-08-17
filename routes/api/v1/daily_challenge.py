from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.daily_challenge import DailyChallengeResponse
from utils.database import get_db
from controllers.api.v1.daily_challenge import get_daily_challenge
from utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/daily-challenge",
    response_model=DailyChallengeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Daily Challenge Problems",
    description="Retrieves 3 daily challenge problems — one Beginner, one Intermediate, and one Advanced. The same set is served to all users on a given day. Assigns a new set if none exists for today.",
    response_description="3 challenge questions with one per difficulty level."
)

@limiter.limit("100/hour")

async def daily_challenge(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_daily_challenge(database, api_key)