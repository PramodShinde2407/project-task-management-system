from sqlalchemy  import Column, Integer, DateTime,ForeignKey
from datetime import datetime
from Backend.database.base import Base

class NotificationAssigned(Base):
    __tablename__="notifications_assigned"
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    notification_id=Column(Integer, ForeignKey("notifications.id"))
    created_at= Column(DateTime, default=datetime.utcnow)
    