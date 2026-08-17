from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.api.v1.sources import GetSourcesResponse
from utils.database import get_db
from controllers.api.v1.sources import get_sources
from utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/sources",
    response_model=GetSourcesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Sources",
    description="Fetches all learning sources for a specific mathematics topic, including both plain text and LaTeX code for better rendering. Requires a valid `api_key` for access.",
    response_description="List of all learning sources of a particular topic."
)

@limiter.limit("100/hour")

async def sources(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve learning sources for. Must match a valid `topic_id` from the `/get-topics` endpoint.",
            examples=["quadratic-equations"]
        ),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_sources(database, api_key, topic_id)