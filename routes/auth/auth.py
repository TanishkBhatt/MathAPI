from fastapi import APIRouter, status, Depends, Response
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.auth.auth import AuthRequest, AuthResponse
from models.errors import ErrorResponse
from utils.database import get_db
from controllers.auth.auth import authenticate_user

app = APIRouter(
    tags=["Auth"],
    prefix=""
)

@app.post(
    "/auth",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register and Obtain API Key",
    description="Registers a new user with a unique username and email address, then returns a generated API key valid for 6 months. The API key is required for authenticated access on the GET endpoints. Registering again with an existing username returns the same API key.",
    response_description="Registration confirmation with the generated API key, username, and expiry information. Returns 201 for new registrations and 200 when the username already exists.",
    responses={
        status.HTTP_200_OK: {
            "model": AuthResponse,
            "description": "Username already registered - the existing API key is returned."
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Database connection failed."
        }
    }
)
async def auth(
        data: AuthRequest,
        response: Response,
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    result = await authenticate_user(database, data)
    if result["message"] == "User Is Already Authenticated":
        response.status_code = status.HTTP_200_OK
    return result
