from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

Base = declarative_base()
"""Базовый класс для всех моделей SQLAlchemy."""

class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy с поддержкой декларативного стиля."""
    pass 

# Импортируем модели для Alembic
from app.db.base_class import Base  # noqa
from app.models.organization import Organization, PhoneNumber  # noqa
from app.models.building import Building  # noqa
from app.models.activity import Activity  # noqa

# Все модели должны быть импортированы здесь для корректной работы Alembic 
