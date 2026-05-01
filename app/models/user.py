from sqlalchemy import Column,Integer,String,TIMESTAMP,text
from enum import Enum as PyEnum
from app.core.database import Base

class UserRole(PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    full_name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,server_default='user',nullable=False)
    role = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))