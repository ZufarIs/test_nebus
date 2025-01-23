from typing import List, TYPE_CHECKING
from pydantic import BaseModel, Field, validator, ConfigDict
from .base import PhoneNumber
import re
from .activity import ActivitySimple
from .building import Building

if TYPE_CHECKING:
    from .building import Building
    from .activity import Activity

class OrganizationBase(BaseModel):
    """Базовая схема организации."""
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    """Схема для создания организации."""
    phones: List[str]
    activity_ids: List[int]

class Organization(OrganizationBase):
    """Схема для отображения организации."""
    id: int
    phones: List['PhoneNumber']
    
    model_config = ConfigDict(
        from_attributes=True
    )

class OrganizationDetail(Organization):
    """Расширенная схема организации с отношениями."""
    building: Building
    activities: List[ActivitySimple]

    model_config = ConfigDict(
        from_attributes=True
    )

class PhoneNumberBase(BaseModel):
    phone: str = Field(..., description="Номер телефона в формате +7XXXXXXXXXX")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^\+7\d{10}$', v):
            raise ValueError('Номер телефона должен быть в формате +7XXXXXXXXXX')
        return v

    model_config = ConfigDict(
        from_attributes=True
    )

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int
    organization_id: int

OrganizationDetail.model_rebuild() 
