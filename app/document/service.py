from uuid import uuid4
from app.document.repository import create_document
from app.core.config import settings
from app.s3.service import upload_file
from app.document.schema import DocumentUploadResponse,DocumentStatus
from datetime import datetime,timezone



async def upload_document(file,user_id:str)->DocumentUploadResponse:
    document_id=str(uuid4())

    object_key = (
    f"documents/"
    f"{user_id}/"
    f"{document_id}/" 
    f"{file.filename}"
    )

    upload_file(
        fileObject=file.file,
        bucket_name=settings.S3_BUCKET_NAME,
        object_key=object_key
    )
    now=datetime.now(timezone.utc)
    document={
        "document_id":document_id,
        "user_id":user_id,
        "filename":file.filename,
        "s3_key":object_key,
        "content_type":file.content_type,
        "status":DocumentStatus.PROCESSING.value,
        "created_at":now,
        "updated_at":now
    }


    await create_document(document)

    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        status=DocumentStatus.PROCESSING.value


    )



