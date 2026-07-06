from pydantic import BaseModel
from typing import List
from backend.models.components.main import LearningSource

class GetSourcesResponse(BaseModel):
    success: bool
    message: str
    total_sources: int
    learning_sources: List[LearningSource]