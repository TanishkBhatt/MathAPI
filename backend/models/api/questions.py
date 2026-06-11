from pydantic import BaseModel
from typing import List
from backend.models.objects.main import Question

class GetQuestionsResponse(BaseModel):
    success: bool
    message: str
    questions: List[Question]