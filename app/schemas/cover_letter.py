from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CoverLetterCreate(BaseModel):
    report_id: int
    tone: str
    content: str

class CoverLetterUpdate(BaseModel):
    tone: Optional[str] = None
    content: Optional[str] = None

class CoverLetterResponse(CoverLetterCreate):
    id: int
    generated_at: datetime

    class Config:
        from_attributes = True
