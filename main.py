from os import system
from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/v1/start")
async def start():

    system(f"cd /python/Savya/Email_Verification && ./Start.sh")
    return {"Message": "Completed", "status": 200}

if __name__ == "__main__":

    run("main:app", host="0.0.0.0", port=8989)