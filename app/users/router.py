from fastapi import APIRouter,Depends

from app.auth.dependency import get_current_user


router=APIRouter(
    prefix="/user",
    tags=["User Route"]
)


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    # print(current_user)
    
    return {
        "id":str(current_user["_id"]),
        "name":current_user["name"],
        "email":current_user["email"],
        "is_active":current_user["is_active"]
    }