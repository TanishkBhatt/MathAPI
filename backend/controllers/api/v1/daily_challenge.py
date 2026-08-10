from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from typing import Any, Dict, List
from datetime import datetime
from backend.utils.database import ensure_index
from backend.utils.helpers import validate_api_key

async def get_daily_challenge(
        database: AsyncIOMotorClient,
        api_key: str | None
    ) -> Dict[str, Any]:

    await validate_api_key(database, api_key)
    today = datetime.now().strftime("%Y-%m-%d")

    db = database["datasets"]
    challenges_coll = db["daily_challenges"]

    # ONE document per day -> same set for every user, no unbounded arrays
    try:
        await ensure_index(
            database,
            "datasets",
            "daily_challenges",
            [("challenge_date", 1)],
            unique=True,
            index_name="challenge_date_unique"
        )
    except Exception:
        # index creation is best-effort; the DuplicateKeyError path below
        # still protects the race even if the index does not exist yet
        pass

    try:
        existing = await challenges_coll.find_one({"challenge_date": today})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    if existing:
        questions: List[Dict[str, Any]] = existing.get("questions", [])
        return {
            "success": True,
            "message": "Daily Challenge Data Successfully Retrieved",
            "challenge_date": today,
            "total_questions": len(questions),
            "questions": questions
        }

    # PICK 1 BEGINNER + 1 INTERMEDIATE + 1 ADVANCED
    questions_coll = db["questions"]

    selected: List[Dict[str, Any]] = []
    difficulties: List[str] = ["Beginner", "Intermediate", "Advanced"]

    try:
        for diff in difficulties:
            cursor = questions_coll.aggregate([
                {"$match": {"difficulty": diff}},
                {"$sample": {"size": 1}}
            ])
            docs: List[Dict[str, Any]] = await cursor.to_list(None)
            if docs:
                docs[0].pop("_id", None)
                selected.append(docs[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # RACE-SAFE UPSERT: if another request created today's set first, adopt it
    try:
        doc = await challenges_coll.find_one_and_update(
            {"challenge_date": today},
            {"$setOnInsert": {"challenge_date": today, "questions": selected}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
    except DuplicateKeyError:
        try:
            doc = await challenges_coll.find_one({"challenge_date": today})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    if doc is None:
        doc = {"challenge_date": today, "questions": selected}

    questions = doc.get("questions", [])
    return {
        "success": True,
        "message": "Daily Challenge Data Successfully Retrieved",
        "challenge_date": today,
        "total_questions": len(questions),
        "questions": questions
    }