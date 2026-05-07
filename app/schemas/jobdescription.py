from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JodDescriptionCreate(BaseModel):
    company: str
    role_title: str
    jb_text: str
    created_at: datetime

class JobDescriptionUpdate(BaseModel):
    company: Optional[str] = None
    role_title: Optional[str] = None
    jb_text: Optional[str] = None

class JobDescriptionResponse(JodDescriptionCreate):
    user_id: int
    id: int

    class Config:
        from_attributes=True