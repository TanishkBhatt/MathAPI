from fastapi import APIRouter, status, Depends
from typing import Any
from pymongo import MongoClient
from backend.models.api.explination import ExplinationResponse
from backend.utils.database import get_db
from backend.controllers.api.explination import explain_topic

app = APIRouter(
    prefix="/api",
    tags=["API"]
)

@app.get(
    "/explination/{topic_name}",
    response_model=ExplinationResponse,
    status_code=status.HTTP_200_OK
)

def explain(topic_name: str, db: MongoClient = Depends(get_db)) -> dict[str, Any]:
    return explain_topic(db, topic_name)