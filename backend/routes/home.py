from fastapi import APIRouter, status
from typing import Any
from backend.models.home import HomeResponse

app = APIRouter(
    prefix="",
    tags=["Home"]
)

@app.get(
    "/",
    response_model=HomeResponse,
    status_code=status.HTTP_200_OK
)

def home() -> dict[str, Any]:
    return {
        "connection": True,
        "message": "MathAPI - Web Services Connected Successfully"
    }