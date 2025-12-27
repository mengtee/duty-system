from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./shift_management.db')

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    @staticmethod
    def create_tables():
        """Create all database tables."""
        Base.metadata.create_all(bind=engine)
    
    @staticmethod
    def drop_tables():
        """Drop all database tables (for testing)."""
        Base.metadata.drop_all(bind=engine)
    
    @staticmethod
    def get_session() -> Generator[Session, None, None]:
        """
        Get database session for dependency injection.
        
        Yields:
            Database session
        """
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()