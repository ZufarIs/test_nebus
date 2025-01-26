from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ActivityBase(BaseModel):
    """Базовая схема для общих полей."""
    name: str
    level: int
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    """Схема для создания Activity (без id)."""
    pass

class ActivitySimple(ActivityBase):
    """Упрощенная схема для использования в других моделях."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class Activity(ActivityBase):
    """Схема для отображения Activity (с id)."""
    id: int
    children: List['Activity'] = []  # По умолчанию пустой список

    model_config = ConfigDict(from_attributes=True)

Activity.model_rebuild() 
