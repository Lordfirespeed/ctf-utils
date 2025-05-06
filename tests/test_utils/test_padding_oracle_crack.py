from secrets import token_urlsafe
import unittest

from utils.padding_oracle_crack import PaddingOracleCracker
from utils.simple_crypto import SimpleCrypto


class PaddingOracleCrackerTests(unittest.IsolatedAsyncioTestCase):
    crypto: SimpleCrypto

    async def oracle(self, iv: bytes, ciphertext: bytes) -> bool:
        try:
            self.crypto.decrypt(iv, ciphertext)
        except (ValueError, AssertionError):
            return False
        return True

    def setUp(self):
        self.crypto = SimpleCrypto()

    def tearDown(self):
        self.crypto = None

    async def test_crack(self):
        message = token_urlsafe()
        plaintext = message.encode("utf-8")
        iv, ciphertext = self.crypto.encrypt(plaintext)
        cracker = PaddingOracleCracker(iv, ciphertext, self.oracle, render_progress=False)
        round_trip_plaintext = await cracker.crack_plaintext()
        round_trip_message = round_trip_plaintext.decode("utf-8")
        self.assertEqual(message, round_trip_message)


if __name__ == '__main__':
    unittest.main()
