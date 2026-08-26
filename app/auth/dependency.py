from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException,Depends
from app.auth.security import decode_token
from app.users.repository import get_user_by_id


security=HTTPBearer()



async def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthroize to access endpoint "
        )

    try:
        payload=decode_token(token,"access")

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token"
        )

    user_id=payload.get("sub")
    

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    user=await get_user_by_id(user_id)



    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not user.get("is_active",False):
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )

    return user

    