import hashlib
import secrets
import jwt
from datetime import datetime,timedelta,timezone
from app.core.config import settings
from uuid import uuid4



def create_access_token(user_id:str)->str:
    now = datetime.now(timezone.utc)

    payload={
        "sub":user_id,
        "type":"access",
        "iat":now,
        "exp":now + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRY))
    }

    return jwt.encode(
        payload,
        settings.ACCESS_TOKEN_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(user_id:str)->str:
    now = datetime.now(timezone.utc)
    
    payload={
            "sub":user_id,
            "type":"refresh",
            "jti":str(uuid4()),
            "iat":now,
            "exp":now + timedelta(days=int(settings.REFRESH_TOKEN_EXPIRY))
        }
    
    return jwt.encode(
            payload,
            settings.REFRESH_TOKEN_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )


def decode_token(token:str,token_type:str)->dict:
    if token_type == "access":
        secret=settings.ACCESS_TOKEN_SECRET
    elif token_type == "refresh":
        secret=settings.REFRESH_TOKEN_SECRET
    else:
        raise ValueError("Invalid token type")

    payload=jwt.decode(
        token,
        secret,
        algorithms=settings.JWT_ALGORITHM
    )

    if payload.get("type") != token_type:
        raise ValueError("Invalid Token type")

    return payload
    