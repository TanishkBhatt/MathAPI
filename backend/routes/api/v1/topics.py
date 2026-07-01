from fastapi import APIRouter, status, Depends
from typing import Any
from pymongo import MongoClient
from backend.models.api.v1.topics import GetAllTopicsResponse
from backend.utils.database import get_db
from backend.controllers.api.v1.topics import get_topics

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
    response_description="Paginated list of all topics with detailed metadata and resource availability counts."
)
def topics(
        api_key: str|None = None, 
        database: MongoClient = Depends(get_db)
    ) -> dict[str, Any]:
    return get_topics(database, api_key)