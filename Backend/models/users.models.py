from sqlalchemy import Column, Integer,Float,String,DateTime
from datetime import datetime
from databases.base import Base
from core.enum import UserRole
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, autoincrement=True)
    name=Column(String)
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    password_hash=Column(String)
    role=Column(SQLEnum(UserRole), nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)