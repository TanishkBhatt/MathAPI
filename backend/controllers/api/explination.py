from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from random import sample
from backend.utils.database import get_documents

def explain_topic(db: MongoClient, topic_id: str) -> Dict[str, Any]:
    # RETRIVEING EXPLINATION WITH FILTER
    try:
        explinations: List[Dict[str, Any]] = get_documents(
            db,
            "datasets",
            "explain",
            {"topic_id": topic_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )
    
    explination = explinations[0]
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not explination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id - {topic_id} not found."
        )
    
    # ADDING EXAMPLES
    try:
        examples: List[Dict[str, Any]] = get_documents(
            db,
            "datasets",
            "examples",
            {"topic_id": topic_id}
        )
        explination["examples"] = sample(examples, 2)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )
    
    # ADDING TRY_YOURSELF_QUESTIONS
    try:
        questions: List[Dict[str, Any]] = get_documents(
            db,
            "datasets",
            "questions",
            {"topic_id": topic_id}
        )
        explination["try_yourself_questions"] = sample(questions, 3)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "explination": explination
    }