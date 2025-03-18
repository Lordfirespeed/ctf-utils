from extras.random_extras.sysrandom import getrandbits
from toy_cryptography.plain_rsa_signatures import verify_signature
from toy_cryptography.plain_rsa_signatures.keys import *


def adversary(key: RSAPublicKey) -> (int, int):
    signature = getrandbits(64)
    message = pow(signature, key.public_exponent, mod=key.modulus)
    return message, signature


def game() -> bool:
    private_key = determine_private_key(
        prime1=514963008337,
        prime2=214745560343,
        public_exponent=2621,
    )
    public_key = private_key.extract_public_key()
    message, signature = adversary(public_key)
    return verify_signature(message, signature, public_key)


def main():
    outcome = game()
    print(f"The adversary {"won" if outcome else "lost"} the game")


if __name__ == "__main__":
    main()
