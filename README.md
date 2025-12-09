# OrgChat - Authentication Service (Minimal)

This is a minimal, self-contained authentication service for OrgChat. It implements:

- JWT access tokens and refresh tokens
- Password hashing using Argon2 (via passlib)
- Endpoints:
  - `POST /auth/login` (username/password or OAuth stub)
  - `POST /auth/logout`
  - `POST /auth/refresh-token`
  - `POST /auth/reset-password/request`
  - `POST /auth/reset-password/confirm`

Run locally:

1. Create a virtualenv and install deps:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the app:

```powershell
uvicorn main:app --reload --port 8000
```

Notes:
- This is intentionally simple and for demonstration. In production you should:
  - Use a secure secret key from env vars.
  - Use HTTPS and secure cookie storage for refresh tokens where appropriate.
  - Persist refresh tokens and reset tokens in a secure store and add revocation/blacklisting if needed.

Project structure (auth-only):

- `main.py` - FastAPI app and router registration
- `auth.py` - The authentication router and endpoint implementations
- `models.py` - SQLModel DB models (User)
- `database.py` - SQLModel engine and helper for creating tables
- `schemas.py` - Pydantic request/response schemas
- `tokens.py` - JWT creation/validation helpers
- `utils.py` - password hashing and helpers
- `requirements.txt` - dependencies
