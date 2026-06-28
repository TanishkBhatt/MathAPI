from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List, Dict
from random import sample
from backend.models.components.helpers import Difficulty, QuestionType
from backend.utils.database import get_documents
from backend.utils.helpers import verify_api_key

def get_questions(
        database: MongoClient, 
        api_key: str|None, 
        topic_id: str, 
        limit: int, 
        difficulty: Difficulty|None, 
        question_type: QuestionType|None
    ) -> Dict[str, Any]:
    
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
        questions: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "questions",
            {"topic_id": topic_id}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    # VALIDATING IS TOPIC_ID VALID OR NOT
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic With ID - '{topic_id}' Not Found"
        )
    
    # FILTERING OUT DIFFICULTY
    f1 = [q for q in questions if q.get("difficulty") == difficulty.value] if difficulty else questions

    # FILTERING OUT QUESTION_TYPE
    f2 = [q for q in f1 if question_type.value in q.get("question_type", [])] if question_type else f1

    # APPLYING LIMITS
    f2 = sample(f2, min(limit, len(f2))) if f2 else []

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_questions": len(f2),
        "questions": f2
    }