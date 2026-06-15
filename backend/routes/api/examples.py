from fastapi import APIRouter, status, Depends, Query
from typing import Any
from pymongo import MongoClient
from backend.models.api.examples import GetExamplesResponse
from backend.utils.database import get_db
from backend.controllers.api.examples import get_examples

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/examples",
    response_model=GetExamplesResponse,
    status_code=status.HTTP_200_OK
)

def examples(topic_id: str, limit: int = Query(2, ge=1), db: MongoClient = Depends(get_db)) -> dict[str, Any]:
    return get_examples(db, topic_id, limit)