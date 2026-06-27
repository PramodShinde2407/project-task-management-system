from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime
from typing import Optional

class NotificationOut(BaseModel):
    id:int
    message:str
    is_read:bool
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)



class NotificationUpdate(BaseModel):
    is_read:Optional[bool]=None