# Quick Reference Guide - New Project Structure

## ✅ What Was Done

Your project has been successfully restructured to match the target layout. Here's what changed:

### Directory Changes
| Old Path | New Path |
|----------|----------|
| `src/app.py` | `src/app/main.py` |
| `src/routes.py` | `src/app/routes.py` |
| `src/core/auth/` | `src/app/auth/` |
| `src/core/core.py` | Removed (empty file) |
| `alembic/` | `migrations/` |

### New Core Modules (in `src/app/`)
- **`main.py`** - FastAPI app initialization
- **`db.py`** - Database engine and session management
- **`schemas.py`** - All Pydantic request/response models
- **`security.py`** - Password hashing, token generation
- **`dependencies.py`** - Dependency injection functions

### Organized Packages
- **`auth/`** - Authentication feature
  - `controller/` - Route handlers
  - `dto/` - Request/response models
  - `model/` - Database models
  - `service/` - Business logic & token utilities
- **`controllers/`** - Ready for other controllers
- **`models/`** - Ready for other models

### Configuration
- **`migrations/env.py`** - Updated to import models and use `settings.DB_URL_STRING`
- **`alembic.ini`** - Updated to point to `migrations/` directory

---

## 📝 How to Update Your Entry Point

Update your `main.py` at the project root:

```python
from app.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🔄 Running Migrations

The migration commands remain the same:

```bash
# Generate new migration
python -m alembic revision --autogenerate -m "Add new table"

# Apply migrations
python -m alembic upgrade head

# Rollback
python -m alembic downgrade -1
```

---

## 📦 Common Import Patterns

### Authentication Routes
```python
from app.auth.controller.auth_controller import auth_router
from app.auth.model.User import User
```

### Schemas & Security
```python
from app.schemas import LoginRequest, TokenResponse
from app.security import hash_password, verify_password
```

### Database
```python
from app.db import get_session, engine
from sqlmodel import Session
```

### Dependencies
```python
from app.dependencies import get_current_user
```

---

## 🚀 Next Steps

1. **Add more models** to `src/app/models/` as needed
2. **Create feature controllers** in `src/app/controllers/`
3. **Add DTOs** directly in `src/app/schemas.py` or organize by feature
4. **Test imports** to ensure all paths resolve correctly
5. **Review and keep** the old `src/core/` directory for now if needed, or delete it once verified

---

## 📚 File Locations Summary

| Purpose | Location |
|---------|----------|
| App initialization | `src/app/main.py` |
| API routes | `src/app/routes.py` |
| Schemas (DTOs) | `src/app/schemas.py` |
| Security utilities | `src/app/security.py` |
| Database config | `src/app/db.py` |
| Dependencies | `src/app/dependencies.py` |
| Auth routes | `src/app/auth/controller/auth_controller.py` |
| Auth models | `src/app/auth/model/User.py` |
| Token utilities | `src/app/auth/service/tokens.py` |
| Config settings | `src/config.py` |
| Migrations | `migrations/` |

---

## ⚠️ Important Notes

- Old `src/core/` directory still exists - you can delete it after verifying everything works
- All imports have been updated in new files
- Database models automatically imported in `migrations/env.py`
- Configuration uses environment variables via `src/config.py`

