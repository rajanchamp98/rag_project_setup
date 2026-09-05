from app.db.database import mongo_db
from datetime import datetime,timezone
from bson import ObjectId

thread_collection=mongo_db["threads"]
message_collection=mongo_db["messages"]



async def create_thread(thread_id:str,user_id:str,title:str)->str:
    now=datetime.now(timezone.utc)
    result=await thread_collection.insert_one({
        "thread_id":thread_id,
        "user_id":ObjectId(user_id),
        "title":title,
        "created_at":now,
        "updated_at":now
    })
    return result.inserted_id


async def get_thread(thread_id:str,user_id:str)->dict:
    result=await thread_collection.find_one({
        "thread_id":thread_id,
        "user_id":ObjectId(user_id)

    })
    return result


async def create_message(user_id:str,thread_id:str,content:str,role:str):

    now=datetime.now(timezone.utc)
    result=await message_collection.insert_one(
        {
            "thread_id":thread_id,
            "user_id":ObjectId(user_id),
            "role":role,
            "content":content,
            "created_at":now

        }   
    )
    await thread_collection.update_one({
        "thread_id":thread_id,
        "user_id":ObjectId(user_id)
    },
    {
        "$set":{
            "updated_at":now
        }
    }
    )

    return result.inserted_id


async def get_chat_history(thread_id:str,user_id:str,limit:int=20):
    cursor=(message_collection.find({
        "thread_id":thread_id,
        "user_id":user_id,
        
    }).sort("created_at",-1).limit(limit))

    messages=await cursor.to_list(length=limit)
    messages.reverse()
    return messages
