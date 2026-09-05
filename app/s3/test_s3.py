from app.s3.service import upload_file
from app.core.config import settings


file_path = "/home/rajan/PROJECT_RAG/storage/upload/nodeJS.pdf"

object_key = "/home/rajan/PROJECT_RAG/storage/upload/nodeJS.pdf"

with open(file_path, "rb") as file:
    upload_file(
        fileObject=file,
        bucket_name="ragprojectproduction-118774114185-us-east-1-an",
        object_key=object_key,
    )

print("Upload successful")