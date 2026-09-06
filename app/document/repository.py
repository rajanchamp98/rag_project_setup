from app.db.database import mongo_db
from bson import ObjectId
from datetime import datetime,timezone

document_collection=mongo_db["documents"]



async def update_document(
    document_id: str,
    user_id: str,
    payload: dict
):
    
    result = await document_collection.find_one_and_update(
        {
            "document_id": document_id,
            "user_id": user_id,
        },
        {
            "$set": {
                **payload,
                "updated_at": datetime.now(timezone.utc),
            }
        },
        return_document=True,
    )

    return result