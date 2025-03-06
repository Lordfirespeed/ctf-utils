import asyncio
from typing import Awaitable, Callable, Iterable

from .state import has_succeeded


async def race_predicate[T](predicate: Callable[[asyncio.Future[T]], bool], awaitables: Iterable[Awaitable[T]]) -> T:
    futures = {asyncio.ensure_future(awaitable) for awaitable in set(awaitables)}
    async for future in asyncio.as_completed(futures):
        if not predicate(future):
            continue

        result = await future
        break
    else:
        raise BaseExceptionGroup(
            'no completed future was satisfactory in asyncio_extras.race_predicate',
            [task.exception() for task in futures]
        )

    for future in futures:
        future.cancel()

    await asyncio.gather(*futures, return_exceptions=True)  # exceptions are silenced
    return result


async def race[T](awaitables: Iterable[Awaitable[T]]) -> T:
    return await race_predicate(lambda _: True, awaitables)


async def race_success[T](awaitables: Iterable[Awaitable[T]]) -> T:
    return await race_predicate(has_succeeded, awaitables)


__all__ = ("race", "race_predicate", "race_success",)
