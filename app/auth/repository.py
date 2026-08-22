from app.db.database import mongo_db
from datetime import datetime,timezone


refresh_token_collection=mongo_db["refresh_tokens"]


async def create_refresh_session(data:dict):
    result=await refresh_token_collection.insert_one(data)
    return result.inserted_id

async def get_refresh_session(jti:str):
    return await refresh_token_collection.find_one({
        "jti":jti,
        "revoked":False,
        "expires_at": {
            "$gt": datetime.now(timezone.utc)
        }
            })

async def revoke_refresh_session(jti:str):
    result=await refresh_token_collection.update_one(
        {
            "jti":jti
        },
        {
        "$set":{
            "revoked":True
        }
        }
    )
    return result.modified_count