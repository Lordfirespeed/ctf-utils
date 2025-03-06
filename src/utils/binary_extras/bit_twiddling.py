from typing import (
    Literal,
    SupportsInt,
    overload,
)

from numpy import integer

from utils.types import BytesLike


def last_set_bit_index(binary: SupportsInt | BytesLike) -> int | Literal[-1]:
    """
    Compute the index (from the right) of the right-most '1' bit in 'binary'.
    For integer powers of 2, this computes log_2(binary).
    If there exists no index (because the input contains no set bits), returns -1.
    """
    if isinstance(binary, SupportsInt):
        binary = int(binary)
    if type(binary) is not int:
        binary = int.from_bytes(binary, byteorder="big")

    if binary == 0:
        return -1

    # bit-hack to create a bit-mask of exactly 1 '1' bit, in the position of the right-most '1' bit from 'binary'
    highest_bit_mask = binary & -binary

    return highest_bit_mask.bit_length() - 1


def first_set_bit_index(binary: SupportsInt | BytesLike) -> int | Literal[-1]:
    """
    Compute the index (from the right) of the left-most '1' bit in 'binary'.
    If there exists no index (because the input contains no set bits), returns -1.
    """
    if isinstance(binary, SupportsInt):
        binary = int(binary)
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
    "last_set_bit_index",
    "first_set_bit_index",
    "circular_left_shift",
    "circular_right_shift",
)
