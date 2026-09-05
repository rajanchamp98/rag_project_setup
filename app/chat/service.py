from app.chat.repository import (create_thread,get_thread,create_message,get_chat_history)
from fastapi import HTTPException
from collections.abc import AsyncIterable
from fastapi.sse import ServerSentEvent,EventSourceResponse
import secrets
from app.llm.chat_model import get_chat_model
from app.rag.retrieve import get_retrivers



async def create_chat_thread(user_id:str,title:str | None):
    thread_id=secrets.token_urlsafe(24)

    await create_thread(user_id=user_id,thread_id=thread_id,title=title)

    return {
        "thread_id":thread_id,
        "title":title
    }


async def stream_chat(user_id,thread_id,message)->AsyncIterable[ServerSentEvent]:
    thread=await get_thread(thread_id,user_id)

    if not thread:
        raise HTTPException(
            status_code=404,
            detail= "Message thread not found "
        )

    await create_message(
        user_id=user_id,
        thread_id=thread_id,
        content=message,
        role="user"
    )

    history=await get_chat_history(
        user_id=user_id,
        thread_id=thread_id,
        limit=20        
    )

    yield ServerSentEvent(
        event="status",
        data={
            "status":"processing"
        }
    )

    assistent_response=""

    #RAG RELATED WORK START HERE

    reteriver=get_retrivers()

    content=reteriver.invoke(message)

    SYSTEM_PROMPT="""
    
"""






    ## RAG RELATED WORK END HERE 

    response=(
        "Test the response1"
        "Test The response2"
        "Test The response3"
        "Test The response4"
        "Test The response5"
        "Test The response6"
    )

    for token in response.split():
        token+=" "

        assistent_response+=token

        yield ServerSentEvent(
            event="token",
            data=token
        )



    await create_message(user_id=user_id,thread_id=thread_id,content=assistent_response,role="assistant")

    yield ServerSentEvent(
        event="done",
        data={
            "status":"completed"
        }
    )

        


    
