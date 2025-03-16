from extras.math_extras import extended_euclidian_algorithm
from extras.random_extras.sysrandom import getrandbits


def randint_coprime_to(value: int) -> int:
    """Return a random integer (non-trivially) co-prime to `value`."""
    while True:
        candidate = getrandbits(value.bit_length())
        gcd = extended_euclidian_algorithm(candidate, value).gcd
        if gcd != candidate:
            break

    if gcd > 1:
        return candidate // gcd
    return candidate


__all__ = ("randint_coprime_to",)
