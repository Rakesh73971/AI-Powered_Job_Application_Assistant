from sqlalchemy import Column,Integer,ForeignKey,String,Text,TIMESTAMP,text
from app.db.database import Base

class CoverLetterHistory(Base):
    __tablename__="cover_letter_histories"

    id = Column(Integer,primary_key=True,nullable=False)
    report_id = Column(Integer,ForeignKey('analysis_reports.id'),nullable=False)
    tone = Column(String,default='formal',nullable=False)
    content = Column(Text,nullable=False)
    generated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    