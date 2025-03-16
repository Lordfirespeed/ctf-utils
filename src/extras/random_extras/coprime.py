from extras.math_extras import extended_euclidian_algorithm
from extras.random_extras.sysrandom import randbelow


def make_coprime(value: int, candidate: int) -> int:
    """Return an integer co-prime to `value` which may be trivial, depending on `candidate`"""
    while True:
        if candidate == 1:
            break

        gcd = extended_euclidian_algorithm(candidate, value).gcd
        if gcd == 1:
            break

        candidate //= gcd
    return candidate


def randint_coprime_to(value: int) -> int:
    """Return a random integer (non-trivially) co-prime to `value`."""
    if value <= 2:
        # reject negative values
        # 0's unique positive co-prime value is 1, but 1 is trivial, so reject
        # similar argument for 1, 2
        raise ValueError

    while True:
        candidate = randbelow(value)
        if candidate == 0:
            continue
        candidate = make_coprime(value, candidate)
        if candidate != 1:
            break

    return candidate


__all__ = ("randint_coprime_to",)
