from pymongo import MongoClient
from fastapi import HTTPException, status
from typing import List, Dict, Any
from backend.utils.config import settings

_client = MongoClient(settings.DB_CONNECTION_URL)

def get_db() -> MongoClient:
    try:
        return _client
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error In Connecting With Database"
        )

def get_documents(
        db_conn: MongoClient, 
        db_name: str, 
        coll_name: str, 
        filter_query: dict[str, str] | None = None
    ) -> List[Dict[str, Any]]:
    client = db_conn
    db = client[db_name]
    coll = db[coll_name]

    query = filter_query or {}
    try:
        data: List[Dict[str, Any]] = list(coll.find(query))
    except Exception as e:
        raise ConnectionError("Error In Connecting With Database")

    for doc in data:
        doc.pop("_id", None)

    return data

def import_data(
        db_conn: MongoClient, 
        db_name: str, 
        coll_name: str, 
        data: Dict[str, Any]
    ) -> None:
    client = db_conn
    db = client[db_name]
    coll = db[coll_name]

    try:
        coll.insert_one(data)
    except Exception as e:
        raise ConnectionError("Error In Connecting With Database")