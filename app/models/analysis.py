from sqlalchemy import Column,Integer,Float,ForeignKey,JSON,Text,String,TIMESTAMP,text,Enum as SAEnum
from app.core.database import Base
from enum import Enum

class Status(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class AnalysisReport(Base):
    __tablename__="analysis_reports"

    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    resume_id = Column(Integer,ForeignKey('resumes.id'),nullable=False)
    jd_id = Column(Integer,ForeignKey('job_descriptions.id'),nullable=False)
    match_score = Column(Float,nullable=True)
    missing_skills = Column(JSON,nullable=True)
    weak_sections = Column(JSON,nullable=True)
    suggestions = Column(JSON,nullable=True)
    cover_letter = Column(Text)
    status = Column(SAEnum(Status,values_callable=lambda x:[e.value for e in x]),
                    default=Status.PENDING,
                    nullable=False)
    task_id = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
