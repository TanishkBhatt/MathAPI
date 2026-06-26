from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, Dict, List
from backend.models.auth import AuthRequest
from backend.utils.database import get_documents, get_all, import_data
from backend.utils.helpers import generate_api_key

def authenticate_user(database: MongoClient, auth_data: AuthRequest) -> Dict[str, Any]:
    # CHECKING IS AUTH_DETAILS ARE UNIQUE OR NOT
    try:
        all_users: List[Dict[str, Any]] = get_documents(
                database,
                "auth",
                "users"
            )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    fields: List[str] = ["username", "email"]
    values: List[str] = [auth_data.username, auth_data.email]
    all_users_values: List[set[str]] = [
            get_all(all_users, "username"), 
            get_all(all_users, "email")
        ]

    for field, value, all_users_value in zip(fields, values, all_users_values):
        if value in all_users_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid '{field}' Input, It Already Exists"
            )
    
    # GENERATING API_KEY
    exp: int|None = None
    api_key: str = generate_api_key(
        auth_data.username, 
        exp
    )

    # IMPORTING DATA TO DB
    try:
        import_data(
            database,
            "auth",
            "users",
            auth_data.model_dump() | {"api_key": api_key}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": "User Have Been Successfully Authenticated",
        "api_key_data": {
            "username": auth_data.username,
            "api_key": api_key,
            "expiry": exp
        }
    }