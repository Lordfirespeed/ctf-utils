from contextlib import AsyncExitStack
from pathlib import Path

import aiohttp
from yarl import URL

from definitions import project_cache_dirname

downloads_cache_dirname = Path(project_cache_dirname, "downloads")
chunk_size = 4096


async def cached_download(url: URL, relative_path: Path = None) -> Path:
    if relative_path is None:
        relative_path = Path(url.name)
    destination = downloads_cache_dirname.joinpath(relative_path)

    if destination.is_relative_to(downloads_cache_dirname):
        destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        return destination

    async with AsyncExitStack() as stack:
        session = await stack.enter_async_context(aiohttp.ClientSession())
        response = await stack.enter_async_context(session.get(url))
        destination_handle = stack.enter_context(open(destination, "wb"))

        async for chunk in response.content.iter_chunked(chunk_size):
            destination_handle.write(chunk)

    return destination


__all__ = ("cached_download",)
