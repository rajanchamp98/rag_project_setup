from fastapi import APIRouter,Depends,File,HTTPException,UploadFile,status
from app.document.schema import DocumentUploadResponse
from app.document.service import upload_document
from app.auth.dependency import get_current_user


router=APIRouter(
    prefix="/document",
    tags=["upload document"]
)



@router.post("/upload",response_model=DocumentUploadResponse)
async def upload_route(
    file:UploadFile=File(...),
    current_user=Depends(get_current_user)
):

    if (file.content_type not in  ["application/pdf","application/octet-stream"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pdf file is accepted!"
        )
    user_id=current_user["_id"]

    return await upload_document(
        file=file,
        user_id=user_id
    )