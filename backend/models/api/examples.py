from pydantic import BaseModel
from typing import List
from backend.models.objects.main import Example

class GetExamplesResponse(BaseModel):
    success: bool
    message: str
    examples: List[Example]