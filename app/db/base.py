from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

Base = declarative_base()
"""Базовый класс для всех моделей SQLAlchemy."""

class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy с поддержкой декларативного стиля."""
    pass 
