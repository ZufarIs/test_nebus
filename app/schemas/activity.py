from typing import Optional, List
from pydantic import BaseModel

class ActivityBase(BaseModel):
    """
    Базовая схема для вида деятельности.
    
    Attributes:
        name (str): Название вида деятельности
        parent_id (Optional[int]): ID родительского вида деятельности
        level (int): Уровень в иерархии
    """
    name: str
    level: Optional[int] = 1
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    """Схема для создания нового вида деятельности."""
    pass

class Activity(ActivityBase):
    """
    Схема для отображения вида деятельности.
    
    Дополнительные атрибуты:
        id (int): Уникальный идентификатор
    """
    id: int
    children: List['Activity'] = []

    class Config:
        from_attributes = True

# Для решения проблемы с циклическими ссылками
Activity.model_rebuild() 
