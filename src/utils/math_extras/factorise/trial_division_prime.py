from math import isqrt

from utils.typedefs.factorise import *


def trial_division_prime_factorise(n: int) -> PrimeFactorisation:
    """
    Factorise an integer into its prime factors using the trial division algorithm.
    """
    if n <= 0:
        raise ValueError
    if n == 1:
        return {}
    if n <= 3:
        return {n: 1}
    for trial in range(2, isqrt(n) + 1):
        new_n, remainder = divmod(n, trial)
        if remainder != 0:
            continue
        factorisation = trial_division_prime_factorise(new_n)
        trial_exponent = factorisation.get(trial, 0)
        factorisation[trial] = trial_exponent + 1
        return factorisation
    return {n: 1}


__all__ = ("trial_division_prime_factorise",)
