from typing import Optional, List
from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    level: Optional[int] = 1
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    children: List['Activity'] = []

    class Config:
        from_attributes = True

# Для решения проблемы с циклическими ссылками
Activity.model_rebuild() 
