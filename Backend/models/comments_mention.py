from sqlalchemy  import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from Backend.database.base import Base

class CommentMention(Base):
    __tablename__="comment_mentions"
    id=Column(Integer,primary_key=True, autoincrement=True)
    comment_id=Column(Integer, ForeignKey("comments.id"))
    user_id=Column(Integer, ForeignKey("users.id"))
    created_at=Column(DateTime, default=datetime.utcnow)
    

