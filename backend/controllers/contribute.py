from fastapi import HTTPException, status
from pymongo import MongoClient
from typing import Any, Dict, List
from backend.models.contribute import ContributionType, ExampleContributionSchema, QuestionContributionSchema
from backend.utils.config import settings
from backend.utils.database import import_data

def contribution(database: MongoClient, admin_token: str, contribution_type: ContributionType, request_data: ExampleContributionSchema | QuestionContributionSchema) -> Dict[str, Any]:
    # VALIDATING ADMIN_TOKEN
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access"
        )
    
    # IMPORT DATA TO DATABASE
    try:
        data: Dict[str, Any] = request_data.model_dump()
        data["difficulty"] = data["difficulty"].value

        for i in range(len(data["question_type"])):
            data["question_type"][i] = data["question_type"][i].value

        if contribution_type.value == "Question":
            data["answer"] = data["answer"].value

        import_data(
            database,
            "datasets",
            contribution_type.value.lower(),
            data
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": f"{contribution_type.value} Contribution Successful"
    }