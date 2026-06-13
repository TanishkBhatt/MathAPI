from fastapi import HTTPException
from pydantic import ValidationError
from pymongo import MongoClient
from typing import Any
from backend.models.objects.helpers import Difficulty

def get_questions(db: MongoClient, topic_name: str, limit: int, difficulty: Difficulty | None) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "questions": {}
    }