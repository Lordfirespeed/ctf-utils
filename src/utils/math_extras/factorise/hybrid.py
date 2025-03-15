from utils.typedefs import PrimeFactorisation

from .trial_division_prime import trial_division_prime_factorise
from .pollards_rho_prime import pollards_rho_prime_factorise


ten_digit_number = 9_999_999_999


def prime_factorise(n: int) -> PrimeFactorisation:
    if n <= 0:
        raise ValueError

    if n <= ten_digit_number:
        return trial_division_prime_factorise(n)

    return pollards_rho_prime_factorise(n)


__all__ = ("prime_factorise",)
