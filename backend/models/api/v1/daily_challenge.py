from pydantic import BaseModel
from typing import List
from backend.models.components.main import Question

class DailyChallengeResponse(BaseModel):
    success: bool
    message: str
    challenge_date: str
    total_questions: int
    questions: List[Question]
