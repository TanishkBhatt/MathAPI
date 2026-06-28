from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, Dict, List
from backend.models.auth import AuthRequest
from backend.utils.database import get_documents, import_data
from backend.utils.helpers import generate_api_key

def authenticate_user(
        database: MongoClient, 
        auth_data: AuthRequest
    ) -> Dict[str, Any]:

    # CHECKING IS USERNAME AND EMAIL ARE UNIQUE OR NOT
    try:
        user: List[Dict[str, Any]] = get_documents(
            database,
            "auth",
            "users",
            {"username": auth_data.username}
        )
        email_user: List[Dict[str, Any]] = get_documents(
            database,
            "auth",
            "users",
            {"email": auth_data.email}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    if len(user) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid AuthRequest Input, This 'username' Already Exists."
        )
    
    if len(email_user) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid AuthRequest Input, This 'email' Already Exists."
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