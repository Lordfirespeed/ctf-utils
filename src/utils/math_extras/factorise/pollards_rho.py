import functools
from operator import index
from random import randrange
from typing import SupportsIndex

from utils.math_extras.extended_euclidian_algorithm import extended_euclidian_algorithm
from utils.typedefs.factorise import *


class PollardRhoFailure(Exception):
    pass


@functools.cache
def make_pollards_rho_factoriser(seed: int = 2, b: int = 1) -> Factoriser:
    def polynomial(value: int, modulus: int):
        return (pow(value, 2, mod=modulus) + b) % modulus

    def factoriser(value: SupportsIndex) -> int:
        """
        https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm#Algorithm
        """
        value = index(value)
        if value <= 1: raise ValueError
        if value % 2 == 0: return 2

        x = seed
        y = x
        d = 1

        while d == 1:
            x = polynomial(x, value)
            y = polynomial(y, value)
            y = polynomial(y, value)
            extended_euclidian_result = extended_euclidian_algorithm(abs(x - y), value)
            d = extended_euclidian_result.gcd

        if d == value:
            other_factoriser = make_pollards_rho_factoriser(seed=randrange(2, value), b=randrange(2, value))
            return other_factoriser(value)

        return d

    return factoriser


default_pollard_rho_factoriser = make_pollards_rho_factoriser()


__all__ = ("PollardRhoFailure", "default_pollard_rho_factoriser", "make_pollards_rho_factoriser",)
