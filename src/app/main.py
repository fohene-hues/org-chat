from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
import sys
import os


from app.routes import base_routes
from app.auth.controller.auth_controller import auth_router

from config import settings
from fastapi.exceptions import RequestValidationError
from sqlalchemy import inspect

from loguru import logger
import logging
from contextlib import asynccontextmanager

app = FastAPI(
    title=settings.SERVICE_NAME,
    version="1.0",
    description="""**Org Chat** An AI focused app infrastructure deployed with python.

    Default Endpoints:
    - Authentication
    - File and Document Management
    - Message and Task Queuing
    - Notifications
    """,
    contact={
        "name": "API Support",
        "url": "http://support@orgchat.com",
        "email": "mail@orgchat.com",
    },
    license_info={
        "name": "MIT",
    }
)


# REMOVE auto table creation (Alembic will handle this)


# print("Initializing database tables...")
# Base.metadata.create_all(bind=engine)
# print("Database tables initialized successfully.")

# -----------------------------------------------------------
# Middleware (CORS)
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers

# Routes Registration

app.include_router(base_routes, prefix="/api/v1", tags=["Base Routes"])
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])

# JWT Authentication Settings

class JWTSettings(BaseSettings):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_algorithm: str = settings.ALGORITHM
    authjwt_access_token_expires: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    authjwt_refresh_token_expires: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60  # in seconds


@AuthJWT.load_config
def get_config():
    return JWTSettings()
