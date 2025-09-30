
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load the .env file
load_dotenv()

# Fetch values
backend_url = os.getenv("BACKEND_URL")
database_url = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:Denmarks123$@localhost/wati_clone'


SQLALCHEMY_DATABASE_URL = database_url or "sqlite+aiosqlite:///./wati.db"

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Denmarks123$@localhost/wati_clone'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()



# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool
from sqlalchemy import text
import asyncio


url = make_url(SQLALCHEMY_DATABASE_URL)

# Log the DB driver/scheme (no secrets)
print(f"Using database driver: {url.drivername}")

# Configure engine options conditionally per backend
engine_kwargs: Dict[str, Any] = {
    "echo": True,
    "future": True,
}

if url.drivername.startswith("sqlite"):
    # SQLite (aiosqlite) works best without pooling in many cases
    engine_kwargs.update({
        "poolclass": NullPool,
        "connect_args": {"timeout": 30},
    })
else:
    # Assume a networked DB like Postgres
    engine_kwargs.update({
        "pool_recycle": 120,
        "pool_pre_ping": True,
        "pool_size": 30,
    })

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)


async def ensure_database_ready() -> None:
    """Ensure DB is reachable; if Postgres fails, fallback to SQLite.

    This is intended for development ergonomics. In production, provide a
    reachable `DATABASE_URL` and do not rely on fallback behavior.
    """
    global engine, AsyncSessionLocal, SQLALCHEMY_DATABASE_URL, url

    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return
    except Exception as exc:
        # If it's not Postgres, just re-raise
        if not url.drivername.startswith("postgres"):
            raise

        print(f"Primary database not reachable ({url.drivername}); falling back to SQLite. Error: {exc}")

        # Reconfigure to SQLite fallback
        fallback_url = "sqlite+aiosqlite:///./wati.db"
        SQLALCHEMY_DATABASE_URL = fallback_url
        url = make_url(SQLALCHEMY_DATABASE_URL)

        fallback_engine_kwargs: Dict[str, Any] = {
            "echo": True,
            "future": True,
            "poolclass": NullPool,
            "connect_args": {"timeout": 30},
        }
        engine = create_async_engine(SQLALCHEMY_DATABASE_URL, **fallback_engine_kwargs)
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

# Create a session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    
)

# Base class for declarative models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

