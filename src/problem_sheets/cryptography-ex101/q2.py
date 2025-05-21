from bitarray import bitarray
from bitarray.util import ba2int, int2ba

from toy_cryptography.feistel_cipher.scheme import *


def feistel_function(text: bitarray, key: bitarray) -> bitarray:
    digits = [
        ((text[0] + key[0]) % 2) * key[1],
        ((text[1] + key[1]) % 2) * key[2],
        ((text[2] + key[2]) % 2) * key[3],
        ((text[3] + key[3]) % 2) * key[0],
    ]
    return bitarray(digits)


def main():
    plaintext = FeistelText(
        left=int2ba(0b0111, length=4),
        right=int2ba(0b0001, length=4),
    )
    print(f"{plaintext.value_int = :08b}")

    round_keys = [
        int2ba(0b0101, length=4),
        int2ba(0b1101, length=4),
    ]

    ciphertext = encrypt(plaintext, round_keys, feistel_function)
    print(f"{ciphertext.value_int = :08b}")

    round_trip = decrypt(ciphertext, round_keys, feistel_function)
    print(f"{round_trip.value_int = :08b}")
    assert plaintext.value_bits == round_trip.value_bits


if __name__ == "__main__":
    main()
