from typing import SupportsIndex
from operator import index
from math import floor, log, gcd

from extras.math_extras.prime_sieve import sieve_primes_less_than


class PollardPMinus1Failure(Exception):
    pass


def pollards_p_minus_1_factorise(value: SupportsIndex, smoothness_bound: int = None) -> int:
    value = index(value)
    if smoothness_bound is None:
        smoothness_bound = 10_000

    assert value % 2 == 1  # even numbers have a trivial factorisation and break fixing the seed a=2
    x = 2
    primes = sieve_primes_less_than(smoothness_bound + 1)
    for prime in primes:
        max_exponent_less_than_smoothness_bound = floor(log(smoothness_bound, prime))
        prime_power = pow(prime, max_exponent_less_than_smoothness_bound)
        x = pow(x, prime_power, mod=value)
        g = gcd(x - 1, value)
        if 1 < g < value:
            return g

    raise PollardPMinus1Failure


__all__ = ("pollards_p_minus_1_factorise",)
