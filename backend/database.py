"""
Database initialization and session management module.

This module sets up SQLAlchemy ORM configuration, creates the database engine,
initializes sessions, and creates all database tables on startup. It provides
a dependency injection function for database sessions used throughout the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from models import Base
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

""" Create database engine with SQLite-specific configuration
connect_args={"check_same_thread": False} allows the same connection to be used
across multiple threads, which is necessary for the application's architecture """
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} # Required for SQLite support
)

# Create a session factory bound to the engine
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes are not automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize all database tables defined in the ORM models
# This creates any tables that don't already exist in the database
Base.metadata.create_all(bind=engine)
logger.info("Database initialized")

def get_db():
    """
    Dependency injection function for database sessions.
    
    This function creates a new database session and yields it to the caller.
    It ensures the session is properly closed after use, even if an exception
    occurs during database operations.
    
    Yields:
        SessionLocal: An active SQLAlchemy session for database operations.
        
    Example:
        for db in get_db():
            recording = db.query(Recording).filter(Recording.id == "123").first()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Ensure the session is closed to prevent connection leaks
        db.close()
