from pydantic import BaseModel
from backend.models.objects.main import Explain

class ExplinationResponse(BaseModel):
    success: bool
    message: str
    explination: Explain