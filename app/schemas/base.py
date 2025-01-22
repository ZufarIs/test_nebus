from typing import List, Optional, ForwardRef
from pydantic import BaseModel, field_validator
import re

# Forward references
OrganizationRef = ForwardRef('Organization')
BuildingRef = ForwardRef('Building')
ActivityRef = ForwardRef('Activity')

class PhoneNumber(BaseModel):
    """Схема для телефонного номера."""
    phone: str

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError('Invalid phone number')
        return v

    class Config:
        from_attributes = True 
