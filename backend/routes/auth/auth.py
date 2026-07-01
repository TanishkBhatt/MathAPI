from fastapi import APIRouter, status, Depends
from typing import Any
from pymongo import MongoClient
from backend.models.auth.auth import AuthRequest, AuthResponse
from backend.utils.database import get_db
from backend.controllers.auth.auth import authenticate_user

app = APIRouter(
    tags=["Auth"],
    prefix=""
)

@app.post(
    "/auth",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register and Obtain API Key",
    description="Registers a new user with a unique username and email address, then returns a generated API key. The API key is required for authenticated access to higher rate limits and additional filtering capabilities on the GET endpoints. Username and email must be unique — duplicates are rejected with a 400 error.",
    response_description="Registration confirmation with the generated API key, username, and optional expiry information."
)
def auth(
        data: AuthRequest, 
        database: MongoClient = Depends(get_db)
    ) -> dict[str, Any]:
    return authenticate_user(database, data)