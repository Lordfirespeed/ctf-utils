from extras.binary_extras import binlify, unbinlify

from toy_cryptography.feistel_cipher.scheme import *


def feistel_function(text: int, key: int) -> int:
    text_digits = binlify(text, 4)
    key_digits = binlify(key, 4)

    digits = [
        ((text_digits[0] + key_digits[0]) % 2) * key_digits[1],
        ((text_digits[1] + key_digits[1]) % 2) * key_digits[2],
        ((text_digits[2] + key_digits[2]) % 2) * key_digits[3],
        ((text_digits[3] + key_digits[3]) % 2) * key_digits[0],
    ]
    return unbinlify(digits)


def main():
    plaintext = FeistelText(
        left=0b0111,
        right=0b0001,
        half_length=4,
    )
    print(f"{ plaintext.value = :08b}")

    ciphertext = encrypt(plaintext, [0b0101, 0b1101], feistel_function)
    print(f"{ciphertext.value = :08b}")

    round_trip = decrypt(ciphertext, [0b0101, 0b1101], feistel_function)
    print(f"{round_trip.value = :08b}")
    assert plaintext.value == round_trip.value


if __name__ == "__main__":
    main()
