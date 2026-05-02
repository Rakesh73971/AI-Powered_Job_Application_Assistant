from pydantic import BaseModel
from datetime import datetime

class JodDescriptionCreate(BaseModel):
    user_id: int
    company: str
    role_title: str
    jb_text: str
    created_at: datetime

class JobDescriptionResponse(JodDescriptionCreate):
    id: int

    class Config:
        from_attributes=True