from typing import List, Optional
from pydantic import BaseModel, field_validator
from .activity import Activity
from .building import Building
import re

class OrganizationBase(BaseModel):
    name: str
    building_id: int

class PhoneNumber(BaseModel):
    phone: str
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError('Invalid phone number')
        return v

class OrganizationCreate(OrganizationBase):
    phones: List[PhoneNumber]
    activity_ids: List[int]

class Organization(OrganizationBase):
    id: int
    building: Building
    activities: List[Activity]
    phones: List[PhoneNumber]

    class Config:
        from_attributes = True 
