from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JodDescriptionCreate(BaseModel):
    company_name: str
    role_title: str
    jd_text: str

class JobDescriptionUpdate(BaseModel):
    company: Optional[str] = None
    role_title: Optional[str] = None
    jd_text: Optional[str] = None

class JobDescriptionResponse(JodDescriptionCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes=True