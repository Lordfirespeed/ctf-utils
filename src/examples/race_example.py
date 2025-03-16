import asyncio

from extras import asyncio_extras


async def wait(t):
    await asyncio.sleep(t)
    return t


async def raising_wait(t):
    await asyncio.sleep(t)
    raise TimeoutError("You waited for too long, pal")


time_scale = 0.5


async def main():
    futures = {
        wait(time_scale * 3),
        raising_wait(time_scale * 2),
        wait(time_scale * 1),
    }

    result = await asyncio_extras.race_success(futures)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
