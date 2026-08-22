from fastapi import APIRouter,Response,Cookie,HTTPException
from app.auth.schemas import TokenResponse,LoginRequest
from app.auth.service import login_user,refresh_access_token,logout_user
from app.users.service import register_user
from app.users.schemas import UserCreate,UserResponse
from app.core.config import settings



router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register",response_model=UserResponse)
async def register(user_data:UserCreate):
   return await register_user(name=user_data.name,email=user_data.email,password=user_data.password)
  

@router.post("/login",response_model=TokenResponse)
async def login(user_data:LoginRequest,response:Response):
    result= await login_user(email=user_data.email,password=user_data.password)


    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=settings.ENVIRONMENT == 'production',
        samesite="lax",
        max_age=60*60*24*7,
        path="/auth"

    )
    return {
        "access_token":result["access_token"],
        "token_type":"bearer"
    }

@router.post("/refresh",response_model=TokenResponse)
async def refresh(response:Response,refresh_token:str | None=Cookie(default=None)):
    print(refresh_token)
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="token missing"
        )

    result=await refresh_access_token(refresh_token)

    response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=settings.ENVIRONMENT == 'production',
            samesite="lax",
            max_age=60*60*24*7,
            path="/auth"
    
        )
    return {
            "access_token":result["access_token"],
            "token_type":"bearer"
        }
@router.post("/logout")
async def logout(response:Response,refresh_token:str | None=Cookie(default=None)):
    if refresh_token:
        await logout_user(refresh_token=refresh_token)

    response.delete_cookie(
        key="refresh_token",
        path="/auth"
    )

    return {
        "message":"logout sucessfull"
    }




