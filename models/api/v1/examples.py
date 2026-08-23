from pydantic import BaseModel
from typing import List
from models.components.main import Example

class GetExamplesResponse(BaseModel):
    success: bool
    message: str
    total_examples: int
    examples: List[Example]
