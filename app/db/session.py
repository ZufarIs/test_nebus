from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
"""SQLAlchemy engine для подключения к базе данных."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Фабрика сессий SQLAlchemy."""

def get_db():
    """
    Генератор сессий базы данных.
    
    Yields:
        Session: Сессия SQLAlchemy
        
    Note:
        Автоматически закрывает сессию после использования
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
