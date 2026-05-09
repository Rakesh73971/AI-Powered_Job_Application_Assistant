from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from app.models.analysis import Status

class AnalysisReportCreate(BaseModel):
    resume_id: int
    jd_id: int

class AnalysisReportUpdate(BaseModel):
    match_score: Optional[float] = None
    missing_skills: Optional[Union[Dict[str, Any], List[Any]]] = None
    weak_sections: Optional[Union[Dict[str, Any], List[Any]]] = None
    suggestions: Optional[Union[Dict[str, Any], List[Any]]] = None
    cover_letter: Optional[str] = None
    status: Optional[Status] = None
    task_id: Optional[str] = None

class AnalysisReportResponse(AnalysisReportCreate):
    id: int
    user_id: int
    match_score: Optional[float] = None
    missing_skills: Optional[Union[Dict[str, Any], List[Any]]] = None
    weak_sections: Optional[Union[Dict[str, Any], List[Any]]] = None
    suggestions: Optional[Union[Dict[str, Any], List[Any]]] = None
    cover_letter: Optional[str] = None
    status: Status
    task_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)