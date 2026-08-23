from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, List, Dict
from utils.database import get_documents
from utils.helpers import validate_api_key

async def get_sources(
        database: AsyncIOMotorClient,
        api_key: str | None,
        topic_id: str
    ) -> Dict[str, Any]:
    
    await validate_api_key(database, api_key)
    
    # RETRIEVING DATA
    try:
        sources_data: List[Dict[str, Any]] = await get_documents(
            database,
            "datasets",
            "sources",
            {"topic_id": topic_id}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # VALIDATING IS TOPIC_ID VALID OR NOT
    sources: List[Dict[str, Any]] = sources_data[0]["learning_sources"] if sources_data else []
    if not sources:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic With ID - '{topic_id}' Not Found"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_sources": len(sources),
        "sources": sources
    }