from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from random import sample
from backend.utils.database import get_documents

def explain_topic(database: MongoClient, topic_id: str, include_examples: bool, include_questions: bool) -> Dict[str, Any]:
    # RETRIVEING EXPLINATION WITH FILTER
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
    
    explination = explinations[0]
    
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not explination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id - {topic_id} not found."
        )
    
    # ADDING EXAMPLES
    if include_examples:
        try:
            examples: List[Dict[str, Any]] = get_documents(
                database,
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
            explination["try_yourself_questions"] = sample(questions, 3)
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