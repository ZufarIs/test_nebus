from typing import List, TYPE_CHECKING
from pydantic import BaseModel
from .base import PhoneNumber

if TYPE_CHECKING:
    from .building import Building
    from .activity import Activity

class OrganizationBase(BaseModel):
    """Базовая схема организации."""
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    """Схема для создания организации."""
    phones: List[PhoneNumber]
    activity_ids: List[int]

class Organization(OrganizationBase):
    """Схема для отображения организации."""
    id: int
    phones: List[PhoneNumber]
    
    class Config:
        from_attributes = True

class OrganizationDetail(Organization):
    """Расширенная схема организации с отношениями."""
    building: 'Building'
    activities: List['Activity']

    class Config:
        from_attributes = True

from .building import Building
from .activity import Activity

OrganizationDetail.model_rebuild() 
