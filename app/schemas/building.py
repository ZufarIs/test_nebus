from pydantic import BaseModel, Field
from typing import Optional, List

class BuildingBase(BaseModel):
    """
    Базовая схема для здания.
    
    Attributes:
        address (str): Адрес здания
        latitude (float): Широта
        longitude (float): Долгота
    """
    address: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class BuildingCreate(BuildingBase):
    """Схема для создания нового здания."""
    pass

class Building(BuildingBase):
    """
    Схема для отображения здания.
    
    Дополнительные атрибуты:
        id (int): Уникальный идентификатор
        organizations (List[Organization]): Список организаций в здании
    """
    id: int
    organizations: List['Organization'] = []

    class Config:
        from_attributes = True 
