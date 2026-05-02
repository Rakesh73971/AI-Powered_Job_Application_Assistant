from pydantic import BaseModel
from datetime import datetime


class ResumeCreate(BaseModel):
    user_id: int
    file_name: str
    file_path: str
    extracted_text: str
    is_active: bool
    created_at: datetime

class ResumeResponse(ResumeCreate):
    id: int

    class Config:
        from_attributes = True