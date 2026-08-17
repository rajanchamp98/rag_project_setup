from app.rag.vector_store import get_vector_store
from langchain_core.vectorstores import VectorStoreRetriever


def get_retrivers()->VectorStoreRetriever:
    vector_store=get_vector_store()
    retriver=vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k":5,
        },
          )

    return retriver