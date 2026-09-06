from app.chat.repository import (create_thread,get_thread,create_message,get_chat_history)
from fastapi import HTTPException
from collections.abc import AsyncIterable
from fastapi.sse import ServerSentEvent,EventSourceResponse
import secrets
from app.llm.chat_model import get_chat_model
from app.rag.retriver_pipeline import retrieve_documents
from app.rag.augmentation import build_context,build_prompt,built_history



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

    history_context = built_history(history)



    yield ServerSentEvent(
        event="status",
        data={
            "status":"processing"
        }
    )

    final_response=""

    #RAG RELATED WORK START HERE

    retrieved_documents = retrieve_documents(
        query=message,
        user_id=str(user_id),
    )

    context = build_context(
        retrieved_documents
    )

    prompt = build_prompt(
        query=message,
        context=context,
        history=history_context
    )

    llm = get_chat_model()

    # print(prompt)

    # response = await llm.ainvoke(prompt)

    # if isinstance(response.content, str):
    #     assistant_response = response.content
    # else:
    #     assistant_response = "".join(
    #     block["text"]
    #     for block in response.content
    #     if isinstance(block, dict) and block.get("type") == "text"
    # )

    # print("\n========== LLM RESPONSE ==========")
    # print(assistant_response)
    # print("==================================\n")




    ## RAG RELATED WORK END HERE 

    async for chunk in  llm.astream(prompt):
        if(not chunk.content):
            continue
        if isinstance(chunk.content, str):
         token = chunk.content

        else:
         token = "".join(
            block.get("text", "")
            for block in chunk.content
            if isinstance(block, dict)
        )

         if not token:
            continue

        final_response+=token

        yield ServerSentEvent(
            event="token",
            data=token
        )



    await create_message(user_id=user_id,thread_id=thread_id,content=final_response,role="assistant")

    yield ServerSentEvent(
        event="done",
        data={
            "status":"completed"
        }
    )

        


    
