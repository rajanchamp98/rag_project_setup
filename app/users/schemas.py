from pydantic import BaseModel,Field,EmailStr
from typing_extensions import Optional


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str=Field(...,max_length=128,min_length=8)

class UserResponse(BaseModel):
    id:str
    name:str
    email:EmailStr
    is_active:bool
    


