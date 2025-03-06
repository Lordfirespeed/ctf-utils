from typing import SupportsInt


def byte_length(value: SupportsInt) -> int:
    value = int(value)
    assert value > 0
    # 2^3 = 8, so right-shifting 3 times is equivalent to dividing by 8
    return ((value.bit_length() - 1) >> 3) + 1


def signed_byte_length(value: SupportsInt) -> int:
    value = int(value)
    # 2^3 = 8, so right-shifting 3 times is equivalent to dividing by 8
    return (value.bit_length() >> 3) + 1


__all__ = ("byte_length", "signed_byte_length",)
