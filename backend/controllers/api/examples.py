from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any

def get_examples(database: MongoClient, topic_id: str, limit: int) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "examples": []
    }