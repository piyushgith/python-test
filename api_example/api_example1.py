import asyncio
from random import random
from time import perf_counter

import aiohttp


semaphore = asyncio.Semaphore(10)


async def make_request(async_session: aiohttp.ClientSession, url: str):
    # Semaphore for limiting concurrent requests to 8
    async with semaphore:
        # Asynchronous GET request
        async with async_session.get(url=url) as _response:
            # avoid overpowering the URL right away by having this happen first
            await asyncio.sleep(random())

            # Print first letter of domain, so we know what is requested.
            if "q" in url:
                print("Q", flush=True, sep="", end="")
            else:
                print("B", flush=True, sep="", end="")


async def makes_all_requests(urls: list[str]):
    # Stores all tasks that will later be used on `asyncio.gather`
    async with aiohttp.ClientSession() as async_session:
        tasks = []
        for url in urls:
            # Creates asyncio.Task that will return a future
            task = asyncio.create_task(
                coro=make_request(
                    async_session=async_session,
                    url=url,
                )
            )

            tasks.append(task)

        # Tasks are ran with asyncio.gather
        # By setting `return_exceptions` to False, we will raise Exceptions within
        #   their asyncio task instance and everything will stop, by putting True, it
        #   will raise when `result()` is called on the future.
        
        await asyncio.gather(*tasks, return_exceptions=False)




if __name__ == "__main__":
    urls = [
        "https://books.toscrape.com/",
        "http://quotes.toscrape.com/",
    ] * 50

    print("---Starting---")

    start_time = perf_counter()

    asyncio.run(makes_all_requests(urls=urls))

    end_time = perf_counter()
    total_time = end_time - start_time
    print(f"\n---Finished in: {total_time:02f} seconds---")