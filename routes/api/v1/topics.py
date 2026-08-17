from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.topics import GetAllTopicsResponse
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
    description="Fetches a comprehensive list of all mathematics topics available in the database. Each topic includes metadata such as difficulty level, branch classification, prerequisites, related topics, sub-topics, and counts of available learning resources (formulae, explanations, examples, and questions). Requires a valid `api_key` for access.",
    response_description="List of all topics with detailed metadata and resource availability counts."
)

@limiter.limit("100/hour")

async def topics(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_topics(database, api_key)