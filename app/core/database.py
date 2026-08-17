from pymongo import MongoClient
from app.core.config import settings


mongo_client=MongoClient(
    settings.MONGODB_URI
)

mongo_db=mongo_client[
    settings.MONGODB_DATABASE
]