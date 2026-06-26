from pydantic import BaseModel, EmailStr, Field
from typing import Any
from enum import Enum
from backend.models.components.main import Example, Question

class ContributionType(Enum):
    example = "Example"
    question = "Question"

class ExampleContributionSchema(Example):
    pass

class QuestionContributionSchema(Question):
    pass

class ContributionResponse(BaseModel):
    success: bool
    message: str