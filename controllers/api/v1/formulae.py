from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, List, Dict
from utils.database import get_documents
from utils.helpers import validate_api_key

async def get_formulae(
        database: AsyncIOMotorClient,
        api_key: str | None,
        topic_id: str
    ) -> Dict[str, Any]:
    
    await validate_api_key(database, api_key)
    
    # RETRIEVING DATA
    try:
        formulae_data: List[Dict[str, Any]] = await get_documents(
            database,
            "datasets",
            "formulae",
            {"topic_id": topic_id}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # VALIDATING IS TOPIC_ID VALID OR NOT
    formulae: List[Dict[str, Any]] = formulae_data[0]["formulae"] if formulae_data else []
    if not formulae:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic With ID - '{topic_id}' Not Found"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_formulae": len(formulae),
        "formulae": formulae
    }