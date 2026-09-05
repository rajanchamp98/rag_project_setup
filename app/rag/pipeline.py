import os
from pathlib import Path
from tempfile import NamedTemporaryFile


from app.rag.loader import doc_loader
from app.rag.splitter import chunking
from app.rag.index_chunks import index_chunk
from app.core.config import settings
from app.s3.service import download_file


def ingest_document(
        s3_key:str,
        document_id:str,
        user_id:str
)-> dict:

    tmp_path=None    
    try:
        temp_dir= Path(settings.TEMP_INGESTION_DOC)
        temp_dir.mkdir(parents=True,exist_ok=True)

        with NamedTemporaryFile(
            suffix=".pdf",
            dir=temp_dir,
            delete=False,

        ) as temp_file:
            temp_path=Path(temp_file.name)

            download_file(
            bucket_name=settings.S3_BUCKET_NAME,
            object_key=s3_key,
            fileobject=temp_file
            )

        documents=doc_loader(temp_path)

        chunks=chunking(documents)


        index_chunk(
            chunks=chunks,
            document_id=document_id,
            user_id=user_id
            )

        return {
            "document_id":document_id,
            "pages":len(documents),
            "chunks":len(chunks),
            "status":"completed"
        }
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()
            
