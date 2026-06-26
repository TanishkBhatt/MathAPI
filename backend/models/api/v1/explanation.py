from pydantic import BaseModel
from backend.models.components.main import Explain

class ExplanationResponse(BaseModel):
    success: bool
    message: str
    explanation: Explain
