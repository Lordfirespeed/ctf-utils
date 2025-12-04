from secrets import token_bytes as random_bytes

from bitarray import bitarray
from bitarray.util import int2ba, ba2int, ba2hex, hex2ba
from cryptography.hazmat.primitives import padding as paddings

from examples.padding_oracle_crack.local_example import ciphertext
from toy_cryptography.sbox.scheme import encrypt as sbox_encrypt, decrypt as sbox_decrypt


class SimpleCryptoUsingSboxCbc:
    def __init__(self, key: bitarray = None) -> None:
        if key is None:
            key = bitarray(random_bytes(8))
        self.key = key
        self.padding = paddings.PKCS7(64)

    def encrypt(self, plaintext: bitarray) -> bitarray:
        padder = self.padding.padder()
        padded_plaintext_bytes = padder.update(plaintext.tobytes()) + padder.finalize()
        padded_plaintext = bitarray(padded_plaintext_bytes)
        iv = bitarray(random_bytes(8))
        previous_ciphertext_block = iv
        ciphertext = bitarray(len(padded_plaintext))
        for block_index in range(len(padded_plaintext) // 64):
            block_slice = slice(64 * block_index, 64 * (block_index + 1))
            plaintext_block = padded_plaintext[block_slice]
            ciphertext_block = plaintext_block ^ previous_ciphertext_block
            ciphertext_block = sbox_encrypt(ciphertext_block, self.key)
            previous_ciphertext_block = ciphertext_block
            ciphertext[block_slice] = ciphertext_block
        return iv + ciphertext

    def decrypt(self, ciphertext: bitarray) -> bitarray:
        iv, ciphertext = ciphertext[:64], ciphertext[64:]
        previous_ciphertext_block = iv
        padded_plaintext = bitarray(len(ciphertext))
        for block_index in range(len(ciphertext) // 64):
            block_slice = slice(64 * block_index, 64 * (block_index + 1))
            ciphertext_block = ciphertext[block_slice]
            plaintext_block = sbox_decrypt(ciphertext_block, self.key)
            plaintext_block = plaintext_block ^ previous_ciphertext_block
            previous_ciphertext_block = ciphertext_block
            padded_plaintext[block_slice] = plaintext_block
        unpadder = self.padding.unpadder()
        plaintext_bytes = unpadder.update(padded_plaintext.tobytes()) + unpadder.finalize()
        return bitarray(plaintext_bytes)


if __name__ == "__main__":
    foo = SimpleCryptoUsingSboxCbc()
    plaintext = hex2ba("0123456789ce")
    print(ba2hex(plaintext))
    ciphertext = foo.encrypt(plaintext)
    print(ba2hex(ciphertext))
    round_trip_plaintext = foo.decrypt(ciphertext)
    print(ba2hex(round_trip_plaintext))
