from extras.math_extras.isqrt import isqrt_floor
from utils.typedefs.factorise import *


def _trial_division_prime_factorise(n: int, from_trial: int = 2) -> PrimeFactorisation:
    """
    Factorise an integer into its prime factors using the trial division algorithm.
    """
    if n <= 0:
        raise ValueError
    if n == 1:
        return {}
    if n <= 3:
        return {n: 1}
    for trial in range(from_trial, isqrt_floor(n) + 1):
        new_n, remainder = divmod(n, trial)
        if remainder != 0:
            continue
        factorisation = _trial_division_prime_factorise(new_n, trial)
        trial_exponent = factorisation.get(trial, 0)
        factorisation[trial] = trial_exponent + 1
        return factorisation
    return {n: 1}


def trial_division_prime_factorise(n: int) -> PrimeFactorisation:
    return _trial_division_prime_factorise(n)


__all__ = ("trial_division_prime_factorise",)
