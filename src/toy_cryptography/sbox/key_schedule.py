from typing import Generator

from bitarray import bitarray

from extras.binary_extras import circular_left_shift


def sbox_key_schedule(key: bitarray) -> Generator[bitarray]:
    assert len(key) == 64

    for _ in range(6):
        key = circular_left_shift(key, 33)
        yield key[0:32]


__all__ = ("sbox_key_schedule",)
