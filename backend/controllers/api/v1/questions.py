from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List, Dict
from random import sample
from backend.models.components.helpers import Difficulty, QuestionType
from backend.utils.database import get_documents
from backend.utils.config import settings

def get_questions(auth_token: str|None, database: MongoClient, topic_id: str, limit: int, difficulty: Difficulty|None, question_type: QuestionType|None) -> Dict[str, Any]:
    # VERIFIYING AUTH TOKEN
    authenticate = False
    if auth_token == settings.AUTH_TOKEN:
        authenticate = True

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
    
    if authenticate:
        # FILTERING OUT DIFFICULTY
        f1_questions = [q for q in questions if q.get("difficulty") == difficulty.value] if difficulty else questions

        # FILTERING OUT QUESTION_TYPE
        f2_questions = [q for q in f1_questions if question_type.value in q.get("question_type", [])] if question_type else f1_questions
    
        # APPLYING LIMITS
        f2_questions = sample(f2_questions, min(limit, len(f2_questions))) if f2_questions else []
        
    else:
        f2_questions = sample(questions[:10], min(10, len(questions))) if questions[:10] else []

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_questions": len(f2_questions),
        "questions": f2_questions
    }