from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Building(Base):
    """
    Модель для представления зданий.
    
    Attributes:
        id (int): Уникальный идентификатор здания
        address (str): Адрес здания
        latitude (float): Широта местоположения
        longitude (float): Долгота местоположения
        organizations (List[Organization]): Организации в здании
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Отношения
    organizations = relationship("Organization", back_populates="building") 
