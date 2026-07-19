from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from asyncio import gather
from typing import List, Dict, Any
from backend.utils.database import get_documents
from backend.utils.helpers import validate_api_key

async def get_topics(
        database: AsyncIOMotorClient,
        api_key: str | None
    ) -> Dict[str, Any]:
    
    await validate_api_key(database, api_key)
    
    # RETRIEVING ALL TOPICS
    try:
        topics: List[Dict[str, Any]] = await get_documents(
            database,
            "datasets",
            "topics"
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    # RETRIEVING ALL TOPICS METADATA
    for topic in topics:
        topic_id = topic["topic_id"]
        
        try:
            formulae_data, sources_data, examples_data, questions_data = await gather(
                get_documents(database, "datasets", "formulae", {"topic_id": topic_id}),
                get_documents(database, "datasets", "sources", {"topic_id": topic_id}),
                get_documents(database, "datasets", "examples", {"topic_id": topic_id}),
                get_documents(database, "datasets", "questions", {"topic_id": topic_id})
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

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_topics": len(topics),
        "topics": topics
    }