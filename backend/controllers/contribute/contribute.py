from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, Dict, List
from backend.models.contribute.contribute import ContributionType, QuestionContributionSchema, ExampleContributionSchema
from backend.config import settings
from backend.utils.database import get_documents, import_data

async def contribution(
        database: AsyncIOMotorClient, 
        admin_token: str, 
        contribution_type: ContributionType,
        request_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

    # VALIDATING ADMIN_TOKEN
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access - Valid ADMIN_TOKEN Required"
        )

    # VALIDATING THE CONTRIBUTION DATA IS NOT EMPTY
    if not request_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Empty Contribution Data - Provide At Least One Item To Contribute"
        )
    
    # VALIDATING THE CONTRIBUTION DATA AND THE TOPIC_ID
    for item in request_data:
        if "topic_id" not in item:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Missing Required Field - 'topic_id' is required in each contribution data"
            )

        # VALIDATING THE CONTRIBUTION DATA (before the topic lookup, so an
        # invalid payload returns 422 rather than a misleading 404)
        if contribution_type.value == "Question":
            try:
                QuestionContributionSchema(**item)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid Question Contribution Data Schema"
                )

        if contribution_type.value == "Example":
            try:
                ExampleContributionSchema(**item)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid Example Contribution Data Schema"
                )

        # VALIDATING IS THE TOPIC_ID VALID
        try:
            topic: List[Dict[str, Any]] = await get_documents(
                database,
                "datasets",
                "topics",
                {"topic_id": item.get("topic_id", "Unknown")}
            )
        except ConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{str(e)}"
            )

        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic With ID - '{item.get('topic_id', 'Unknown')}' Not Found"
            )
    
    # IMPORT DATA TO DATABASE
    try:
        await import_data(
            database,
            "datasets",
            f"{contribution_type.value.lower()}s",
            request_data,
            data_type="List"
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # RETURN OBJECT
    return {
        "success": True,
        "message": f"{contribution_type.value}s Contribution Successful"
    }