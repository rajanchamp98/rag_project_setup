from langchain_aws import ChatBedrockConverse
from app.core.config import settings


def get_chat_model()->ChatBedrockConverse:
    return ChatBedrockConverse(
    model="openai.gpt-oss-safeguard-120b",  
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    temperature=0
    )
