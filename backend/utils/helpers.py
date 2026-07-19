import hashlib
import secrets
import time
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

def generate_api_key(
        username: str,
        expiry: int | None
    ) -> str:
    user_hash: str = hashlib.sha256(username.encode()).hexdigest()[:12]
    api_key: str = f"mathapi_key_{user_hash}_{secrets.token_urlsafe(24)}_exp={expiry}"
    return api_key

async def verify_api_key(
        db_conn: AsyncIOMotorClient,
        api_key: str
    ) -> bool:
    db = db_conn["auth"]
    coll = db["users"]

    try:
        user = await coll.find_one({"api_key": api_key})
    except Exception:
        raise ConnectionError("Error In Connecting With Database")

    if user is None:
        return False

    expiry = user.get("expiry")
    if expiry is not None and time.time() > expiry:
        return False

    return True

async def validate_api_key(database: AsyncIOMotorClient, api_key: str | None) -> None:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access - Valid API Key Required"
        )
    try:
        authenticated = await verify_api_key(database, api_key)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error In Connecting With Database"
        )
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access - Valid API Key Required"
        )
