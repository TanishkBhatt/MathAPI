import time
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError, PyMongoError
from typing import Any, Dict, List
from config import settings
from models.auth.auth import AuthRequest
from utils.database import get_documents, import_data, update_documents, ensure_index
from utils.helpers import generate_api_key, compute_expiry


def _normalize_email(email: str) -> str:
    return email.strip().lower()


# BUILDS THE EXISTING USER RESPONSE, BACKFILLS LEGACY KEY EXPIRY AND ROTATES EXPIRED KEYS
async def _existing_user_response(database: AsyncIOMotorClient, user: Dict[str, Any], email: str) -> tuple[Dict[str, Any], bool]:
    stored_email = _normalize_email(str(user.get("email") or ""))
    if stored_email != _normalize_email(email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username Already Registered With A Different Email"
        )

    expiry: int | None = user.get("expiry")
    if expiry is None:
        expiry = compute_expiry(settings.API_KEY_VALID_MONTHS)
        try:
            await update_documents(database, "auth", "users", {"username": user["username"]}, {"$set": {"expiry": expiry}})
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    elif time.time() > expiry:
        new_expiry: int = compute_expiry(settings.API_KEY_VALID_MONTHS)
        new_api_key: str = generate_api_key(user["username"], new_expiry)
        users = database["auth"]["users"]
        try:
            updated = await users.find_one_and_update(
                {"username": user["username"], "api_key": user["api_key"], "expiry": {"$lte": time.time()}},
                {"$set": {"api_key": new_api_key, "expiry": new_expiry}},
                return_document=ReturnDocument.AFTER
            )
            if updated is None:
                updated = await users.find_one({"username": user["username"]})
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )

        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error In Connecting With Database"
            )

        api_key = updated.get("api_key")
        current_expiry = updated.get("expiry")
        if not api_key or current_expiry is None or time.time() > current_expiry:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="API Key Rotation Failed"
            )

        return {
            "username": updated["username"],
            "api_key": api_key,
            "expiry": time.ctime(current_expiry)
        }, True

    return {
        "username": user["username"],
        "api_key": user["api_key"],
        "expiry": time.ctime(expiry)
    }, False


def _existing_user_result(api_key_data: Dict[str, Any], rotated: bool) -> Dict[str, Any]:
    return {
        "success": True,
        "message": "API Key Expired - New API Key Generated" if rotated else "User Is Already Authenticated",
        "api_key_data": api_key_data
    }

async def authenticate_user(database: AsyncIOMotorClient, auth_data: AuthRequest) -> Dict[str, Any]:
    # ENFORCE ONE API KEY PER USERNAME (unique index + DuplicateKeyError guard)
    try:
        await ensure_index(database, "auth", "users", [("username", 1)], unique=True, index_name="username_unique")
        await ensure_index(database, "auth", "users", [("api_key", 1)], unique=True, index_name="api_key_unique")
    except PyMongoError:
        pass

    # CHECKING IS USERNAME ALREADY EXISTS OR NOT
    try:
        users: List[Dict[str, Any]] = await get_documents(database, "auth", "users", {"username": auth_data.username})
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    user: Dict[str, Any] = users[0] if users else {}
    if user:
        api_key_data, rotated = await _existing_user_response(database, user, auth_data.email)
        return _existing_user_result(api_key_data, rotated)
    
    # GENERATING API_KEY WITH A 6-MONTH EXPIRY
    exp: int = compute_expiry(settings.API_KEY_VALID_MONTHS)
    api_key: str = generate_api_key(auth_data.username, exp)

    # IMPORTING DATA TO DB
    try:
        await import_data(database, "auth", "users", auth_data.model_dump() | {"api_key": api_key, "expiry": exp})
    except DuplicateKeyError:
        users = await get_documents(database, "auth", "users", {"username": auth_data.username})
        if users:
            api_key_data, rotated = await _existing_user_response(database, users[0], auth_data.email)
            return _existing_user_result(api_key_data, rotated)
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