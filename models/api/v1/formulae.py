from pydantic import BaseModel
from typing import List
from models.components.main import Formula

class GetFormulaeResponse(BaseModel):
    success: bool
    message: str
    total_formulae: int
    formulae: List[Formula]