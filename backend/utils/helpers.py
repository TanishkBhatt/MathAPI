import hashlib
import secrets
import time
from pymongo import MongoClient

def generate_api_key(username: str, expiry: int | None) -> str:
    """GENERATING AKI_KEY FOR AUTH ACCESS"""
    user_hash: str = hashlib.sha256(username.encode()).hexdigest()[:12]
    api_key: str = f"mathapi_key_{user_hash}_{secrets.token_urlsafe(24)}_exp={expiry}"
    return api_key

def verify_api_key(db_conn: MongoClient, api_key: str) -> bool:
    """VERIFING API_KEY EXISTANCE"""
    db = db_conn["auth"]
    coll = db["users"]

    try:
        user = coll.find_one({"api_key": api_key})
    except Exception:
        raise ConnectionError("Error In Connecting With Database")

    if user is None:
        return False

    expiry = user.get("expiry")
    if expiry is not None and time.time() > expiry:
        return False

    return True