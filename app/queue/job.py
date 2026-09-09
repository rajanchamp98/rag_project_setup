import asyncio
from app.rag.pipeline import ingest_document
from app.document.repository import update_document
from app.document.schema import DocumentStatus

def process_ingestion_job(s3_key:str,document_id:str,user_id:str):

    try:
        result=ingest_document(
            s3_key=s3_key,
            document_id=document_id,
            user_id=user_id)



        asyncio.run(
                update_document(
                   document_id=document_id,
                    user_id=user_id,
                    payload={
                        "status":DocumentStatus.COMPLETED.value,
                        "chunks":result["chunks"],
                        "pages":result["pages"]
                    }
                )
            )

        return result

        

        
    except Exception as e:
        asyncio.run(
            update_document(
                document_id=document_id,
                user_id=user_id,
                payload={
                "status":DocumentStatus.FAILED.value,
                "errors":str(e)

            }
            )

            )
        raise
        