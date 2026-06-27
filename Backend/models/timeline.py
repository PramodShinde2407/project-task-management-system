from sqlalchemy  import Column, Integer, Float, DateTime,ForeignKey, String
from datetime import datetime
from Backend.databases.base import Base

class Timeline(Base):
    __tablename__="timeline"
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    task_id=Column(Integer, ForeignKey("tasks.id"))
    action=Column(String)
    old_value=Column(String)
    new_value=Column(String)
    created_at= Column(DateTime, default=datetime.utcnow)
    