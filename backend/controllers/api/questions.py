from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List
from backend.models.objects.helpers import Difficulty

def get_questions(database: MongoClient, topic_id: str, limit: int, difficulty: List[Difficulty] | None) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "questions": []
    }