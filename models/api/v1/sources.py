from pydantic import BaseModel
from typing import List
from models.components.main import LearningSource

class GetSourcesResponse(BaseModel):
    success: bool
    message: str
    total_sources: int
    sources: List[LearningSource]