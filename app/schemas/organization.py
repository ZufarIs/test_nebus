from typing import List, Optional
from pydantic import BaseModel, field_validator
from .activity import Activity
from .building import Building
import re

class PhoneNumber(BaseModel):
    """
    Схема для валидации телефонного номера.
    
    Attributes:
        phone (str): Номер телефона в формате +7XXXXXXXXXX
    """
    phone: str
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """
        Валидация формата телефонного номера.
        
        Args:
            v (str): Номер телефона для проверки
            
        Returns:
            str: Валидный номер телефона
            
        Raises:
            ValueError: Если формат номера неверный
        """
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError('Invalid phone number')
        return v

class OrganizationBase(BaseModel):
    """
    Базовая схема для организации.
    
    Attributes:
        name (str): Название организации
        building_id (int): ID здания
    """
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    """
    Схема для создания организации.
    
    Attributes:
        phones (List[PhoneNumber]): Список телефонных номеров
        activity_ids (List[int]): Список ID видов деятельности
    """
    phones: List[PhoneNumber]
    activity_ids: List[int]

class Organization(OrganizationBase):
    """
    Схема для отображения организации.
    
    Attributes:
        id (int): Уникальный идентификатор
        building (Building): Информация о здании
        activities (List[Activity]): Список видов деятельности
        phones (List[PhoneNumber]): Список телефонных номеров
    """
    id: int
    building: Building
    activities: List[Activity]
    phones: List[PhoneNumber]

    class Config:
        from_attributes = True 
