from fastapi import APIRouter, status, Depends
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.auth.auth import AuthRequest, AuthResponse
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
    description="Registers a new user with a unique username and email address, then returns a generated API key. The API key is required for authenticated access on the GET endpoints.",
    response_description="Registration confirmation with the generated API key, username, and expiry information."
)
async def auth(
        data: AuthRequest, 
        database: AsyncIOMotorClient = Depends(get_db)
    ) -> dict[str, Any]:
    return await authenticate_user(database, data)