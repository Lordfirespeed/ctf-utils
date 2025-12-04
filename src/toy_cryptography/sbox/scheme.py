from bitarray import bitarray
from bitarray.util import int2ba, ba2int

from toy_cryptography import feistel_cipher
from toy_cryptography.sbox.feistel_function import sbox_feistel_function
from toy_cryptography.sbox.key_schedule import sbox_key_schedule


def encrypt(plaintext: bitarray, key: bitarray) -> bitarray:
    round_keys = list(sbox_key_schedule(key))
    left = plaintext[0:32]
    right = plaintext[32:64]
    text = feistel_cipher.FeistelText(left, right)
    encrypted = feistel_cipher.encrypt(text, round_keys, sbox_feistel_function)
    return encrypted.left + encrypted.right


if __name__ == "__main__":
    key = int2ba(0x0000000000000000, length=64)
    plaintext = int2ba(0x0123456789abcdef, length=64)
    ciphertext = encrypt(plaintext, key)
    print(hex(ba2int(ciphertext)))
