from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime


class CommentCreate(BaseModel):
    task_id:int           #task id only be required only when it is not comming from the url
    comment:str= Field(..., min_length=1, max_length=1000)

    
class CommentOut(BaseModel):
    id:int
    comment:str
    task_id:int
    user_id:int
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)
class CommentUpdate(BaseModel):
    comment:str= Field(..., min_length=1, max_length=1000)

