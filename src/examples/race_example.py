import asyncio

from utils import asyncio_extras


async def wait(t):
    await asyncio.sleep(t)
    return t


async def raising_wait(t):
    await asyncio.sleep(t)
    raise TimeoutError("You waited for too long, pal")


async def main():
    futures = {
        wait(0.2),
        raising_wait(1),
        wait(2),
    }

    result = await asyncio_extras.race_success(futures)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
