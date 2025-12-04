import json
from pathlib import Path

from bitarray import bitarray
from bitarray.util import ba2int, int2ba

this_file = Path(__file__)
sbox_file = this_file.parent / "sbox.json"
with open(sbox_file) as sbox_file_handle:
    sbox = json.load(sbox_file_handle)


def apply_sbox(text: bitarray) -> bitarray:
    assert len(text) == 32
    substituted_digits = bitarray(32)
    for digit_index in range(4):
        text_slice = slice(8 * digit_index, 8 * (digit_index+1))
        digit = ba2int(text[text_slice])
        substituted_digit = sbox[digit]
        substituted_digits[text_slice] = int2ba(substituted_digit, length=8)
    return substituted_digits


def sbox_feistel_function(text: bitarray, key: bitarray) -> bitarray:
    sboxed = apply_sbox(text)
    mixture = sboxed ^ key
    return mixture
