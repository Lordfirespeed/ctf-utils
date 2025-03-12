"""
See
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands
"""
from typing import ClassVar, Self

from .constants import *


class StyleEscapeBuilder:
    terminator: ClassVar[bytes] = b"m"
    """the terminator for all style-modifying escape codes."""

    def __init__(self):
        self._buffer = bytearray(8)
        self._cursor = 0
        self._argument_count = 0
        self._append_raw(control_sequence_introducer)

    def _append_raw(self, value: bytes) -> None:
        previous_cursor = self._cursor
        self._cursor += len(value)
        self._buffer[previous_cursor:self._cursor] = value

    def _character_at(self, index: int) -> bytes:
        return self._buffer[index].to_bytes(1)

    def _content(self) -> bytearray:
        return self._buffer[:self._cursor]

    def argue(self, ordinal: int) -> Self:
        assert ordinal >= 0

        if self._argument_count > 0:
            self._append_raw(delimiter)

        self._argument_count += 1

        if ordinal == 0:
            # missing numbers are treated as zero, so we can miss zeroes
            return self

        self._append_raw(str(ordinal).encode("ascii"))
        return self

    def finalize(self) -> str:
        self._append_raw(self.terminator)
        return self._content().decode("ascii")

    @classmethod
    def quick(cls, ordinal: int) -> str:
        return cls().argue(ordinal).finalize()


__all__ = ("StyleEscapeBuilder",)
