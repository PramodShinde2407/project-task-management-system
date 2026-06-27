from sqlalchemy  import Column, Integer, Float, DateTime,ForeignKey
from datetime import datetime
from Backend.databases.base import Base

class ProjectAssigned(Base):
    __tablename__="projects_assigned"
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    project_id=Column(Integer, ForeignKey("projects.id"))
    created_at= Column(DateTime, default=datetime.utcnow)
    
