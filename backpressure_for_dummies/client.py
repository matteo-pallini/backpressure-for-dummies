import asyncio
import aiohttp
import logging
import time

logging.basicConfig(level=logging.INFO)

async def get(session: aiohttp.ClientSession, value: int, url: str, retries: int = 10):
    while retries>0:
        url_value = f"{url}/{value}"
        logging.info(f"requesting {url_value}")
        resp = await session.request("GET", url=url_value)
        if resp.status == 429:
            retries -= 1
            logging.info(f"Got a 429 for {url_value} - retrying")
            await asyncio.sleep(0.3)
            continue
        else:
            logging.info(f"completed request for {value}")
            break
    data = await resp.json()
    return data


async def run_many_requests_concurrently(url:str, number: int):
    async with aiohttp.ClientSession() as session:
        tasks = [get(session=session, url=url,value=i) for i in range(number)]
        vals = await asyncio.gather(*tasks, return_exceptions=True)
        return vals

async def query_endpoint(endpoint_name: str, number: int):
    logging.info(f"Start querying the {endpoint_name}")
    URL = f"http://127.0.0.1:8080/{endpoint_name}"
    start = time.time()
    await run_many_requests_concurrently(url=URL, number=number)
    end = time.time()
    logging.info(f"time spent: {end-start}\n\n\n")


if __name__ == "__main__":
    number = 12
    asyncio.run(query_endpoint(endpoint_name="async_endpoint_with_backpressure", number=number))
    asyncio.run(query_endpoint(endpoint_name="sync_endpoint", number=number))
    asyncio.run(query_endpoint(endpoint_name="async_endpoint_with_backpressure", number=number))
