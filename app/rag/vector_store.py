from langchain_chroma import Chroma
from app.core.config import settings
from app.llm.embedding_model import get_embedding_model



def get_vector_store()->Chroma:
    embedding_model=get_embedding_model()

    vector_store=Chroma(
        collection_name="document",
        embedding_function=embedding_model,
        persist_directory=settings.CHROMA_DIR

    )

    return vector_store


