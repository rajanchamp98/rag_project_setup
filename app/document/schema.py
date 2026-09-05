from pydantic import BaseModel
from enum import Enum


class DocumentStatus(str,Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentUploadResponse(BaseModel):
    document_id:str
    filename:str
    status:DocumentStatus
