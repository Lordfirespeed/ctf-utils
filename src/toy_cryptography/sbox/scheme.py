from bitarray import bitarray
from bitarray.util import int2ba, ba2int, ba2hex

from toy_cryptography import feistel_cipher
from toy_cryptography.sbox.feistel_function import sbox_feistel_function
from toy_cryptography.sbox.key_schedule import sbox_key_schedule


def encrypt(plaintext: bitarray, key: bitarray) -> bitarray:
    assert len(plaintext) == 64
    round_keys = list(sbox_key_schedule(key))
    left = plaintext[0:32]
    right = plaintext[32:64]
    text = feistel_cipher.FeistelText(left, right)
    encrypted = feistel_cipher.encrypt(text, round_keys, sbox_feistel_function)
    return encrypted.left + encrypted.right


def decrypt(ciphertext: bitarray, key: bitarray) -> bitarray:
    assert len(ciphertext) == 64
    round_keys = list(sbox_key_schedule(key))
    left = ciphertext[0:32]
    right = ciphertext[32:64]
    text = feistel_cipher.FeistelText(left, right)
    decrypted = feistel_cipher.decrypt(text, round_keys, sbox_feistel_function)
    return decrypted.left + decrypted.right


if __name__ == "__main__":
    key = int2ba(0x0123456789abcdef, length=64)
    plaintext = int2ba(0x00000000ffffffff, length=64)
    ciphertext = encrypt(plaintext, key)
    print(ba2hex(ciphertext))
    round_trip_plaintext = decrypt(ciphertext, key)
    print(ba2hex(round_trip_plaintext))
