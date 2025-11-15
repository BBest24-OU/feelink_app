"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://feelink_user:feelink_password@postgres:5432/feelink_db"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,        # Connection pool size
    max_overflow=20,     # Max overflow connections
    echo=False,          # Set to True for SQL logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.
    Yields a database session and ensures it's closed after use.

    Usage in FastAPI:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database (create tables if they don't exist).
    This is mainly for development. In production, use Alembic migrations.
    """
    from app.models import Base
    Base.metadata.create_all(bind=engine)
