from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResumeCreate(BaseModel):
    file_name: str
    file_path: str
    is_active: bool


class ResumeUpdate(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    extracted_text: Optional[str] = None
    is_active: Optional[bool] = None

class ResumeResponse(ResumeCreate):
    id: int
    user_id: int
    extracted_text: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True