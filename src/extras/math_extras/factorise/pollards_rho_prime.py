from extras.math_extras.primality import miller_rabin_primality_test
from utils.typedefs.factorise import *

from .lib import combine_factors_left
from .pollards_rho import default_pollard_rho_factoriser


def pollards_rho_prime_factorise(n: int) -> PrimeFactorisation:
    """
    Factorise an integer into its prime factors using the trial division algorithm.
    """
    if n <= 0:
        raise ValueError
    if n == 1:
        return {}
    if miller_rabin_primality_test(n):
        return {n: 1}

    factor = default_pollard_rho_factoriser(n)
    new_n, remainder = divmod(n, factor)
    if remainder != 0:
        raise Exception

    first_factorisation = pollards_rho_prime_factorise(new_n)
    second_factorisation = pollards_rho_prime_factorise(factor)
    combine_factors_left(first_factorisation, second_factorisation)

    return first_factorisation


__all__ = ("pollards_rho_prime_factorise",)
