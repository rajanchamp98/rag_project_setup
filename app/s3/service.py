from app.s3.client import get_s3_client
from app.core.config import settings
from typing import BinaryIO



def upload_file(
        fileObject:BinaryIO,
        bucket_name:str,
        object_key:str
)->None:
    s3_client=get_s3_client()
    s3_client.upload_fileobj(
        fileObject,
        bucket_name,
        object_key,
        ExtraArgs={
            "ContentType": "application/pdf"
        }
    )


def download_file(
        bucket_name:str,
        object_key:str,
        fileobject:BinaryIO
        ):

        s3_client=get_s3_client()

        s3_client.download_fileobj(
              bucket_name,
              object_key,
              fileobject
        )

