from sqlalchemy  import Column, Integer, Float, DateTime, String
from datetime import datetime
from Backend.databases.base import Base

class Notification(Base):
    __tablename__="notifications"
    id=Column(Integer, primary_key=True, autoincrement=True)
    message= Column(String)
    created_at= Column(DateTime, default=datetime.utcnow)
    