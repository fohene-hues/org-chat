# FastAPI dependencies for injection
# This file contains all dependency providers
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from app.db import get_session
from sqlmodel import Session


def get_current_user(authorize: AuthJWT = Depends()):
    """
    Get current authenticated user from JWT token
    """
    authorize.jwt_required()
    claims = authorize.get_raw_jwt()
    return claims.get("sub")
