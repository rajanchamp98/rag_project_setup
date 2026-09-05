from app.db.database import mongo_db

document_collection=mongo_db["documents"]



async def create_document(document:dict):
   await  document_collection.insert_one(document)