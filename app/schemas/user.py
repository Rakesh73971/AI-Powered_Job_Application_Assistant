from pydantic import BaseModel,EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str,Enum):
    admin = 'admin'
    user = 'user'

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole
    is_active: bool
    created_at: datetime


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: str
    created_at: datetime

    class Config:
        from_attributes=True