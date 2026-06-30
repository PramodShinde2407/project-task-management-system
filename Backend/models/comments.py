from sqlalchemy  import Column, Integer, Float, DateTime, ForeignKey,String
from datetime import datetime
from Backend.database.base import Base

class Comment(Base):
    __tablename__ = "comments"
    id= Column(Integer, primary_key=True, autoincrement=True)
    comment= Column(String)
    task_id=Column(Integer, ForeignKey("tasks.id"))
    user_id=Column(Integer, ForeignKey("users.id"))
    created_at= Column(DateTime, default=datetime.utcnow)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    