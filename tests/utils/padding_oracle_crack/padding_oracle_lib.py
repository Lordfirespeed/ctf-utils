from secrets import token_bytes as random_bytes

from cryptography.hazmat.primitives import padding as paddings
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SimpleCrypto:
    def __init__(self, key: bytes = None) -> None:
        if key is None:
            key = random_bytes(32)

        self.algorithm = algorithms.AES(key)
        self.padding = paddings.PKCS7(self.algorithm.block_size)
        self.block_size_in_bytes = self.algorithm.block_size // 8
        self.mode_factory = modes.CBC

    def cipher_factory(self, iv: bytes) -> Cipher:
        return Cipher(self.algorithm, self.mode_factory(iv))

    def encrypt(self, plaintext: bytes) -> bytes:
        padder = self.padding.padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        iv = random_bytes(self.block_size_in_bytes)
        encryptor = self.cipher_factory(iv).encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, payload: bytes) -> bytes:
        block_length, remainder = divmod(len(payload), self.block_size_in_bytes)
        assert remainder == 0, "payload length should be a multiple of block size"
        assert block_length >= 2, "payload should contain one IV block and at least one ciphertext block"

        iv = payload[:self.block_size_in_bytes]
        ciphertext = payload[self.block_size_in_bytes:]
        decryptor = self.cipher_factory(iv).decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = self.padding.unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext


def main():
    my_crypto = SimpleCrypto()

    message = u"a secret message of arbitrary length"
    encrypted_message = my_crypto.encrypt(message.encode("utf-8"))
    round_trip_message = my_crypto.decrypt(encrypted_message).decode("utf-8")
    assert message == round_trip_message


if __name__ == "__main__":
    main()
