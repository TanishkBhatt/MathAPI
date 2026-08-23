from pydantic import BaseModel, EmailStr

class AuthRequest(BaseModel):
    username: str
    email: EmailStr

class APIKeyData(BaseModel):
    username: str
    api_key: str
    expiry: str | None = None

class AuthResponse(BaseModel):
    success: bool
    message: str
    api_key_data: APIKeyData
