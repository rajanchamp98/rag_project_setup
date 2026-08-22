import asyncio
from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError
from app.core.config import settings


mongo_client=AsyncMongoClient(
    settings.MONGODB_URI
)

mongo_db=mongo_client[
    settings.MONGODB_DATABASE
]


async def check_mongo_connection():
    try:
        await mongo_client.admin.command("ping")
        print("mongodb connected sucessfully")
        return True
    except PyMongoError as e:
        print("mongodb connection failed ")
        return False

if __name__ =="__main__":
        print(asyncio.run(check_mongo_connection()))


