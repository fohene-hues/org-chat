from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional

from app.db import get_session
from app.auth.model.User import User
from app.schemas import LoginRequest, TokenResponse, RefreshRequest, ResetRequest, ResetConfirm
from app.security import hash_password, verify_password, generate_reset_token, token_expiry
from app.auth.service.tokens import create_access_token, create_refresh_token, verify_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, session: Session = Depends(get_session)):
    # Username/password flow
    if body.username and body.password:
        statement = select(User).where((User.username == body.username) | (User.email == body.username))
        user = session.exec(statement).first()
        if not user or not verify_password(body.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access = create_access_token({"sub": str(user.id), "username": user.username})
        refresh = create_refresh_token({"sub": str(user.id)})
        user.refresh_token = refresh
        session.add(user)
        session.commit()
        return TokenResponse(access_token=access, refresh_token=refresh)

    # OAuth stub: provider + provider_token
    if body.provider and body.provider_token:
        # In a real app you'd verify the provider_token with the provider.
        # Here we accept it and create/get a user with provider-token-derived username.
        provider_user_id = f"{body.provider}:{body.provider_token[:8]}"
        statement = select(User).where(User.username == provider_user_id)
        user = session.exec(statement).first()
        if not user:
            user = User(username=provider_user_id, email=f"{provider_user_id}@example.invalid", hashed_password=hash_password(generate_reset_token()))
            session.add(user)
            session.commit()
            session.refresh(user)

        access = create_access_token({"sub": str(user.id), "username": user.username})
        refresh = create_refresh_token({"sub": str(user.id)})
        user.refresh_token = refresh
        session.add(user)
        session.commit()
        return TokenResponse(access_token=access, refresh_token=refresh)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing credentials")


@auth_router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(body: RefreshRequest, session: Session = Depends(get_session)):
    try:
        payload = verify_token(body.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = int(payload.get("sub"))
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if not user or user.refresh_token != body.refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access = create_access_token({"sub": str(user.id), "username": user.username})
    refresh = create_refresh_token({"sub": str(user.id)})
    user.refresh_token = refresh
    session.add(user)
    session.commit()
    return TokenResponse(access_token=access, refresh_token=refresh)


@auth_router.post("/logout")
def logout(body: RefreshRequest, session: Session = Depends(get_session)):
    # Invalidate refresh token by removing it from the user record
    try:
        payload = verify_token(body.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = int(payload.get("sub"))
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.refresh_token != body.refresh_token:
        # Already logged out or token mismatch
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Logged out"})

    user.refresh_token = None
    session.add(user)
    session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Logged out"})


@auth_router.post("/reset-password/request")
def reset_password_request(body: ResetRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == body.email)
    user = session.exec(statement).first()
    if not user:
        # Do not reveal whether the email exists
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "If the email exists, a reset token was sent"})

    token = generate_reset_token()
    user.reset_token = token
    user.reset_token_expires = token_expiry(60)
    session.add(user)
    session.commit()

    # In a real app send email. For demo we return the token.
    return {"detail": "Reset token generated (in production send via email)", "reset_token": token}


@auth_router.post("/reset-password/confirm")
def reset_password_confirm(body: ResetConfirm, session: Session = Depends(get_session)):
    statement = select(User).where(User.reset_token == body.token)
    user = session.exec(statement).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    user.hashed_password = hash_password(body.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    session.add(user)
    session.commit()
    return {"detail": "Password reset successful"}
