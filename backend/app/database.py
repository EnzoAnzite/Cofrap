# app/database.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=True,
)

SessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
Base = declarative_base()


def init_db():
    async def _create():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(_create())


async def get_db():
    """
    Génère une session AsyncSession, la yield puis la ferme.
    À utiliser avec Depends(get_db) dans tes routers.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
