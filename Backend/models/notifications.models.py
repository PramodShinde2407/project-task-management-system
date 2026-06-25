from sqlalchemy  import Column, Integer, SQLEnum, Float, DateTime
from datetime import datetime
from databases.base import Base

class Notification(Base):
    __tablename__=" notifications"
    id=Column(Integer, primary_key=True, autoincrement=True)
    message= Column(String)
    created_at= Column(DateTime, default=datetime.utcnow)
    