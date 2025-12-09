from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional


user_routes = APIRouter(prefix="/user", tags=["user"])


@user_routes.post("/all", response_model=TokenResponse)
def get_all_users(body: LoginRequest, session: Session = Depends(get_session)):
    statement = select(User)
    users = session.exec(statement).all()
    return users