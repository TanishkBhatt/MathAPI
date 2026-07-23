from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any
from backend.config import settings

_client = AsyncIOMotorClient(settings.DB_CONNECTION_URL)

def get_db() -> AsyncIOMotorClient:
    return _client

async def get_documents(
        db_conn: AsyncIOMotorClient,
        db_name: str,
        coll_name: str,
        filter_query: dict[str, str] | None = None
    ) -> List[Dict[str, Any]]:

    client = db_conn
    db = client[db_name]
    coll = db[coll_name]

    query = filter_query or {}
    try:
        data: List[Dict[str, Any]] = await coll.find(query).to_list(length=None)
    except Exception as e:
        raise ConnectionError("Error In Connecting With Database")
    
    for doc in data:
        doc.pop("_id", None)
    
    return data


async def update_documents(
        db_conn: AsyncIOMotorClient,
        db_name: str,
        coll_name: str,
        filter_query: dict,
        update_data: dict
    ) -> None:

    client = db_conn
    db = client[db_name]
    coll = db[coll_name]

    try:
        await coll.update_many(filter_query, update_data)
    except Exception as e:
        raise ConnectionError("Error In Connecting With Database")

async def import_data(
        db_conn: AsyncIOMotorClient,
        db_name: str,
        coll_name: str,
        data: Dict[str, Any] | List[Dict[str, Any]],
        data_type: str = "Dict"
    ) -> None:

    client = db_conn
    db = client[db_name]
    coll = db[coll_name]

    try:
        if data_type == "List":
            await coll.insert_many(data)
        else:
            await coll.insert_one(data)
    except Exception as e:
        raise ConnectionError("Error In Connecting With Database")
