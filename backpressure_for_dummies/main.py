from fastapi import FastAPI
import logging
import time

app = FastAPI()
logging.basicConfig(level=logging.INFO)
counter = 0

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/friendly_endpoint")
async def friendly_endpoint():
    global counter
    counter += 1
    logging.info(f"got request {counter}")
    time.sleep(2)
    logging.info(f"completed request {counter}")
    return {"message": "What a time to be alive"}
