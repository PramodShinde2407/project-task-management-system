from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from Backend.database.base import Base
from Backend.core.enum import UserRole
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, autoincrement=True)
    name=Column(String)
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    password_hash=Column(String)
    role=Column(Enum(UserRole), nullable=False,default=UserRole.TEAM_MEMBER)  # at start we are giving user role by default later only admin have access to change it
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)


