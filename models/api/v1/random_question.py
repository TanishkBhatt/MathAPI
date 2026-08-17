from pydantic import BaseModel
from models.components.main import Question

class RandomQuestionResponse(BaseModel):
    success: bool
    message: str
    question: Question