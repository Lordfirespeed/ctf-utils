from typing import Callable

from toy_cryptography.plain_rsa_signatures import signature_for, verify_signature
from toy_cryptography.plain_rsa_signatures.keys import *

type SigningOracle = Callable[[int], int]


def adversary(oracle: SigningOracle, key: RSAPublicKey) -> (int, int):
    message = 1234567890

    residual = pow(message, -1, mod=key.modulus)
    residual_signature = oracle(residual)

    signature = pow(residual_signature, -1, mod=key.modulus)
    return message, signature


def game() -> bool:
    private_key = determine_private_key(
        prime1=278_087,
        prime2=115_903,
        public_exponent=31,
    )
    public_key = private_key.extract_public_key()
    messages_submitted_to_signing_oracle: set[int] = set()

    def signing_oracle(message: int) -> int:
        nonlocal messages_submitted_to_signing_oracle, private_key
        messages_submitted_to_signing_oracle.add(message)
        return signature_for(message, private_key)

    message, signature = adversary(signing_oracle, public_key)
    if message in messages_submitted_to_signing_oracle:
        return False
    return verify_signature(message, signature, public_key)


def main():
    outcome = game()
    print(f"The adversary {"won" if outcome else "lost"} the game")


if __name__ == '__main__':
    main()
