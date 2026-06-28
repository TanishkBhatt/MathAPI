from fastapi import APIRouter, status, Depends, Query
from typing import Any
from pymongo import MongoClient
from backend.models.api.v1.formulae import GetFormulaeResponse
from backend.utils.database import get_db
from backend.controllers.api.v1.formulae import get_formulae

app = APIRouter(
    prefix="/api/v1",
    tags=["Get API"]
)

@app.get(
    "/formulae",
    response_model=GetFormulaeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Formulae",
    description="Fetches all formulae for a specific mathematics topic, including both plain text and LaTeX code for better rendering. Requires a valid `api_key` for access.",
    response_description="List of all formulae of a particular topic."
)
def formulae(
        api_key: str|None = None,
        topic_id: str = Query(
            ...,
            description="Unique identifier of the mathematics topic to retrieve formulae for. Must match a valid `topic_id` from the `/get-topics` endpoint.",
            examples=["quadratic-equation"]
        ),
        database: MongoClient = Depends(get_db)
    ) -> dict[str, Any]:
    return get_formulae(database, api_key, topic_id)