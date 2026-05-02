from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,TIMESTAMP,text,Text
from app.core.database import Base

class Resume(Base):
    __tablename__="resumes"

    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    file_name = Column(String,nullable=False)
    file_path = Column(String,nullable=False)
    extracted_text = Column(Text)
    is_active = Column(Boolean,server_default='True',nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))