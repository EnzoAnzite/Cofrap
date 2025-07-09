# backend/app/main.py

from fastapi import FastAPI
from .routers import auth, users
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Backend FastAPI with MySQL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    """
    À l'initialisation de FastAPI, ouvre une connexion
    et crée toutes les tables manquantes via SQLAlchemy.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
