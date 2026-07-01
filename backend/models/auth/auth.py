from pydantic import BaseModel, EmailStr, Field
from typing import Any

class AuthRequest(BaseModel):
    username: str
    email: EmailStr

class APIKeyData(BaseModel):
    username: str
    api_key: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    api_key_data: APIKeyData