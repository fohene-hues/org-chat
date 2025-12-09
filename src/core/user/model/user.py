from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    department: Optional[str] = None

    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    role: Optional[Role] = Relationship(back_populates="users")

    refresh_token: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None
