from pydantic import BaseModel
from backend.models.components.main import Question

class QuestionContributionSchema(Question):
    pass

class ContributionResponse(BaseModel):
    success: bool
    message: str