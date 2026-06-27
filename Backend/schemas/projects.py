
from pydantic import BaseModel, Field
from datetime import date, datetime
from Backend.core.enum import ProjectStatus
from pydantic import ConfigDict
from typing import Optional

class ProjectCreate(BaseModel):
    name:str=Field(..., min_length=3, max_length=100)
    description:str=Field(..., min_length=10, max_length=500)
    start_date:date
    end_date:date
    
class ProjectOut(BaseModel):
    id:int
    name:str
    description:str
    start_date:date
    end_date:date
    status:ProjectStatus
    manager_id:int
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)
    
# we are keeping every filed of updation optional because sometimes we want only updation of 1 thing or 2 or 3
class ProjectUpdate(BaseModel):
    name:Optional[str]=None
    description:Optional[str]=None
    start_date:Optional[date]=None
    end_date:Optional[date]=None
    status:Optional[ProjectStatus]=None