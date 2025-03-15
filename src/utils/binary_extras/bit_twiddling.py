from operator import index
from typing import (
    Literal,
    # prefer SupportsIndex to SupportsInt as this prevents overleazous type coercion
    # e.g. index(float) -> TypeError
    SupportsIndex,
    overload,
)

from numpy import integer

from utils.typedefs import BytesLike


def count_trailing_zeroes(binary: SupportsIndex | BytesLike):
    return last_set_bit_index(binary)


def last_set_bit_index(binary: SupportsIndex | BytesLike) -> int | Literal[-1]:
    """
    Compute the index (from the right) of the right-most '1' bit in 'binary'.
    For integer powers of 2, this computes log_2(binary).
    If there exists no index (because the input contains no set bits), returns -1.
    """
    if isinstance(binary, SupportsIndex):
        binary = index(binary)
    if type(binary) is not int:
        binary = int.from_bytes(binary, byteorder="big")

    if binary == 0:
        return -1

    # bit-hack to create a bit-mask of exactly 1 '1' bit, in the position of the right-most '1' bit from 'binary'
    # https://stackoverflow.com/a/63552117/11045433
    highest_bit_mask = binary & -binary

    return highest_bit_mask.bit_length() - 1


def first_set_bit_index(binary: SupportsIndex | BytesLike) -> int | Literal[-1]:
    """
    Compute the index (from the right) of the left-most '1' bit in 'binary'.
    If there exists no index (because the input contains no set bits), returns -1.
    """
    if isinstance(binary, SupportsIndex):
        binary = index(binary)
    if type(binary) is not int:
        binary = int.from_bytes(binary, byteorder="big")

    if binary == 0:
        return -1

    return binary.bit_length() - 1


@overload
def circular_left_shift(value: integer, shift: int | integer, width: int | integer) -> integer: ...

@overload
def circular_left_shift(value: int, shift: int | integer, width: int | integer) -> int: ...

def circular_left_shift(value, shift, width):
    if isinstance(value, integer):
        return (value << shift) | (value >> (width - shift))
    # https://stackoverflow.com/a/63767548/11045433
    return ((value << shift) % (1 << width)) | (value >> (width - shift))


@overload
def circular_right_shift(value: integer, shift: int | integer, width: int | integer) -> integer: ...

@overload
def circular_right_shift(value: int, shift: int | integer, width: int | integer) -> int: ...

def circular_right_shift(value, shift, width):
    if isinstance(value, integer):
        return (value >> shift) | (value << (width - shift))
    return (value >> shift) | ((value << (width - shift)) % (1 << width))


__all__ = (
    "count_trailing_zeroes",
    "last_set_bit_index",
    "first_set_bit_index",
    "circular_left_shift",
    "circular_right_shift",
)
