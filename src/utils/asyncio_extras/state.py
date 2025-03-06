import asyncio


def has_succeeded(future: asyncio.Future) -> bool:
    if not future.done():
        raise ValueError("future is incomplete; its success is indeterminable")
    return (not future.cancelled()) and (future.exception() is None)

__all__ = ("has_succeeded",)
