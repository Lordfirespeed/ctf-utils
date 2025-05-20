from dataclasses import dataclass, field
from random import randrange
from typing import NamedTuple

from toy_cryptography.dh.params import DiffieHellmanParams


@dataclass
class ElGamalKeyPair:
    params: DiffieHellmanParams
    private_key: int
    public_key: int = field(init=False)

    def __post_init__(self):
        self.public_key = pow(self.params.generator, self.private_key, mod=self.params.prime)

    @classmethod
    def random(cls, params: DiffieHellmanParams) -> "ElGamalKeyPair":
        private_key = pick_secret(params)
        return cls(params, private_key)


class ElGamalEncryptedMessage(NamedTuple):
    y1: int  # g^s mod p, for s a random IV
    y2: int  # m * g^(as) mod p


def pick_secret(params: DiffieHellmanParams) -> int:
    # choosing 0 or 1 would make the system insecure even without solving discrete log
    return randrange(2, params.prime - 1)


def el_gamal_encrypt(params: DiffieHellmanParams, public_key: int, message: int) -> ElGamalEncryptedMessage:
    secret = pick_secret(params)
    y1 = pow(params.generator, secret, mod=params.prime)
    y2 = (message * pow(public_key, secret, mod=params.prime)) % params.prime
    return ElGamalEncryptedMessage(y1, y2)


def el_gamal_decrypt(params: DiffieHellmanParams, private_key: int, ciphertext: ElGamalEncryptedMessage) -> int:
    neutraliser = pow(pow(ciphertext.y1, private_key, mod=params.prime), -1, mod=params.prime)
    return (neutraliser * ciphertext.y2) % params.prime


__all__ = (
    "ElGamalKeyPair",
    "ElGamalEncryptedMessage",
    "el_gamal_encrypt",
    "el_gamal_decrypt",
)
