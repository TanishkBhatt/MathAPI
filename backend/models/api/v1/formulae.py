from pydantic import BaseModel
from typing import List
from backend.models.components.main import Formula

class GetFormulaeResponse(BaseModel):
    success: bool
    message: str
    total_formulae: int
    formulae: List[Formula]