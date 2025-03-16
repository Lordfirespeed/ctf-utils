from random import randrange
from typing import NamedTuple

from extras.binary_extras import count_trailing_zeroes


class TwoFactorisation(NamedTuple):
    two_exponent: int
    remaining_factor: int

    @property
    def value(self) -> int:
        return pow(2, self.two_exponent) * self.remaining_factor


def factor_out_powers_of_two(value: int) -> TwoFactorisation:
    two_exponent = count_trailing_zeroes(value)
    remaining_factor = value >> two_exponent
    return TwoFactorisation(two_exponent, remaining_factor)


def miller_rabin_primality_test(value: int, round_count=2) -> bool:
    """
    https://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Miller-Rabin_test
    :return: True for a probable prime, False otherwise
    """
    if value < 0:
        raise ValueError
    if value <= 1:
        return False
    if value <= 3:
        return True

    s, d = factor_out_powers_of_two(value - 1)
    if s == 0:
        # if `value - 1` is odd, `value` is even and therefore not prime
        return False

    for _ in range(round_count):
        a = randrange(2, value - 1)
        x = pow(a, d, mod=value)
        y = None
        for _ in range(s):
            y = pow(x, 2, mod=value)
            if y == 1 and x != 1 and x != (value - 1):
                return False
            x = y
        if y != 1:
            return False
    return True


__all__ = (
    "TwoFactorisation",
    "factor_out_powers_of_two",
    "miller_rabin_primality_test",
)
