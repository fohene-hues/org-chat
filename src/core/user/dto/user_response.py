from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class UserResponse(SQLModel):
    id: int
    username: str
    email: EmailStr
    name: Optional[str] = None
    department: Optional[str] = None
    is_active: bool
    created_at: datetime


    class Config:
        orm_mode = True
