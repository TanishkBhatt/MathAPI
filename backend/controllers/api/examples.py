from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List, Dict
from random import sample
from backend.utils.database import get_documents

def get_examples(database: MongoClient, topic_id: str, limit: int) -> dict[str, Any]:
    # RETRIEVING DATA
    try:
        examples: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "examples",
            {"topic_id": topic_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )
    
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not examples:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id - {topic_id} not found."
        )
    
    # APPLYING LIMITS
    examples = sample(examples, min(limit, len(examples)))
    
    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_examples": len(examples),
        "examples": examples
    }