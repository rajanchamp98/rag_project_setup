from rq import Worker
from app.queue.config import redis_connection,rag_queue


def start_worker()-> None:
    worker=Worker(
        queues=[rag_queue],
        connection=redis_connection
    )

    worker.work()

if __name__ == "__main__":
    start_worker()

