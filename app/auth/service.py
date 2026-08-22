from app.users.repository import get_user
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime,timezone
from app.auth.repository import create_refresh_session,get_refresh_session,revoke_refresh_session



from app.auth.security import create_refresh_token,create_access_token,decode_token
from app.core.security import verify_password
from app.core.config import settings



async def login_user(email:str,password:str)->dict:

    user=await get_user(email_id=email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user or password"
        )

    is_password_valid =verify_password(password,user["password_hash"])    
    if not is_password_valid:
        raise HTTPException(
            status_code=401,
            detail="invalid email or password"
            )                  

    if not user.get("is_active",False):
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    user_id=str(user["_id"])

    # creating access token here 

    access_token=create_access_token(user_id)

    # creating refresh token 

    refresh_token=create_refresh_token(user_id)

    #decoding refresh token to get jit and exp

    refresh_payload=decode_token(refresh_token,"refresh")

    jti=refresh_payload["jti"]
    expires_at=datetime.fromtimestamp(
        refresh_payload["exp"],
        tz=timezone.utc
    )

    await create_refresh_session({
        "user_id": user["_id"],
        "jti": jti,
        "expires_at": expires_at,
        "revoked": False,
        "created_at": datetime.now(timezone.utc)
    }
    
    )



    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }


async def refresh_access_token(refresh_token:str):
    try:
        # decoding refresh token
        payload=decode_token(refresh_token,"refresh")
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    user_id=payload.get("sub")
    jti=payload.get("jti")

    if not user_id or not jti:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh Token"
        )

    session=await get_refresh_session(jti)
    if not session:
        raise HTTPException(
            status_code=401,
            detail="refresh token is invalid or revoked"
        )

    modified=await revoke_refresh_session(jti)

    if modified==0:
        raise HTTPException(
            status_code=401,
            detail="refresh token is alredy revoked"
        )

    new_access_token=create_access_token(user_id)
    new_refresh_token=create_refresh_token(user_id)

    new_decode_payload=decode_token(new_refresh_token,"refresh")
    new_jti=new_decode_payload["jti"]
    new_expires_at=datetime.fromtimestamp(
        new_decode_payload["exp"],
        tz=timezone.utc
        )

    await create_refresh_session(
        {
            "user_id":ObjectId(user_id),
            "jti":new_jti,
            "expires_at":new_expires_at,
            "revoked":False,
             "created_at": datetime.now(timezone.utc)
        }
    )


    return {
        "access_token":new_access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer"
    }

async def logout_user(refresh_token:str):
    try:
        payload=decode_token(refresh_token,"refresh")

    except Exception:
        return

    jti=payload.get("jti")

    await revoke_refresh_session(jti)

    return



