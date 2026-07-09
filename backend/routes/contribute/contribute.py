from fastapi import APIRouter, status, Depends, Query, Body
from typing import Any, Dict, List
from pymongo import MongoClient
from backend.models.contribute.contribute import ContributionResponse, ContributionType
from backend.utils.database import get_db
from backend.controllers.contribute.contribute import contribution

app = APIRouter(
    tags=["Contribute"]
)

@app.post(
    "/contribute",
    response_model=ContributionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Contribute New Content (Admin Only)",
    description="Allows an admin to contribute new examples or practice questions to the database. Requires a valid `admin_token` (configured in the server environment) for authorization.",
    response_description="Confirmation message indicating that contribution was successful."
)
def contribute(
    admin_token: str = Query(
        ...,
        description="Admin authorization token. Must match the server-configured `ADMIN_TOKEN` environment variable."
    ),
    contribution_type: ContributionType = "Question",   # type: ignore
    data: List[Dict[str, Any]] = Body(
        ...,
        description="List of the content data to be contributed."
    ),
    database: MongoClient = Depends(get_db)
) -> dict[str, Any]:
    return contribution(database, admin_token, contribution_type, data)