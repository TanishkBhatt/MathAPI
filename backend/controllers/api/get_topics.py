from fastapi import HTTPException
from pydantic import ValidationError
from pymongo import MongoClient
from typing import Any

def get_topics(db: MongoClient) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "topics": {}
    }