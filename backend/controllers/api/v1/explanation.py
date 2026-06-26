from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from random import sample
from backend.utils.database import get_documents

def explain_topic(database: MongoClient, topic_id: str, include_examples: bool, include_questions: bool) -> Dict[str, Any]:
    try:
        explanations: List[Dict[str, Any]] = get_documents(
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

    if not explanations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id - {topic_id} not found."
        )

    explanation = explanations[0]

    if include_examples:
        try:
            examples: List[Dict[str, Any]] = get_documents(
                database,
                "datasets",
                "examples",
                {"topic_id": topic_id}
            )
            explanation["examples"] = examples[:2] if examples else []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database connection error - {str(e)}"
            )
    else:
        explanation["examples"] = []

    if include_questions:
        try:
            questions: List[Dict[str, Any]] = get_documents(
                database,
                "datasets",
                "questions",
                {"topic_id": topic_id}
            )
            explanation["try_yourself_questions"] = sample(questions[:10], 3) if questions else []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database connection error - {str(e)}"
            )
    else:
        explanation["try_yourself_questions"] = []

    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "explanation": explanation
    }
