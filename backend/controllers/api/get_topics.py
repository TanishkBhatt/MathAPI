from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from backend.utils.database import get_documents

def get_topics(db: MongoClient) -> Dict[str, Any]:
    # RETRIEVING ALL TOPICS
    try:
        topics: List[Dict[str, Any]] = get_documents(
            db,
            "datasets",
            "topics"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error - {str(e)}"
        )
    
    # RETRIEVING ALL TOPICS META DATA - QUESTIONS AVAILABLE AND LEARNING SOURCES AVAILABLE
    for topic in topics:
        topic_id = topic["topic_id"]
        
        try:
            explain_data = get_documents(
                db,
                "datasets",
                "explain",
                {"topic_id": topic_id}
            )

            questions_data = get_documents(
                db,
                "datasets",
                "questions",
                {"topic_id": topic_id}
            ) 
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database connection error - {str(e)}"
            )

        topic["learning_sources_available"] = len(explain_data[0]["learning_sources"])
        topic["questions_available"] = len(questions_data)
    
    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "topics": topics
    }