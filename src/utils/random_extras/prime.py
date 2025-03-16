from utils.math_extras.primality import miller_rabin_primality_test as probable_prime

from .specific_length import randint_of_bit_length, randint_of_digit_length


def prime_randint_of_bit_length(k: int) -> int:
    """Return a random non-negative prime integer with exactly `k` bits."""
    while True:
        candidate = randint_of_bit_length(k)
        if not probable_prime(candidate):
            continue
        return candidate
    raise Exception


def prime_randint_of_digit_length(k: int) -> int:
    """Return a random non-negative prime integer with exactly `k` digits."""
    while True:
        candidate = randint_of_digit_length(k)
        if not probable_prime(candidate):
            continue
        return candidate
    raise Exception


__all__ = (
    "prime_randint_of_bit_length",
    "prime_randint_of_digit_length",
)
