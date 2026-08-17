from pathlib import Path

from app.rag.loader import doc_loader
from app.rag.splitter import chunking
from app.rag.vector_store import get_vector_store


def ingest_document(file_path:Path)->dict:
     print(f"Starting ingestion: {file_path}")

     # 1. Load
     documents = doc_loader(file_path)

     print(f"Loaded pages: {len(documents)}")

     # 2. Chunk
     chunks = chunking(documents)

     print(f"Created chunks: {len(chunks)}")

     # 3 embedding + vector store
     vector_store=get_vector_store()
     vector_store.add_documents(chunks)

     print("Documents stored in Chroma")

     return {
        "file": str(file_path),
        "pages": len(documents),
        "chunks": len(chunks),
        "status": "completed",
    }

     



