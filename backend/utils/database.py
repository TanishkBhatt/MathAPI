from pymongo import MongoClient
from backend.utils.config import settings

_client = MongoClient(settings.DB_CONNECTION_URL)

def get_db() -> MongoClient:
    return _client