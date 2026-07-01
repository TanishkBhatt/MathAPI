from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, Dict, List
from backend.models.contribute.example import ExampleContributionSchema
from backend.utils.config import settings
from backend.utils.database import get_documents, import_data

def example_contribution(
        database: MongoClient, 
        admin_token: str, 
        request_data: ExampleContributionSchema     # type: ignore
    ) -> Dict[str, Any]:

    # VALIDATING ADMIN_TOKEN
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access"
        )
    
    # VALIDATING IS THE TOPIC_ID VALID
    try:
        topic: List[Dict[str, Any]] = get_documents(
            database,
            "datasets",
            "topics",
            {"topic_id": request_data.topic_id}
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic With ID - '{request_data.topic_id}' Not Found"
        )
    
    # IMPORT DATA TO DATABASE
    try:
        request_data: Dict[str, Any] = request_data.model_dump()
        request_data["difficulty"] = request_data["difficulty"].value

        for i in range(len(request_data["question_type"])):
            request_data["question_type"][i] = request_data["question_type"][i].value

        import_data(
            database,
            "datasets",
            "examples",
            request_data
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Example Contribution Successful"
    }