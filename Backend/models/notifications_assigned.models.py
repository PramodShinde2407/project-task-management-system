from sqlalchemy  import Column, Integer, SQLEnum, Float, DateTime
from datetime import datetime
from databases.base import Base

class NotificationAssinged(Base):
    __tablename__=" notifications_assingned"
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    notification_id=Column(Integer, ForeignKey("notifications.id"))
    created_at= Column(DateTime, default=datetime.utcnow)
    