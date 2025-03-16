from .keys import RSAPrivateKey, RSAPublicKey


def signature_for(message: int, key: RSAPrivateKey) -> int:
    return pow(message, key.private_exponent, mod=key.modulus)


def verify_signature(message: int, signature: int, key: RSAPublicKey) -> bool:
    round_trip = pow(signature, key.public_exponent, mod=key.modulus)
    return message == round_trip


__all__ = ("signature_for", "verify_signature",)
