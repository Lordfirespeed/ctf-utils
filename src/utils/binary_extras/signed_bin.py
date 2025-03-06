from typing import SupportsInt

from .byte_length import signed_byte_length


def signed_bin(value: SupportsInt, binary_byte_length: int | None = None) -> str:
    value = int(value)
    if binary_byte_length is None:
        binary_byte_length = signed_byte_length(value)
    binary_bit_length = binary_byte_length * 8
    signed_value_bytes = value.to_bytes(length=binary_byte_length, signed=True)
    unsigned_value_integer = int.from_bytes(signed_value_bytes)
    return f"{unsigned_value_integer:0{binary_bit_length}b}"


__all__ = ("signed_bin",)
