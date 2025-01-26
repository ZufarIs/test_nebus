from typing import List, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    from .organization import Organization

class BuildingBase(BaseModel):
    """Базовая схема для общих полей."""
    address: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class BuildingCreate(BuildingBase):
    """Схема для создания Building (без id)."""
    pass

class Building(BuildingBase):
    """Схема для отображения Building (с id)."""
    id: int

    model_config = ConfigDict(from_attributes=True)

class BuildingDetail(Building):
    """Расширенная схема здания с организациями."""
    organizations: List['Organization'] = []

    class Config:
        from_attributes = True 
