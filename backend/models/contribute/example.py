from pydantic import BaseModel
from backend.models.components.main import Example

class ExampleContributionSchema(Example):
    pass

class ContributionResponse(BaseModel):
    success: bool
    message: str