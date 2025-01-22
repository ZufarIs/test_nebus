from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

# Определение связующей таблицы для телефонов
organization_phones = Table(
    'organization_phones',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('phone', String, primary_key=True)
)
"""Связующая таблица для хранения телефонных номеров организаций."""

# Определение связующей таблицы для активностей
organization_activities = Table(
    'organization_activities',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True)
)
"""Связующая таблица для связи организаций с видами деятельности."""

class Organization(Base):
    """
    Модель для представления организаций.
    
    Attributes:
        id (int): Уникальный идентификатор организации
        name (str): Название организации
        building_id (int): ID здания, где находится организация
        phones (List[str]): Список телефонных номеров
        activities (List[Activity]): Виды деятельности организации
        building (Building): Связь со зданием
    """
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    level = Column(Integer)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    
    # Исправленные отношения
    phones = relationship("str", secondary=organization_phones)
    activities = relationship("Activity", secondary=organization_activities, backref="organizations")
    parent = relationship("Organization", remote_side=[id], backref="children")
    building = relationship("Building", back_populates="organizations")
