from fastapi import APIRouter, status, Depends, Query, Body
from typing import Any
from pymongo import MongoClient
from backend.models.contribute.example import ContributionResponse, ExampleContributionSchema
from backend.utils.database import get_db
from backend.controllers.contribute.example import example_contribution

app = APIRouter(
    tags=["Contribute"],
    prefix="/contribute"
)

@app.post(
    "/example",
    response_model=ContributionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Contribute New Content (Admin Only)",
    description="Allows an admin to contribute new examples or practice examples to the database. Requires a valid `admin_token` (configured in the server environment) for authorization.",
    response_description="Confirmation message indicating that example contribution was successful."
)
def contribute(
    admin_token: str = Query(
        ...,
        description="Admin authorization token. Must match the server-configured `ADMIN_TOKEN` environment variable."
    ),
    data: ExampleContributionSchema = Body(
        ...,
        description="The content data to be contributed."
    ),
    database: MongoClient = Depends(get_db)
) -> dict[str, Any]:
    return example_contribution(database, admin_token, data)