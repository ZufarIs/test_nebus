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
    phones = relationship(
        "PhoneNumber", 
        back_populates="organization",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
        uselist=True
    )
    activities = relationship(
        "Activity",
        secondary="organization_activity",
        back_populates="organizations",
        cascade="save-update, merge"
    )
    building = relationship("Building", back_populates="organizations")

class PhoneNumber(Base):
    """Модель телефонного номера."""
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="phones")
