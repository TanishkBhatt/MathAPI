from fastapi import HTTPException
from pydantic import ValidationError
from pymongo import MongoClient
from typing import Any

def explain_topic(db: MongoClient, topic_name: str) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "explination": {}
    }