import time
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from typing import Any, Dict, List
from config import settings
from models.auth.auth import AuthRequest
from utils.database import get_documents, import_data, update_documents, ensure_index
from utils.helpers import generate_api_key, compute_expiry

# BUILDS THE EXISTING USER RESPONSE, BACKFILLS LEGACY KEY EXPIRY AND REJECTS EXPIRED KEYS
async def _existing_user_response(
        database: AsyncIOMotorClient,
        user: Dict[str, Any]
    ) -> Dict[str, Any]:

    expiry: int | None = user.get("expiry")
    if expiry is None:
        expiry = compute_expiry(settings.API_KEY_VALID_MONTHS)
        try:
            await update_documents(
                database,
                "auth",
                "users",
                {"username": user["username"]},
                {"$set": {"expiry": expiry}}
            )
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    elif time.time() > expiry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key Expired, Create Another"
        )

    return {
        "username": user["username"],
        "api_key": user["api_key"],
        "expiry": time.ctime(expiry)
    }

async def authenticate_user(
        database: AsyncIOMotorClient, 
        auth_data: AuthRequest
    ) -> Dict[str, Any]:

    # ENFORCE ONE API KEY PER USERNAME (unique index + DuplicateKeyError guard)
    try:
        await ensure_index(
            database,
            "auth",
            "users",
            [("username", 1)],
            unique=True,
            index_name="username_unique"
        )
    except Exception:
        pass

    # CHECKING IS USERNAME ALREADY EXISTS OR NOT
    try:
        users: List[Dict[str, Any]] = await get_documents(
            database,
            "auth",
            "users",
            {"username": auth_data.username}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    user: Dict[str, Any] = users[0] if users else {}
    if user:
        api_key_data = await _existing_user_response(database, user)
        return {
            "success": True,
            "message": "User Is Already Authenticated",
            "api_key_data": api_key_data
        }
    
    # GENERATING API_KEY WITH A 6-MONTH EXPIRY
    exp: int = compute_expiry(settings.API_KEY_VALID_MONTHS)
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
            auth_data.model_dump() | {"api_key": api_key, "expiry": exp}
        )
    except DuplicateKeyError:
        users = await get_documents(
            database,
            "auth",
            "users",
            {"username": auth_data.username}
        )
        if users:
            api_key_data = await _existing_user_response(database, users[0])
            return {
                "success": True,
                "message": "User Is Already Authenticated",
                "api_key_data": api_key_data
            }
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error In Connecting With Database"
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
            "expiry": time.ctime(exp)
        }
    }