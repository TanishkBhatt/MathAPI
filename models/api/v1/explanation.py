from pydantic import BaseModel
from models.components.main import Explain

class ExplanationResponse(BaseModel):
    success: bool
    message: str
    explanation: Explain