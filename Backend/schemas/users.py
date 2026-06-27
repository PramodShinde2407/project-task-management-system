#user.py → User CRUD operations
from pydantic import BaseModel ,Field, EmailStr
from datetime import datetime
from typing import Optional
from Backend.core.enum import UserRole
from pydantic import ConfigDict

class UserCreate(BaseModel):
    name:str= Field(..., min_length=2, max_length=50)
    username:str= Field(..., min_length=2, max_length=50)
    email:EmailStr
    password:str=Field(...,min_length=8)
    
class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    username:str
    role:UserRole
    created_at:datetime
    model_config = ConfigDict(from_attributes=True) #This allows FastAPI to convert SQLAlchemy model instances into UserOut.
    
class UserUpdate(BaseModel):
    name:Optional[str]=None
    email:Optional[EmailStr]=None
    

    
    