from fastapi import APIRouter, status
from typing import Any
from backend.models.home import HomeResponse

app = APIRouter(
    tags=["Home"]
)

@app.get(
    "/",
    response_model=HomeResponse,
    status_code=status.HTTP_200_OK,
    summary="API Health Check",
    description="Returns a health-check response confirming that the MathAPI service is running and accessible. Use this endpoint to verify connectivity before making other API calls.",
    response_description="Service status confirmation with success flag and welcome message."
)
def home() -> dict[str, Any]:
    return {
        "success": True,
        "message": "MathAPI - API Services Connected Successfully"
    }