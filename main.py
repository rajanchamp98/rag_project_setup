from app.app import app
import uvicorn


def main():
    uvicorn.run(app,port=8080,host="0.0.0.0")

main()