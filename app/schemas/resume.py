from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str
    extracted_text: Optional[str] = None
    is_active: bool
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ResumeUpdate(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    extracted_text: Optional[str] = None
    is_active: Optional[bool] = None