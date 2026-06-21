from fastapi import HTTPException, status, Request
from pymongo import MongoClient
from typing import Any, List, Dict
from random import sample
from backend.utils.database import get_documents
from backend.utils.config import settings

def get_examples(request: Request, database: MongoClient, topic_id: str, limit: int) -> Dict[str, Any]:
    # VERIFIYING HEADERS
    auth_token: str = request.headers.get("auth_token", "")

    if auth_token == settings.AUTH_TOKEN:
        authenticate = True
    else:
        authenticate = False

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
    if authenticate:
        examples = sample(examples, min(limit, len(examples)))
    else:
        examples = sample(examples[:2], 2)
    
    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_examples": len(examples),
        "examples": examples
    }