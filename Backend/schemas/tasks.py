from pydantic import BaseModel, Field
from datetime import date, datetime
from Backend.core.enum import TaskStatus, TaskPriority
from pydantic import ConfigDict
from typing import Optional

class TaskCreate(BaseModel):
    title:str=Field(..., min_length=5, max_length=50)
    description:str=Field(..., min_length=10, max_length=200)
    priority:TaskPriority
    project_id:int
    due_date:date
    
#during creation of task we dont enter status -it set todo by default and can be change after by only manger or admin, creator also user not enter , it will be feteched from user logedin, createdat and updatedat are by default

class TaskOut(BaseModel):
    id:int
    title:str
    description:str
    priority:TaskPriority
    project_id:int
    status:TaskStatus
    due_date:date
    creator_id:int
    created_at:datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class TaskUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None
    priority:Optional[TaskPriority]=None
    due_date:Optional[date]=None
    status:Optional[TaskStatus]=None
    


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskPriorityUpdate(BaseModel):
    priority: TaskPriority

class TaskAssign(BaseModel):
    user_id: int = Field(..., gt=0)