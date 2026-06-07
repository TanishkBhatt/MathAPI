from pydantic import BaseModel

class HomeResponse(BaseModel):
    connection: bool
    message: str