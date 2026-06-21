from pydantic import BaseModel
from typing import List
from backend.models.components.main import Question

class GetQuestionsResponse(BaseModel):
    success: bool
    message: str
    total_questions: int
    questions: List[Question]