from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResumeCreate(BaseModel):
    file_name: str
    file_path: str
    extracted_text: str
    is_active: bool
    created_at: datetime

class ResumeUpdate(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    extracted_text: Optional[str] = None
    is_active: Optional[bool] = None

class ResumeResponse(ResumeCreate):
    user_id: int
    id: int

    class Config:
        from_attributes = True