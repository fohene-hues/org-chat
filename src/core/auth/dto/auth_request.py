from pydantic import BaseModel, EmailStr
from typing import Optional





class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    # For OAuth stub
    provider: Optional[str] = None
    provider_token: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: str


class ResetRequest(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str
