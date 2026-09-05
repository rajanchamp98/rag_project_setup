from fastapi import APIRouter,Depends
from collections.abc import AsyncIterable
from fastapi.sse import EventSourceResponse,ServerSentEvent
from app.chat.schema import ThreadResponse,CreateThreadRequest,ChatRequest
from app.auth.dependency import get_current_user
from app.chat.service import create_chat_thread,stream_chat


router=APIRouter(
    prefix="/chat",
    tags=["chat routes"])




@router.post("/thread",response_model=ThreadResponse)
async def create_thread_route(request:CreateThreadRequest,current_user=Depends(get_current_user)):
    user_id=current_user["_id"]
    result=await create_chat_thread(user_id=user_id,title=request.title)
    return result

@router.post("/",response_class=EventSourceResponse)
async def chat_route(request:ChatRequest,current_user=Depends(get_current_user))->AsyncIterable[ServerSentEvent]:
    user_id=current_user["_id"]
    thred_id=request.thread_id
    content=request.message

    async for event in stream_chat(thread_id=thred_id,user_id=user_id,message=content):
        yield event




