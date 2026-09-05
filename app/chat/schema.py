from pydantic import BaseModel,Field


class CreateThreadRequest(BaseModel):
    title:str | None


class ThreadResponse(BaseModel):
    thread_id:str
    title:str | None=None

class ChatRequest(BaseModel):
    thread_id:str=Field(...,min_length=1,description="This is thred id which uniqely identify chat session")
    message:str=Field(...,min_length=1,max_length=100000,description="It will take users question in form of string to be answered")
