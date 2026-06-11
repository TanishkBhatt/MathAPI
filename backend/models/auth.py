from pydantic import BaseModel, EmailStr, Field
from typing import Any

class AuthRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=10)

class AuthResponse(BaseModel):
    success: bool
    message: str
    auth_token: dict[str, Any]