from pydantic import BaseModel
from typing import List
from backend.models.components.main import Topic

class GetAllTopicsResponse(BaseModel):
    success: bool
    message: str
    total_topics: int
    topics: List[Topic]