from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, Dict, List
from backend.models.auth.auth import AuthRequest
from backend.utils.database import get_documents, import_data
from backend.utils.helpers import generate_api_key

async def authenticate_user(
        database: AsyncIOMotorClient, 
        auth_data: AuthRequest
    ) -> Dict[str, Any]:

    # CHECKING IS USERNAME AND EMAIL ALREADY EXISTS OR NOT
    try:
        users: List[Dict[str, Any]] = await get_documents(
            database,
            "auth",
            "users",
            {
                "username": auth_data.username,
                "email": auth_data.email
            }
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    user: Dict[str, Any] = users[0] if users else {}
    if user:
        return {
        "success": True,
        "message": "User Is Already Authenticated",
        "api_key_data": {
            "username": auth_data.username,
            "api_key": user["api_key"]
            }
        }
    
    # GENERATING API_KEY
    exp: int|None = None
    api_key: str = generate_api_key(
            auth_data.username, 
            exp
        )

    # IMPORTING DATA TO DB
    try:
        await import_data(
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
            "api_key": api_key
        }
    }