from fastapi import APIRouter,Query
from app.queue.config import chat_queue
from app.services.chat_service import process_chat

router=APIRouter(prefix="/api/v1",
                 tags=["chat Routes"])

@router.get("/chat")
def get_chat(message=Query(...,description="will accept message")):
    job=chat_queue.enqueue(
        process_chat,
        message
    )

    return {
        "status":"queued",
        "job_id":job.id
    }

@router.post("/result")
def get_result(job_id:str=Query(...,description="provide job id to get result")):
    job=chat_queue.fetch_job(job_id=job_id)
    result=job.return_value()
    return {
        "status":"retrived",
        "result":result
    }


