from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List, Dict
from random import sample
from backend.models.objects.helpers import Difficulty
from backend.utils.database import get_documents

def get_questions(database: MongoClient, topic_id: str, limit: int, difficulty: Difficulty|None) -> dict[str, Any]:
    # RETRIEVING DATA
    try:
        questions: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "questions",
            {"topic_id": topic_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )
    
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id - {topic_id} not found."
        )
    
    # FILTERING OUT DIFFICULTY
    if difficulty:
        filtered_questions = []
        for question in questions:
            if question["difficulty"] == difficulty.value:
                filtered_questions.append(question)
    else:
        filtered_questions = questions
    
    # APPLYING LIMITS
    filtered_questions = sample(filtered_questions, min(limit, len(filtered_questions)))

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_questions": len(filtered_questions),
        "questions": filtered_questions
    }