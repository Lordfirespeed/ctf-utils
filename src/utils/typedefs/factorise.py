from typing import Callable


type PrimeFactorisation = dict[int, int]
"""a prime factorisation is a mapping of prime factors to exponents"""

type PrimeFactoriser = Callable[[int], PrimeFactorisation]
"""a prime factoriser completely factorises an integer"""

type Factoriser = Callable[[int], int]
"""a factoriser finds a single (non-trivial) factor of an integer"""


__all__ = ("PrimeFactorisation", "PrimeFactoriser", "Factoriser",)
