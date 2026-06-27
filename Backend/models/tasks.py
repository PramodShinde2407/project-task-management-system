from sqlalchemy  import Column, Integer, Enum, String, DateTime,ForeignKey,Date
from datetime import datetime
from Backend.databases.base import Base
from ..core.enum import TaskPriority
from ..core.enum import TaskStatus

class Task(Base):
    __tablename__="tasks"
    id=Column(Integer, primary_key=True, autoincrement=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Enum(TaskPriority),nullable=False)
    status=Column(Enum(TaskStatus), nullable=False, default=TODO)
    due_date=Column(Date)
    project_id=Column(Integer,ForeignKey("projects.id"))
    creator_id=Column(Integer, ForeignKey("users.id"))
    created_at=Column(DateTime, default=datetime.utcnow ) # this will be fetched from logedin user directly
    updated_at=Column(DateTime, default=datetime.utcnow ,onupdate=datetime.utcnow)