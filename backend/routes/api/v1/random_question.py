from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.api.v1.random_question import RandomQuestionResponse
from backend.utils.database import get_db
from backend.controllers.api.v1.random_question import get_random_question
from backend.utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/random-question",
    response_model=RandomQuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a Random Question",
    description="Retrieves a single random question from the entire pool — any topic, any difficulty, any type.",
    response_description="A single random question object."
)

@limiter.limit("100/hour")

async def random_question(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_random_question(database, api_key)
