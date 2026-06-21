from pymongo import MongoClient
from typing import List, Dict, Any
from backend.utils.config import settings

_client = MongoClient(settings.DB_CONNECTION_URL)

def get_db() -> MongoClient:
    return _client

def get_documents(db_conn: MongoClient, db_name: str, coll_name: str, filter_query: dict[str, str] | None = None) -> List[Dict[str, Any]]:
    client = db_conn
    db = client[db_name]
    coll = db[coll_name]

    query = filter_query or {}
    data: List[Dict[str, Any]] = list(coll.find(query))

    for doc in data:
        doc.pop("_id", None)

    return data