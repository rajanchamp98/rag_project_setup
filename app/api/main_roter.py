from fastapi import APIRouter
from app.auth.router import router as auth_route
from app.users.router import router as user_route
from app.chat.router import router as chat_route
from app.document.router import router as document_route

router=APIRouter(prefix="/api/v1")


router.include_router(auth_route)
router.include_router(user_route)
router.include_router(chat_route)
router.include_router(document_route)


