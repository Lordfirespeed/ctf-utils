from contextlib import suppress
from dataclasses import dataclass
from io import TextIOWrapper
from itertools import islice
from pathlib import Path
from typing import Iterator, Iterable, Self

from yarl import URL

from utils.cached_download import cached_download


word_lists_dirname = Path("data")


@dataclass
class WordListMetadata:
    slug: str
    url: URL
    filename: str

    @property
    def file_destination(self):
        return word_lists_dirname / self.filename


word_lists_metadata_list = [
    WordListMetadata(
        slug = "bip-39",
        url = URL("https://raw.githubusercontent.com/bitcoin/bips/refs/heads/master/bip-0039/english.txt"),
        filename = "bip-39-en.txt",
    ),
    WordListMetadata(
        slug = "english-words",
        url = URL("https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt"),
        filename = "english-words.txt"
    )
]
word_lists_metadata_dict: dict[str, WordListMetadata] = dict(((meta.slug, meta) for meta in word_lists_metadata_list))


class WordList(Iterable[str]):
    def __init__(self, meta: WordListMetadata):
        self.meta = meta
        self._file_handle: TextIOWrapper | None = None
        self._length: int | None = None
        self._open = False

    async def __aenter__(self) -> Self:
        filename = await cached_download(
            self.meta.url,
            self.meta.file_destination,
        )
        self._file_handle = open(filename, "r")
        self._open = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._file_handle.close()
        self._open = False

    def __iter__(self) -> Iterator[str]:
        self._file_handle.seek(0)
        for line in iter(self._file_handle.readline, ""):  # https://stackoverflow.com/a/73565535/11045433
            cursor_position = self._file_handle.tell()
            yield line.strip()
            self._file_handle.seek(cursor_position)

    def __getitem__(self, item: int) -> str:
        """Note time complexity here is O(n) as this effectively seeks from start of file"""
        self._file_handle.seek(0)
        lines = islice(iter(self._file_handle.readline, ""), item, item+1)
        with suppress(StopIteration):
            return next(lines).strip()
        raise KeyError

    def __len__(self) -> int:
        if self._length is not None:
            return self._length
        count = 0
        self._file_handle.seek(0)
        for _ in iter(self._file_handle.readline, ""):
            count += 1
        self._length = count
        return self._length


def word_list(slug: str) -> WordList:
    meta = word_lists_metadata_dict.get(slug)
    if meta is None:
        raise KeyError(f"Unrecognised word list {slug!r}")
    return WordList(meta)


__all__ = ("word_list", "WordList",)
