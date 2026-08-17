from app.core.config import settings
from rq import Queue
from redis import Redis


#valkey connection

redis_connection=Redis.from_url(
    url=settings.REDIS_URL,
)


"""RQ queue for RAG ingetion"""

# for document queue
rag_queue=Queue(
    name="rag_queue",
    connection=redis_connection
)

# for chat queue
chat_queue=Queue(
    name="chat_queue",
    connection=redis_connection
)

