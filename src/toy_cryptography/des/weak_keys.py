from typing import Sequence

from bitarray import bitarray
from bitarray.util import int2ba

from .key_schedule import des_key_schedule


weak_keys = [
    0x0101_0101_0101_0101,  # C_0: 0...0,  D_0: 0...0
    0xfefe_fefe_fefe_fefe,  # C_0: 1...1,  D_0: 1...1
    0x1f1f_1f1f_0e0e_0e0e,  # C_0: 0...0,  D_0: 1...1
    0xe0e0_e0e0_f1f1_f1f1,  # C_0: 1...1,  D_0: 0...0
]
"""
a DES weak key is one such that E(E(x, K), K) = x, i.e. encryption is an involution.
The above are actually the only weak keys of DES (since values with invalid parity bits are not keys).

Note that weak keys of n-round Feistel ciphers must have the property that their key schedule is
palindromic, ie. K_1 = K_n, K_2 = K_{n-1}, etc.
By the construction of DES' key schedule, the only keys with palindromic schedules are those with
homogeneous C_0, D_0; those keys are listed here.
"""


def is_palindrome(sequence: Sequence[object]) -> bool:
    return all(a == b for a, b in zip(sequence, reversed(sequence)))


def check_weak_key(key: bitarray) -> None:
    round_keys = list(des_key_schedule(key))
    assert is_palindrome(round_keys)


def main():
    for key_int in weak_keys:
        key = int2ba(key_int, length=64)
        check_weak_key(key)


if __name__ == '__main__':
    main()
