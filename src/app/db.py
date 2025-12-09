# Database configuration file
# Add database connection and session management here
from sqlmodel import SQLModel, create_engine, Session, select
from config import settings
from typing import Generator

# Create engine with async support
engine = create_engine(str(settings.DB_URL_STRING), echo=settings.DB_ECHO, pool_size=settings.DB_POOL_SIZE)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    with Session(engine) as session:
        yield session
