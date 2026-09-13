from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from typing import Any, Dict, List
from datetime import datetime
from utils.database import update_documents, get_documents
from utils.helpers import validate_api_key

DB_ERROR = "Error In Connecting With Database"

async def get_daily_challenge(database: AsyncIOMotorClient, api_key: str | None) -> Dict[str, Any]:
    await validate_api_key(database, api_key)
    today = datetime.now().strftime("%Y-%m-%d")

    client = database
    db = client["datasets"]
    coll = db["questions"]

    # CHECK IF TODAY'S CHALLENGE EXISTS - MUST HAVE 1 OF EACH DIFFICULTY
    try:
        cursor = coll.find({"challenge_date": today}).sort("_id", 1).limit(3)
        existing: List[Dict[str, Any]] = await cursor.to_list(None)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=DB_ERROR
        )

    # Verify existing challenge has 1 of each difficulty
    difficulties_in_existing = {doc.get("difficulty") for doc in existing}
    required_difficulties = {"Beginner", "Intermediate", "Advanced"}
    
    if len(existing) >= 3 and required_difficulties.issubset(difficulties_in_existing):
        for doc in existing:
            doc.pop("_id", None)
        return {
            "success": True,
            "message": "Daily Challenge Data Successfully Retrieved",
            "challenge_date": today,
            "total_questions": len(existing),
            "questions": existing
        }

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

    return {
        "success": True,
        "message": "Daily Challenge Data Successfully Retrieved",
        "challenge_date": today,
        "total_questions": len(selected),
        "questions": selected
    }