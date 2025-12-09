from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Stored refresh token (in real apps store hashed token instead)
    refresh_token: Optional[str] = None
    # Password reset token and expiry
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None
