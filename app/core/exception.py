from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handling(request:Request,exc:RequestValidationError):
    message=[]

    for val in exc.errors():
        message.append(val.get("msg","Invalid"))

    return JSONResponse(
        status_code=422,
        content={
            "sucess":False,
            "message":message,
            "errors":exc.errors()
        }
    )

