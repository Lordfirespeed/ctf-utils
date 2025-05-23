import itertools
from typing import Generator

from bitarray import bitarray
from extras.binary_extras import binlify, unbinlify, circular_left_shift


pc1_c_schedule = (
    57, 49, 41, 33, 25, 17,  9,  1,
    58, 50, 42, 34, 26, 18, 10,  2,
    59, 51, 43, 35, 27, 19, 11,  3,
    60, 52, 44, 36,
)
pc1_d_schedule = (
    63, 55, 47, 39, 31, 23, 15,  7,
    62, 54, 46, 38, 30, 22, 14,  6,
    61, 53, 45, 37, 29, 21, 13,  5,
                    28, 20, 12,  4,
)
def permuted_choice_1(key: bitarray) -> tuple[bitarray, bitarray]:
    """given 64-bit DES key, returns C_0, D_0 (for computing round keys)"""
    assert len(key) == 64
    c_register = bitarray(key[i - 1] for i in pc1_c_schedule)
    d_register = bitarray(key[i - 1] for i in pc1_d_schedule)
    return c_register, d_register


pc2_schedule = (
    # first 24 bits from C register
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,

    # last 24 bits from D register
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
)
def permuted_choice_2(c_register: bitarray, d_register: bitarray) -> bitarray:
    """Given C_i and D_i, returns K_i (a round key)"""
    assert len(c_register) == 28
    assert len(d_register) == 28

    first_half_digits = (c_register[i - 1] for i in pc2_schedule[:24])
    second_half_digits = (d_register[i - 29] for i in pc2_schedule[24:])
    round_key_digits = itertools.chain(first_half_digits, second_half_digits)
    return bitarray(round_key_digits)


def des_key_schedule(key: bitarray) -> Generator[bitarray]:
    assert len(key) == 64
    c_register: bitarray
    d_register: bitarray
    c_register, d_register = permuted_choice_1(key)

    def get_v(round_number: int) -> int:
        if round_number in {1, 2, 9, 16}: return 1
        return 2

    for round_number in range(1, 17):
        v = get_v(round_number)
        c_register = circular_left_shift(c_register, v)
        d_register = circular_left_shift(d_register, v)
        round_key = permuted_choice_2(c_register, d_register)
        yield round_key


__all__ = ("des_key_schedule",)
