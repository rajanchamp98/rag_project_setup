from app.db.database import mongo_db
from datetime import datetime,timezone

thread_collection=mongo_db["threads"]
message_collection=mongo_db["messages"]



async def create_thread(thread_id:str,user_id:str,title:str)->str:
    now=datetime.now(timezone.utc)
    result=await thread_collection.insert_one({
        "thread_id":thread_id,
        "user_id":user_id,
        "title":title,
        "created_at":now,
        "updated_at":now
    })
    return result.inserted_id


async def get_thread(thread_id:str,user_id:str)->dict:
    result=await thread_collection.find_one({
        "thread_id":thread_id,
        "user_id":user_id

    })
    return result


async def create_message(user_id:str,thread_id:str,content:str,role:str):
    await message_collection.insert_one(
        {
            
        }
    )

