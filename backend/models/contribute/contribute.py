from pydantic import BaseModel
from enum import Enum
from backend.models.components.main import Question, Example

class ContributionType(Enum):
    question = "Question"
    example = "Example"

class ContributionResponse(BaseModel):
    success: bool
    message: str

class QuestionContributionSchema(Question):
    pass

class ExampleContributionSchema(Example):
    pass