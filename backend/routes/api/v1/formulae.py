from fastapi import APIRouter, Request, status, Depends, Query
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.api.v1.formulae import GetFormulaeResponse
from backend.utils.database import get_db
from backend.controllers.api.v1.formulae import get_formulae
from backend.utils.limiter import limiter

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/formulae",
    response_model=GetFormulaeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Formulae",
    description="Fetches all formulae for a specific mathematics topic, LaTeX code for better rendering. Requires a valid `api_key` for access.",
    response_description="List of all formulae of a particular topic."
)

@limiter.limit("100/hour")

async def formulae(
        request: Request,
        api_key: str | None = Query(None, description="Your API key for authentication"),
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve formulae for. Must match a valid `topic_id` from the `/get-topics` endpoint.",
            examples=["quadratic-equations"]
        ),
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await get_formulae(database, api_key, topic_id)