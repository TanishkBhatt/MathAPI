from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, List, Dict
from random import sample
from models.components.helpers import Difficulty, QuestionType
from utils.database import get_documents
from utils.helpers import validate_api_key

async def get_questions(
        database: AsyncIOMotorClient,
        api_key: str | None,
        topic_id: str, 
        limit: int, 
        difficulty: Difficulty|None, 
        question_type: QuestionType|None
    ) -> Dict[str, Any]:
    
    await validate_api_key(database, api_key)
    
    # RETRIEVING DATA
    try:
        questions: List[Dict[str, Any]] = await get_documents(
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
    by_difficulty = [q for q in questions if q.get("difficulty") == difficulty.value] if difficulty else questions

    # FILTERING OUT QUESTION_TYPE
    by_type = [q for q in by_difficulty if question_type.value in q.get("question_type", [])] if question_type else by_difficulty

    # APPLYING LIMITS
    selected = sample(by_type, min(limit, len(by_type))) if by_type else []

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_questions": len(selected),
        "questions": selected
    }