from sqlalchemy  import Column, Integer, SQLEnum, Float, DateTime
from datetime import datetime
from databases.base import Base
from core.enum import ProjectStatus

class Project(Base):
    __tablename__="projects"
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    description=Column(String)
    start_date=Column(Date)
    end_date=Column(Date)
    status=Column(SQLEnum(ProjectStatus), nullable=False)
    manager_id=Column(Integer,ForeignKey("users.id"))
    created_at=Column(Datetime, default=datetime.utcnow)
    updated_at=Column(Datetime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
