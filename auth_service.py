from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def token_expiry(minutes: int = 60) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)
