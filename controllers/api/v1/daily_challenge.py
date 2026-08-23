from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from typing import Any, Dict, List
from random import sample
from datetime import datetime
from utils.database import update_documents
from utils.helpers import validate_api_key

DB_ERROR = "Error In Connecting With Database"

def _challenge_payload(
        today: str,
        selected: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
    return {
        "success": True,
        "message": "Daily Challenge Data Successfully Retrieved",
        "challenge_date": today,
        "total_questions": len(selected),
        "questions": selected
    }

async def get_daily_challenge(
        database: AsyncIOMotorClient,
        api_key: str | None
    ) -> Dict[str, Any]:

    await validate_api_key(database, api_key)
    today = datetime.now().strftime("%Y-%m-%d")

    client = database
    db = client["datasets"]
    coll = db["questions"]

    # CHECK IF TODAY'S CHALLENGE EXISTS - SORTED BY _id SO EVERY USER GETS THE SAME SET
    try:
        cursor = coll.find({"challenge_date": today}).sort("_id", 1).limit(3)
        existing: List[Dict[str, Any]] = await cursor.to_list(None)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=DB_ERROR
        )

    if len(existing) >= 3:
        for doc in existing:
            doc.pop("_id", None)
        return _challenge_payload(today, existing)

    existing_ids: List[Any] = [doc["_id"] for doc in existing]

    # PICK 1 BEGINNER + 1 INTERMEDIATE + 1 ADVANCED (EXCLUDING ALREADY-TAGGED ONES)
    selected: List[Dict[str, Any]] = []
    ids: List[Any] = []
    difficulties = ["Beginner", "Intermediate", "Advanced"]

    try:
        for diff in difficulties:
            cursor = coll.aggregate([
                {
                    "$match": {
                        "difficulty": diff,
                        "_id": {"$nin": existing_ids}
                    }
                },
                {"$sample": {"size": 1}}
            ])
            docs: List[Dict[str, Any]] = await cursor.to_list(None)
            if docs:
                ids.append(docs[0]["_id"])
                docs[0].pop("_id", None)
                selected.append(docs[0])
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=DB_ERROR
        )

    if ids:
        try:
            await update_documents(
                database,
                "datasets",
                "questions",
                {"_id": {"$in": ids}},
                {"$addToSet": {"challenge_date": today}}
            )
        except ConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=DB_ERROR
            )

    return _challenge_payload(today, selected)
