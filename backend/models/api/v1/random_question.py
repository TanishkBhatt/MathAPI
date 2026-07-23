from pydantic import BaseModel
from backend.models.components.main import Question

class RandomQuestionResponse(BaseModel):
    success: bool
    message: str
    question: Question
