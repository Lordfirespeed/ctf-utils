from typing import (
    Iterable,
    SupportsBytes,
    SupportsIndex,
)

type BytesLike = Iterable[SupportsIndex] | SupportsBytes

__all__ = ("BytesLike",)
