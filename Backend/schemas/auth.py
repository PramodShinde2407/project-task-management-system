#auth.py → Login, JWT, password management


from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from Backend.schemas.users import UserOut
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class LoginResponse(BaseModel):
    access_token:str
    token_type:str
    user:UserOut     #frontend immediately know who logged in.-because this response is send by  server to client i.e to frontend so no need to give extra get req for who loged in
