from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ActivityBase(BaseModel):
    """Базовая схема вида деятельности."""
    name: str
    level: int
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    """Схема для создания вида деятельности."""
    pass

class Activity(ActivityBase):
    """Схема для отображения вида деятельности."""
    id: int
    children: List['Activity'] = []

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

# Необходимо для правильной работы рекурсивных ссылок
Activity.model_rebuild() 
