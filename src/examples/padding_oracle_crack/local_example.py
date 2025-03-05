from secrets import token_urlsafe
from time import sleep

from utils.padding_oracle_crack import PaddingOracleCracker
from utils.simple_crypto import SimpleCrypto


crypto = SimpleCrypto()


def oracle(iv: bytes, ciphertext: bytes) -> bool:
    global crypto
    sleep(0.0005)  # to simulate delay of e.g. performing HTTP request
    try:
        crypto.decrypt(iv, ciphertext)
    except (ValueError, AssertionError):
        return False
    return True


message = token_urlsafe()
plaintext = message.encode("ascii")
iv, ciphertext = crypto.encrypt(plaintext)


assert oracle(iv, ciphertext)


def main():
    cracker = PaddingOracleCracker(iv, ciphertext, oracle)
    round_trip_plaintext = cracker.crack_plaintext()
    round_trip_message = round_trip_plaintext.decode("ascii")
    print(round_trip_message)


if __name__ == "__main__":
    main()
