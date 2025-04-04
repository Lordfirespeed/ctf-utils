from typing import Sequence

from utils.typedefs import SupportsBool


def binlify(value: int, bit_length: int) -> tuple[bool, ...]:
    return tuple(bool(value & (1 << i)) for i in reversed(range(0, bit_length)))


def unbinlify(value: Sequence[SupportsBool]) -> int:
    accumulator = 0
    for digit in value:
        accumulator += bool(digit)
        accumulator <<= 1
    accumulator >>= 1
    return accumulator


__all__ = ("binlify", "unbinlify",)
