from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import List, Dict, Any
from backend.utils.database import get_documents
from backend.utils.helpers import validate_api_key

def get_topics(
        database: MongoClient,
        api_key: str | None,
        skip: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
    
    validate_api_key(database, api_key)
    
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
    
    total_topics = len(topics)
    
    # RETRIEVING ALL TOPICS METADATA
    for topic in topics:
        topic_id = topic["topic_id"]
        
        try:
            formulae_data = get_documents(
                database,
                "datasets",
                "formulae",
                {"topic_id": topic_id}
            )

            sources_data = get_documents(
                database,
                "datasets",
                "sources",
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

        topic["learning_sources_available"] = len(sources_data[0].get("learning_sources", [])) if sources_data else 0
        topic["formulae_available"] = len(formulae_data[0].get("formulae", [])) if formulae_data else 0
        topic["examples_available"] = len(examples_data)
        topic["questions_available"] = len(questions_data)
    
    # APPLY PAGINATION
    paginated_topics = topics[skip:skip + limit]
    
    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_topics": total_topics,
        "page": skip // limit + 1,
        "per_page": limit,
        "topics": paginated_topics
    }