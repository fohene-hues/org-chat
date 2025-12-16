from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from fastapi_jwt_auth.exceptions import MissingTokenError
import jwt

# Router for organizing routes
base_routes = APIRouter()

# ROOT ROUTE
@base_routes.get("/")
def home():
    return {
        "message": "Welcome to Org Chat Backend!",
        "description": "API backend for Org Chat Platform.",
        "default endpoints": [
            "Authentication",
            "File / Document Management",
            "Message and Task Queuing",
            "Notifications",
        ],
        "note": "Pay attention to the API Documentation via README.md.",
    }

# DOCUMENATION ROUTE
@base_routes.get("/docs-info")
def docs_info():
    return {
        "message": "API Documentation is available at /docs or /redoc endpoints.",
        "note": "Ensure to check the README.md for setup and usage instructions.",
    }
