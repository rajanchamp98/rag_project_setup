from app.db.database import mongo_db
from bson import ObjectId


user_collection=mongo_db["users"]

async def create_user(user_data:dict):
    result = await user_collection.insert_one(user_data)
    return result.inserted_id

async def get_user(email_id:str):
    result=await user_collection.find_one({
        "email":email_id
    })
    return result

async def get_user_by_id(user_id:str):
    result=await user_collection.find_one(
        {
            "_id":ObjectId(user_id)
        }
    )
    return result