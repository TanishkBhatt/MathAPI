from fastapi import APIRouter, status, Depends, Query, Body
from typing import Any
from pymongo import MongoClient
from backend.models.contribute import ContributionResponse, QuestionContributionSchema
from backend.utils.database import get_db
from backend.controllers.contribute import contribution

app = APIRouter(
    tags=["Contribute"],
    prefix=""
)

@app.post(
    "/contribute-question",
    response_model=ContributionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Contribute New Content (Admin Only)",
    description="Allows an admin to contribute new examples or practice questions to the database. Requires a valid `admin_token` (configured in the server environment) for authorization. The `contribution_type` parameter determines whether an Example or Question is being submitted, and the request body must match the corresponding schema.",
    response_description="Confirmation message indicating the type of contribution that was successfully added."
)
def contribute(
    
    admin_token: str = Query(
        ...,
        description="Admin authorization token. Must match the server-configured `ADMIN_TOKEN` environment variable."
    ),
    data: QuestionContributionSchema = Body(
        ...,
        description="The content data to be contributed."
    ),
    db: MongoClient = Depends(get_db)
) -> dict[str, Any]:
    return contribution(db, admin_token, data)