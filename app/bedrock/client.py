import boto3
from app.core.config import settings


def get_reranker_client():
    return boto3.client(
        "bedrock-agent-runtime",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )