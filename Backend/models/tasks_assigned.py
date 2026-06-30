from sqlalchemy  import Column, Integer, Float, DateTime,ForeignKey
from datetime import datetime
from Backend.database.base import Base

class TaskAssigned(Base):
    __tablename__="tasks_assigned"
    id=Column(Integer, primary_key=True, autoincrement=True)
    task_assined_user_id= Column(Integer, ForeignKey("users.id"))
    task_id=Column(Integer, ForeignKey("tasks.id"))
    created_at= Column(DateTime, default=datetime.utcnow)
    