from fastapi import APIRouter, status, Depends
from typing import Any
from pymongo import MongoClient
from backend.models.api.get_topics import GetAllTopicsResponse
from backend.utils.database import get_db
from backend.controllers.api.get_topics import get_topics

app = APIRouter(
    prefix="/api",
    tags=["API"]
)

@app.get(
    "/get-topics",
    response_model=GetAllTopicsResponse,
    status_code=status.HTTP_200_OK
)

def explain(db: MongoClient = Depends(get_db)) -> dict[str, Any]:
    return get_topics(db)