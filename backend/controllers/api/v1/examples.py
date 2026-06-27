from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List, Dict
from random import sample
from backend.utils.database import get_documents
from backend.utils.helpers import verify_api_key

def get_examples(database: MongoClient, api_key: str|None, topic_id: str, limit: int) -> Dict[str, Any]:
    # VERIFIYING API KEY
    authenticate: bool = False
    if api_key:
        try:
            authenticate = verify_api_key(
                database,
                api_key
            )
        except Exception:
            pass
    
    if not authenticate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access"
        )
    
    # RETRIEVING DATA
    try:
        examples: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "examples",
            {"topic_id": topic_id}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not examples:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic With ID - '{topic_id}' Not Found"
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