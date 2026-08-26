from fastapi import FastAPI
from app.api.chat_route import router as chat_router
from app.auth.router import router as auth_route
from app.core.exception import validation_exception_handling
from fastapi.exceptions import RequestValidationError
from app.users.router import router as user_route


app=FastAPI()

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handling
)
app.include_router(auth_route)
app.include_router(chat_router)
app.include_router(user_route)


@app.get("/")
def helath():
    return {
        "message":"Serve is healthy"
    }