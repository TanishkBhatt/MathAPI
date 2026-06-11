from pydantic import BaseModel
from typing import List
from backend.models.objects.main import Topic

class GetAllTopicsResponse(BaseModel):
    success: bool
    message: str
    topics: List[Topic]