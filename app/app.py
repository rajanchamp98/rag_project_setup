from fastapi import FastAPI


app=FastAPI()


@app.get("/")
def helath():
    return {
        "message":"Serve is healthy"
    }