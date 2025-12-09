from fastapi import FastAPI, Depends
from database import create_db_and_tables
from auth_controller import router as auth_router

app = FastAPI(title="OrgChat - Auth Service")

app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health():
    return {"status": "ok"}
