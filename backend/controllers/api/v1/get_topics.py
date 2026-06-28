from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from backend.utils.database import get_documents
from backend.utils.helpers import verify_api_key

def get_topics(
        database: MongoClient, 
        api_key: str|None
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
    
    # RETRIEVING ALL TOPICS
    try:
        topics: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "topics"
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    # RETRIEVING ALL TOPICS METADATA - QUESTIONS AVAILABLE AND LEARNING SOURCES AVAILABLE
    for topic in topics:
        topic_id = topic["topic_id"]
        
        try:
            explain_data = get_documents(
                database,
                "datasets",
                "explain",
                {"topic_id": topic_id}
            )

            examples_data = get_documents(
                database,
                "datasets",
                "examples",
                {"topic_id": topic_id}
            )

            questions_data = get_documents(
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

        topic["learning_sources_available"] = len(explain_data[0].get("learning_sources", [])) if explain_data else 0
        topic["examples_available"] = len(examples_data)
        topic["questions_available"] = len(questions_data)
    
    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_topics": len(topics),
        "topics": topics
    }