import asyncio
from typing import Awaitable, Iterable


async def race_success[T](awaitables: Iterable[Awaitable[T]]) -> T:
    futures: set[asyncio.Future[T]] = set()
    async for future in asyncio.as_completed(awaitables):
        futures.add(future)
        if future.cancelled() or future.exception() is not None:
            continue

        result = await future
        break
    else:
        raise BaseExceptionGroup(
            'no task completed successfully in asyncio_extras.race_success',
            [task.exception() for task in futures]
        )

    for future in futures:
        future.cancel()

    await asyncio.gather(*futures, return_exceptions=True)  # exceptions are silenced
    return result


__all__ = ("race_success",)
