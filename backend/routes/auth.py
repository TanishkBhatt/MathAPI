from fastapi import APIRouter, status, Depends
from typing import Any
from pymongo import MongoClient
from backend.models.auth import AuthRequest, AuthResponse
from backend.utils.db_config import get_db
from backend.controllers.auth import authenticate_user

app = APIRouter(
    tags=["Auth"]
)

@app.post(
    "/auth",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED
)

def auth(data: AuthRequest, db: MongoClient = Depends(get_db)) -> dict[str, Any]:
    return authenticate_user(db, data)