"""Database configuration and setup for the Product API."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.models.product import Base

# Database configuration
DATABASE_URL = "sqlite:///./products.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    """Create all database tables.
    
    This function creates all tables defined in the Base metadata.
    Should be called during application startup.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency function to get database session.
    
    This function provides a database session for dependency injection
    in FastAPI endpoints. The session is automatically closed after use.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()