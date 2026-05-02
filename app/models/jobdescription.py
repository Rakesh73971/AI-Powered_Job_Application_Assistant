from sqlalchemy import Column,Integer,String,ForeignKey,Text,TIMESTAMP,text
from app.core.database import Base

class JobDescription(Base):
    __tablename__="job_descriptions"

    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    company_name = Column(String)
    role_title = Column(String,nullable=False)
    jd_text = Column(Text,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))