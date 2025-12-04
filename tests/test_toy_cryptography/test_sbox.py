import unittest
from typing import Sequence

from bitarray.util import ba2hex, int2ba

from toy_cryptography.sbox.scheme import encrypt as sbox_encrypt, decrypt as sbox_decrypt

class SboxTestVectors(unittest.TestCase):

    def _test_with_vectors(self, vectors: Sequence[tuple[int, int, int]]):
        for key_int, plaintext_int, expected_ciphertext_int in vectors:
            key = int2ba(key_int, length=64)
            plaintext = int2ba(plaintext_int, length=64)
            expected_ciphertext = int2ba(expected_ciphertext_int, length=64)

            with self.subTest(plaintext=ba2hex(plaintext)):
                ciphertext = sbox_encrypt(plaintext, key)
                self.assertEqual(ba2hex(expected_ciphertext), ba2hex(ciphertext))
                round_trip_plaintext = sbox_decrypt(ciphertext, key)
                self.assertEqual(ba2hex(plaintext), ba2hex(round_trip_plaintext))

    test_vectors = (
        (0x0000000000000000, 0x0123456789abcdef, 0x1b03106309d4565c),
        (0xffffffffffffffff, 0x0123456789abcdef, 0x3e0fd46fb452fe83),
        (0x0123456789abcdef, 0x0000000000000000, 0x1a8db1ce0ae235dd),
        (0x0123456789abcdef, 0x0123456789abcdef, 0x90bdd061ddf6c261),
        (0x0123456789abcdef, 0xffffffffffffffff, 0xda0f1f303bb1bf3c),
        (0x0123456789abcdef, 0x00000000ffffffff, 0x0edc46ae2dc2011f),
    )

    def test(self):
        self._test_with_vectors(self.test_vectors)


if __name__ == '__main__':
    unittest.main()
