from sqlalchemy  import Column, Integer, SQLEnum, Float, DateTime
from datetime import datetime
from databases.base import Base
from core.enum import TaskPriority
from core.enum import TaskStatus

class Task(Base):
    __tablename__=tasks
    id=Column(Integer, primary_key=True, autoincrement=True)
    title=Column(String)
    description=Column(String)
    priority=Column(SQLEnum(TaskPriority),nullable=false)
    status=Column(SQLEnum(TaskStatus), nullable=false)
    due_date=Column(Date)
    project_id=Column(Integer,ForeignKey("projects.id"))
    creator_id=Column(Integer, ForeignKey("users.id"))
    created_at=Column(DateTime, default=datetime.utcnow )
    updated_at=Column(DateTime, default=datetime.utcnow ,onupdate=datetime.utcnow)