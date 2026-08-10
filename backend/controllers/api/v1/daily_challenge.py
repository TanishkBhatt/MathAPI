from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, Dict, List
from random import sample
from datetime import datetime
from backend.utils.database import get_documents, update_documents
from backend.utils.helpers import validate_api_key

async def get_daily_challenge(
        database: AsyncIOMotorClient,
        api_key: str | None
    ) -> Dict[str, Any]:

    await validate_api_key(database, api_key)
    today = datetime.now().strftime("%Y-%m-%d")

    # CHECK IF TODAY'S CHALLENGE EXISTS
    try:
        existing: List[Dict[str, Any]] = await get_documents(
            database,
            "datasets",
            "questions",
            {"challenge_date": today}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    if len(existing) >= 3:
        selected = sample(existing, 3)
        return {
            "success": True,
            "message": "Daily Challenge Data Successfully Retrieved",
            "challenge_date": today,
            "total_questions": len(selected),
            "questions": selected
        }

    # PICK 1 BEGINNER + 1 INTERMEDIATE + 1 ADVANCED
    client = database
    db = client["datasets"]
    coll = db["questions"]

    selected = []
    ids = []
    difficulties = ["Beginner", "Intermediate", "Advanced"]

    try:
        for diff in difficulties:
            cursor = coll.aggregate([
                {"$match": {"difficulty": diff}},
                {"$sample": {"size": 1}}
            ])
            docs: List[Dict[str, Any]] = await cursor.to_list(None)
            if docs:
                ids.append(docs[0]["_id"])
                docs[0].pop("_id", None)
                selected.append(docs[0])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error In Connecting With Database"
        )

    if ids:
        try:
            await update_documents(
                database,
                "datasets",
                "questions",
                {"_id": {"$in": ids}},
                {"$push": {"challenge_date": today}}
            )
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )

    return {
        "success": True,
        "message": "Daily Challenge Data Successfully Retrieved",
        "challenge_date": today,
        "total_questions": len(selected),
        "questions": selected
    }
