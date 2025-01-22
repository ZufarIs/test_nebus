from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Таблица для связи many-to-many между организациями и видами деятельности
organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Organization(Base):
    """Модель организации."""
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    # Отношения
    building = relationship("Building", back_populates="organizations")
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations"
    )
    phones = relationship("PhoneNumber", back_populates="organization")

class PhoneNumber(Base):
    """Модель телефонного номера."""
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="phones")
