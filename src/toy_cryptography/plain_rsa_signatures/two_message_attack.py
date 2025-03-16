from typing import Callable

from extras.random_extras.sysrandom import randrange
from toy_cryptography.plain_rsa_signatures import signature_for, verify_signature

from .keys import *


type SigningOracle = Callable[[int], int]


def adversary(oracle: SigningOracle, key: RSAPublicKey) -> (int, int):
    message = 13457160153138022877

    factor1 = randrange(2, key.modulus)
    factor1_inverse = pow(factor1, -1, mod=key.modulus)
    factor2 = (message * factor1_inverse) % key.modulus

    signature1 = oracle(factor1)
    signature2 = oracle(factor2)

    signature = (signature1 * signature2) % key.modulus
    return message, signature


def game() -> bool:
    private_key = determine_private_key(
        prime1=514963008337,
        prime2=214745560343,
        public_exponent=2621,
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


if __name__ == "__main__":
    main()
