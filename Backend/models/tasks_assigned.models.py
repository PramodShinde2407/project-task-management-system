from sqlalchemy  import Column, Integer, SQLEnum, Float, DateTime
from datetime import datetime
from databases.base import Base

class TaskAssigned(Base):
    __tablename__=" tasks_assinged"
    id=Column(Integer, primary_key=True, autoincrement=True)
    task_assined_user_id= Column(Integer, ForeignKey("users.id"))
    task_id=Column(Integer, ForeignKey("tasks.id"))
    created_at= Column(DateTime, default=datetime.utcnow)
    