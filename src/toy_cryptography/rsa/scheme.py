from .keys import RSAPrivateKey, RSAPublicKey


def encrypt(message: int, key: RSAPublicKey) -> int:
    return pow(message, key.public_exponent, mod=key.modulus)


def decrypt(ciphertext: int, key: RSAPrivateKey) -> int:
    return pow(ciphertext, key.private_exponent, mod=key.modulus)


__all__ = ("encrypt", "decrypt",)
