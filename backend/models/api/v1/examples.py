from pydantic import BaseModel
from typing import List
from backend.models.components.main import Example

class GetExamplesResponse(BaseModel):
    success: bool
    message: str
    total_examples: int
    examples: List[Example]