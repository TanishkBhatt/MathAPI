from fastapi import APIRouter, status, Depends, Query
from typing import Any
from pymongo import MongoClient
from backend.models.api.questions import GetQuestionsResponse
from backend.models.objects.helpers import Difficulty
from backend.utils.db_config import get_db
from backend.controllers.api.questions import get_questions

app = APIRouter(
    prefix="/api",
    tags=["API"]
)

@app.get(
    "/questions/{topic_name}",
    response_model=GetQuestionsResponse,
    status_code=status.HTTP_200_OK
)

def questions(topic_name: str, limit: int = Query(10, ge=1), difficulty: Difficulty | None = None, db: MongoClient = Depends(get_db)) -> dict[str, Any]:
    return get_questions(db, topic_name, limit, difficulty)