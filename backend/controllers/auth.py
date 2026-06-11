from fastapi import HTTPException
from pydantic import ValidationError
from pymongo import MongoClient
from typing import Any
from backend.models.auth import AuthRequest

def authenticate_user(db: MongoClient, data: AuthRequest) -> dict[str, Any]:
    return {
        "success": True,
        "message": "User Have Been Successfully Authenticated",
        "auth_token": {}
    }