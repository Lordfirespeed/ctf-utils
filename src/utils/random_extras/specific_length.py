from utils.random_extras.sysrandom import randrange, getrandbits


def randint_of_bit_length(k: int) -> int:
    """Return a random non-negative integer with exactly `k` bits."""
    constant_contribution = 1 << (k - 1)
    random_contribution = getrandbits(k - 1)
    return constant_contribution + random_contribution


def randint_of_digit_length(k: int) -> int:
    """
    Return a random non-negative integer with exactly `k` digits.
    Note the first digit is technically 'less random' than the other digits, as it can't be zero.
    """
    lower_bound = pow(10, k)
    upper_bound = lower_bound * 10
    return randrange(lower_bound, upper_bound)


__all__ = (
    "randint_of_bit_length",
    "randint_of_digit_length",
)
