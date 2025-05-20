from typing import NewType

from extras.random_extras.sysrandom import randrange

from toy_cryptography.dh.params import DiffieHellmanParams


DHPrivateKey = NewType("DHPrivateKey", int)
DHPublicKey = NewType("DHPublicKey", int)


def pick_private_key(params: DiffieHellmanParams) -> DHPrivateKey:
    return DHPrivateKey(randrange(2, params.prime - 1))


def derive_public_key(params: DiffieHellmanParams, private_key: DHPrivateKey) -> DHPublicKey:
    return DHPublicKey(pow(params.generator, private_key, mod=params.prime))


def derive_shared_secret_key(params: DiffieHellmanParams, alice_private_key: DHPrivateKey, bob_public_key: DHPublicKey) -> int:
    return pow(bob_public_key, alice_private_key, mod=params.prime)


__all__ = (
    "DHPrivateKey",
    "DHPublicKey",
    "pick_private_key",
    "derive_public_key",
    "derive_shared_secret_key",
)
