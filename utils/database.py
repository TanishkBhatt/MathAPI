from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from typing import List, Dict, Any
from config import settings

_client = AsyncIOMotorClient(settings.DB_CONNECTION_URL)

# INDEXES THAT HAVE ALREADY BEEN CREATED IN THIS PROCESS
_ensured_indexes: set = set()

def get_db() -> AsyncIOMotorClient:
    return _client

async def ensure_index(
        db_conn: AsyncIOMotorClient,
        db_name: str,
        coll_name: str,
        index_spec: List[tuple],
        unique: bool = False,
        index_name: str | None = None
    ) -> None:

    key = (db_name, coll_name, tuple(index_spec), unique)
    if key in _ensured_indexes:
        return

    db = db_conn[db_name]
    coll = db[coll_name]
    await coll.create_index(index_spec, unique=unique, name=index_name)
    # create_index is idempotent, but definitive only once we succeeded
    _ensured_indexes.add(key)

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
    except DuplicateKeyError:
        raise
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
    except DuplicateKeyError:
        raise
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

    if data_type == "List" and not data:
        return

    try:
        if data_type == "List":
            await coll.insert_many(data)
        else:
            await coll.insert_one(data)
    except DuplicateKeyError:
        raise
    except Exception as e:
        raise ConnectionError("Error In Connecting With Database")