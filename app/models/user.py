from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,Enum as SAEnum
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
    password = Column(String,nullable=False)
    role = Column(SAEnum(UserRole,values_callable=lambda x:[e.value for e in x]),
            default=UserRole.USER,
            nullable=False
    )
    is_active = Column(Boolean,server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))