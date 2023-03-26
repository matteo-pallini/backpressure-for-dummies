from fastapi import FastAPI
from fastapi import status, HTTPException
import logging
import asyncio
import time

app = FastAPI()
logging.basicConfig(level=logging.INFO)
sem = asyncio.Semaphore(4)


def _compute(value):
    return [str(_) for _ in range(value + 1_000_000)]

async def _async_io(value, time_needed=2):
    await asyncio.sleep(time_needed)


def _io(value, time_needed=2):
    time.sleep(time_needed)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/blocking_endpoint/{value}")
async def blocking_endpoint(value: int):
    logging.info(f"got request for value {value}")
    start = time.time()
    _ = _compute(value) # preprocessing state
    _io(value)
    _ = _compute(value) # postprocessing state
    logging.info(f"completed request {value} - {time.time() - start}")
    return {"message": value ** 2}


@app.get("/async_endpoint_without_backpressure/{value}")
async def async_endpoint_without_backpressure(value: int):
    logging.info(f"got request for value {value}")
    start = time.time()
    _ = _compute(value) # preprocessing state
    await _async_io(value)
    _ = _compute(value) # postprocessing state
    logging.info(f"completed request {value} - {time.time() - start}")
    return {"message": value ** 2}


@app.get("/async_endpoint_with_backpressure/{value}")
async def async_endpoint_with_backpressure(value: int):
    global sem
    if sem.locked():
        print(f"Semaphore blocked {value}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="server overloaded"
                            )
    await sem.acquire()
    try:
        start = time.time()
        logging.info(f"got request for value {value}")
        _ = _compute(value) # preprocessing state
        await _async_io(value)
        _ = _compute(value) # postprocessing state
        logging.info(f"completed request {value} - {time.time() - start}")
        return {"message": value ** 2}
    finally:
        sem.release()
