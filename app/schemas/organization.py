from typing import List
from pydantic import BaseModel, ConfigDict
from .activity import ActivitySimple
from .building import Building

class PhoneNumberBase(BaseModel):
    """Базовая схема для телефонного номера."""
    phone: str

class PhoneNumberCreate(PhoneNumberBase):
    """Схема для создания телефонного номера (без id)."""
    pass

class PhoneNumber(PhoneNumberBase):
    """Схема для отображения телефонного номера (с id)."""
    id: int
    organization_id: int

    model_config = ConfigDict(from_attributes=True)

class OrganizationBase(BaseModel):
    """Базовая схема для общих полей."""
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    """Схема для создания Organization (без id)."""
    phones: List[str]
    activities: List[int]

class Organization(OrganizationBase):
    """Схема для отображения Organization (с id)."""
    id: int
    phones: List[PhoneNumber]
    activities: List[ActivitySimple]
    building: Building

    model_config = ConfigDict(from_attributes=True)

class OrganizationDetail(Organization):
    """Расширенная схема организации с отношениями."""
    pass

OrganizationDetail.model_rebuild() 
