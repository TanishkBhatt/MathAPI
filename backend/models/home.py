from pydantic import BaseModel

class HomeResponse(BaseModel):
    success: bool
    message: str