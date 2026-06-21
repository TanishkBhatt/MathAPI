from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from random import sample
from backend.utils.database import get_documents

def explain_topic(database: MongoClient, topic_id: str, include_examples: bool, include_questions: bool) -> Dict[str, Any]:
    # RETRIVEING EXPLINATION
    try:
        explinations: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "explain",
            {"topic_id": topic_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )
    
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not explinations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id - {topic_id} not found."
        )
    
    explination = explinations[0]
    
    # ADDING EXAMPLES
    if include_examples:
        try:
            examples: List[Dict[str, Any]] = get_documents(
                database,
                "datasets",
                "examples",
                {"topic_id": topic_id}
            )
            explination["examples"] = examples[:2] if examples else []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database connection error - {str(e)}"
            )
    else:
        explination["examples"] = []
    
    # ADDING TRY_YOURSELF_QUESTIONS
    if include_questions:
        try:
            questions: List[Dict[str, Any]] = get_documents(
                database,
                "datasets",
                "questions",
                {"topic_id": topic_id}
            )
            explination["try_yourself_questions"] = sample(questions[:10], 3) if questions else []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database connection error - {str(e)}"
            )
    else:
        explination["try_yourself_questions"] = []

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "explination": explination
    }