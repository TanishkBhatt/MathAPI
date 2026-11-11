from pydantic import BaseModel
from typing import Dict

class HomeResponse(BaseModel):
    success: bool
    message: str
    help: Dict[str, str]
    docs: str
    repo: str
    demo_app: str
    author: str
