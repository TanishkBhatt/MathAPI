from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, List, Dict
from backend.utils.database import get_documents
from backend.utils.helpers import verify_api_key

def get_formulae(
        database: MongoClient, 
        api_key: str|None, 
        topic_id: str
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
        formulae_data: List[Dict[str, Any]] = get_documents(
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