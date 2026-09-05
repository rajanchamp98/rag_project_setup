from fastapi import FastAPI
from app.core.exception import validation_exception_handling
from fastapi.exceptions import RequestValidationError
from app.api.main_roter import router as main_router



app=FastAPI()

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handling
)
app.include_router(main_router)



@app.get("/api/v1")
def helath():
    return {
        "message":"Serve is healthy"
    }