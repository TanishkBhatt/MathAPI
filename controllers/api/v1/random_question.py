from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, Dict, List
from utils.database import get_documents
from utils.helpers import validate_api_key

async def get_random_question(
        database: AsyncIOMotorClient,
        api_key: str | None
    ) -> Dict[str, Any]:

    await validate_api_key(database, api_key)

    client = database
    db = client["datasets"]
    coll = db["questions"]

    try:
        cursor = coll.aggregate([{"$sample": {"size": 1}}])
        docs: List[Dict[str, Any]] = await cursor.to_list(None)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error In Connecting With Database"
        )

    if not docs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Questions Available"
        )

    docs[0].pop("_id", None)

    return {
        "success": True,
        "message": "Random Question Successfully Retrieved",
        "question": docs[0]
    }