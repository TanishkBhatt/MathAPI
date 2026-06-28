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
    description="Returns a health-check response confirming that the MathAPI service is running and accessible. Also provides a guide to proceed.",
    response_description="Service status confirmation with success flag and welcome message."
)
def home() -> dict[str, Any]:
    return {
        "success": True,
        "message": "MathAPI - API Services",
        "help": {
            "get_started": "Go to our documentation, then go to the POST auth/ route, submit your details and get an api_key.",
            "explore_routes": "We have currently a total of 5 routes serving topics, explanations, worked examples, practice questions and formulae sheets respectivly.",
            "contribution": "You can contribute a question through POST /contribute-question route via a protected admin_token."
        },
        "docs": "https://mathapi.vercel.app/docs",
        "repo": "https://github.com/TanishkBhatt/MathAPI",
        "author": "Tanishk Bhatt - A Student and A Programmer"
    }