import hashlib
import secrets
import time
from calendar import monthrange
from datetime import datetime
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

def generate_api_key(
        username: str,
        expiry: int | None
    ) -> str:
    user_hash: str = hashlib.sha256(username.encode()).hexdigest()[:12]
    api_key: str = f"mathapi_key_{user_hash}_{secrets.token_urlsafe(24)}_exp={expiry}"
    return api_key

# CALENDAR-ACCURATE "NOW + N MONTHS" EPOCH (HANDLES LEAP/SHORT MONTHS)
def compute_expiry(validity_months: int) -> int:
    now = datetime.now()
    month_index = now.month - 1 + validity_months
    year = now.year + month_index // 12
    month = month_index % 12 + 1
    day = min(now.day, monthrange(year, month)[1])
    expiry = now.replace(year=year, month=month, day=day)
    return int(expiry.timestamp())

# RETURNS THE STATE OF AN API KEY
async def get_api_key_state(
        db_conn: AsyncIOMotorClient,
        api_key: str
    ) -> str:
    db = db_conn["auth"]
    coll = db["users"]

    try:
        user = await coll.find_one({"api_key": api_key})
    except Exception:
        raise ConnectionError("Error In Connecting With Database")

    if user is None:
        return "invalid"

    expiry = user.get("expiry")
    if expiry is not None and time.time() > expiry:
        return "expired"

    return "valid"

async def verify_api_key(
        db_conn: AsyncIOMotorClient,
        api_key: str
    ) -> bool:
    return await get_api_key_state(db_conn, api_key) == "valid"

async def validate_api_key(database: AsyncIOMotorClient, api_key: str | None) -> None:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access - Valid API Key Required"
        )
    try:
        key_state = await get_api_key_state(database, api_key)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error In Connecting With Database"
        )
    if key_state == "expired":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key Expired, Create Another"
        )
    if key_state != "valid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access - Valid API Key Required"
        )