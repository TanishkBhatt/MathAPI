from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError, PyMongoError
from typing import Any, Dict, List
from datetime import datetime, timezone
from utils.database import ensure_index
from utils.helpers import validate_api_key

DB_ERROR = "Error In Connecting With Database"
DIFFICULTIES = ("Beginner", "Intermediate", "Advanced")


async def _pick_question_ids(database: AsyncIOMotorClient) -> List[Any]:
    questions = database["datasets"]["questions"]
    ids: List[Any] = []

    for difficulty in DIFFICULTIES:
        cursor = questions.aggregate([
            {"$match": {"difficulty": difficulty}},
            {"$sample": {"size": 1}},
            {"$project": {"_id": 1}}
        ])
        docs: List[Dict[str, Any]] = await cursor.to_list(None)
        if docs:
            ids.append(docs[0]["_id"])

    return ids


async def _get_or_create_challenge(database: AsyncIOMotorClient, today: str) -> Dict[str, Any] | None:
    challenges = database["datasets"]["daily_challenges"]

    challenge = await challenges.find_one({"challenge_date": today})
    if challenge and challenge.get("question_ids"):
        return challenge

    ids = await _pick_question_ids(database)
    if not ids:
        return None

    if challenge is None:
        try:
            return await challenges.find_one_and_update(
                {"challenge_date": today},
                {
                    "$setOnInsert": {
                        "challenge_date": today,
                        "question_ids": ids,
                        "created_at": datetime.now(timezone.utc)
                    }
                },
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
        except DuplicateKeyError:
            return await challenges.find_one({"challenge_date": today})

    return await challenges.find_one_and_update(
        {"_id": challenge["_id"]},
        {
            "$set": {
                "question_ids": ids,
                "created_at": datetime.now(timezone.utc)
            }
        },
        return_document=ReturnDocument.AFTER
    )


async def _load_questions(database: AsyncIOMotorClient, question_ids: List[Any]) -> List[Dict[str, Any]]:
    questions = database["datasets"]["questions"]
    docs: List[Dict[str, Any]] = await questions.find({"_id": {"$in": question_ids}}).to_list(None)
    by_id = {doc["_id"]: doc for doc in docs}
    selected: List[Dict[str, Any]] = []

    for question_id in question_ids:
        doc = by_id.get(question_id)
        if doc is None:
            continue
        doc.pop("_id", None)
        doc.pop("challenge_date", None)
        selected.append(doc)

    return selected


async def get_daily_challenge(database: AsyncIOMotorClient, api_key: str | None) -> Dict[str, Any]:
    await validate_api_key(database, api_key)
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        await ensure_index(
            database,
            "datasets",
            "daily_challenges",
            [("challenge_date", 1)],
            unique=True,
            index_name="challenge_date_unique"
        )
        challenge = await _get_or_create_challenge(database, today)
        questions = await _load_questions(database, challenge.get("question_ids", []) if challenge else [])
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=DB_ERROR
        )

    return {
        "success": True,
        "message": "Daily Challenge Data Successfully Retrieved",
        "challenge_date": today,
        "total_questions": len(questions),
        "questions": questions
    }
