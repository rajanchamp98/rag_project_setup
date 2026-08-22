from app.users.repository import create_user,get_user,get_user_by_id
from fastapi import HTTPException
from app.core.security import hash_passowrd
from datetime import datetime,timezone


async def register_user(name:str,email:str,password:str):

    user_exist=await get_user(email_id=email)
    if user_exist:
        raise HTTPException(
            status_code=409,
            detail="user already exist"
        )
    now=datetime.now(timezone.utc)

    user_data={
        "name":name,
        "email":email,
        "password_hash":hash_passowrd(password),
        "is_active":True,
        "created_at":now,
        "updated_at":now
    }

    id=await create_user(user_data=user_data)
    if not id:
        raise HTTPException(
            status_code=500,
            detail="User creation failed "
        )

    return {
            "id":str(id),
            "name":name,
            "email":email,
            "is_active":True
        }








