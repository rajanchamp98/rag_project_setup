from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME:str
    ENVIRONMENT:str
    REDIS_URL:str
    CHROMA_DIR:str

    AWS_REGION:str="us-east-1"
    AWS_ACCESS_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str
    MONGODB_URI:str
    MONGODB_DATABASE:str
    

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings=Settings()