from pydantic import BaseModel,Field
from typing_extensions import Optional


class Chat(BaseModel):
       thread_id:str=Field(...,min_length=1)
       message:str=Field(...,max_length=10000)