from typing import Sequence

from extras.binary_extras import binlify, unbinlify

from toy_cryptography.des.feistel_function import des_feistel_function
from toy_cryptography.des.key_schedule import des_key_schedule
from toy_cryptography import feistel_cipher

initial_permutation_schedule = (
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7,
)
def initial_permute(text: int) -> int:
    text_digits = binlify(text, bit_length=64)
    permuted_digits = [text_digits[i - 1] for i in initial_permutation_schedule]
    return unbinlify(permuted_digits)


final_permutation_schedule = (
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
)
def final_permute(text: int) -> int:
    text_digits = binlify(text, bit_length=64)
    permuted_digits = [text_digits[i - 1] for i in final_permutation_schedule]
    return unbinlify(permuted_digits)


def _encrypt_core(plaintext: int, round_keys: Sequence[int]) -> int:
    initial_permutation = initial_permute(plaintext)
    left = initial_permutation >> 32
    right = initial_permutation & 0xffffffff
    text = feistel_cipher.FeistelText(left, right, half_length=32)

    encrypted = feistel_cipher.encrypt(text, round_keys, des_feistel_function)
    return final_permute((encrypted.right << 32) + encrypted.left)


def encrypt(plaintext: int, key: int) -> int:
    round_keys = list(des_key_schedule(key))
    return _encrypt_core(plaintext, round_keys)


def decrypt(plaintext: int, key: int) -> int:
    round_keys = list(des_key_schedule(key))
    round_keys.reverse()
    return _encrypt_core(plaintext, round_keys)


__all__ = ("encrypt", "decrypt",)
