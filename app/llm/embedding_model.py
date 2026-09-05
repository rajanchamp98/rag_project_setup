from langchain_aws import BedrockEmbeddings
from app.core.config import settings



def get_embedding_model() -> BedrockEmbeddings:
    return BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

