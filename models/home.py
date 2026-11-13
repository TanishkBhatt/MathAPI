from pydantic import BaseModel
from typing import Dict

class help(BaseModel):
    get_started: str
    explore_routes: str
    explore_demo_application: str

class HomeResponse(BaseModel):
    success: bool
    message: str
    help: Dict[str, str]
    docs: str
    repo: str
    author: str
