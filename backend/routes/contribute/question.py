from fastapi import APIRouter, status, Depends, Query, Body
from typing import Any
from pymongo import MongoClient
from backend.models.contribute.question import ContributionResponse, QuestionContributionSchema
from backend.utils.database import get_db
from backend.controllers.contribute.question import question_contribution

app = APIRouter(
    tags=["Contribute"],
    prefix="/contribute"
)

@app.post(
    "/question",
    response_model=ContributionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Contribute New Content (Admin Only)",
    description="Allows an admin to contribute new examples or practice questions to the database. Requires a valid `admin_token` (configured in the server environment) for authorization.",
    response_description="Confirmation message indicating that question contribution was successful."
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
    database: MongoClient = Depends(get_db)
) -> dict[str, Any]:
    return question_contribution(database, admin_token, data)