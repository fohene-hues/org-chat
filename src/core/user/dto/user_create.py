from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel
from pydantic import EmailStr

# User DTOs
class UserCreate(SQLModel):
    username: str
    email: EmailStr
    name: Optional[str] = None
    department: Optional[str] = None
    password: str
    role_id: Optional[int] = None



