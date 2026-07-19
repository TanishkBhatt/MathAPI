from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any
from random import sample
from backend.utils.database import get_documents
from backend.utils.helpers import validate_api_key

async def explain_topic(
        database: AsyncIOMotorClient,
        api_key: str | None,
        topic_id: str, 
        include_formulae: bool, 
        include_examples: bool, 
        include_questions: bool,
        include_sources: bool
    ) -> Dict[str, Any]:
    
    await validate_api_key(database, api_key)
    
    # RETRIVEING DATA
    try:
        explanations: List[Dict[str, Any]] = await get_documents(
            database,
            "datasets",
            "explain",
            {"topic_id": topic_id}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # VALIDATING IS THE TOPIC_ID VALID
    if not explanations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic With ID - '{topic_id}' Not Found"
        )

    explanation = explanations[0]

    # FORMULAE, EXAMPLES, QUESTIONS LEARNING SOURCES INCLUSION
    if include_formulae:
        try:
            formulae: List[Dict[str, Any]] = await get_documents(
                database,
                "datasets",
                "formulae",
                {"topic_id": topic_id}
            )
            explanation["formulae"] = formulae[0]["formulae"] if formulae else []
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    else:
        explanation["formulae"] = []

    if include_examples:
        try:
            examples: List[Dict[str, Any]] = await get_documents(
                database,
                "datasets",
                "examples",
                {"topic_id": topic_id}
            )
            explanation["solved_examples"] = examples[:2] if examples else []
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    else:
        explanation["solved_examples"] = []

    if include_questions:
        try:
            questions: List[Dict[str, Any]] = await get_documents(
                database,
                "datasets",
                "questions",
                {
                    "topic_id": topic_id,
                    "difficulty": "Beginner"
                }
            )
            explanation["try_yourself_questions"] = sample(questions, min(3, len(questions))) if questions else []
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    else:
        explanation["try_yourself_questions"] = []

    if include_sources:
        try:
            source_data: List[Dict[str, Any]] = await get_documents(
                database,
                "datasets",
                "sources",
                {"topic_id": topic_id}
            )
            explanation["learning_sources"] = source_data[0]["learning_sources"] if source_data else []
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )
    else:
        explanation["learning_sources"] = []

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "explanation": explanation
    }
