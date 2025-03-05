from secrets import token_urlsafe
import unittest

from utils.padding_oracle_crack import PaddingOracleCracker
from utils.simple_crypto import SimpleCrypto


class MyTestCase(unittest.TestCase):
    crypto: SimpleCrypto

    def oracle(self, iv: bytes, ciphertext: bytes) -> bool:
        try:
            self.crypto.decrypt(iv, ciphertext)
        except (ValueError, AssertionError):
            return False
        return True

    def setUp(self):
        self.crypto = SimpleCrypto()

    def tearDown(self):
        self.crypto = None

    def test_crypto(self):
        message = token_urlsafe()
        plaintext = message.encode("utf-8")
        iv, ciphertext = self.crypto.encrypt(plaintext)
        round_trip_plaintext = self.crypto.decrypt(iv, ciphertext)
        round_trip_message = round_trip_plaintext.decode("utf-8")
        self.assertEqual(message, round_trip_message)

    def test_crack(self):
        message = token_urlsafe()
        plaintext = message.encode("utf-8")
        iv, ciphertext = self.crypto.encrypt(plaintext)
        cracker = PaddingOracleCracker(iv, ciphertext, self.oracle, render_progress=False)
        round_trip_plaintext = cracker.crack_plaintext()
        round_trip_message = round_trip_plaintext.decode("utf-8")
        self.assertEqual(message, round_trip_message)


if __name__ == '__main__':
    unittest.main()
