from sqlalchemy  import Column, Integer, Enum, Float, Date,DateTime, String, ForeignKey
from datetime import datetime
from Backend.databases.base import Base
from ..core.enum import ProjectStatus

class Project(Base):
    __tablename__="projects"
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    description=Column(String)
    start_date=Column(Date)
    end_date=Column(Date)
    status=Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNED)
    manager_id=Column(Integer,ForeignKey("users.id"))
    created_at=Column(DateTime, default=datetime.utcnow)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
