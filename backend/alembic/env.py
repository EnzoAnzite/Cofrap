import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from dotenv import load_dotenv
import os

# charge votre .env
load_dotenv()

# récupère l'URL de la base
DATABASE_URL = os.getenv("DATABASE_URL")

# configuration Alembic
config = context.config
fileConfig(config.config_file_name)

# Patch de l’URL dynamique
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Importez votre Base metadata
from app.database import Base  # adapte selon votre arborescence
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata,
        literal_binds=True, dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode with an async engine."""
    # Crée l’engine asynchrone via la factory, pas via AsyncEngine()
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

