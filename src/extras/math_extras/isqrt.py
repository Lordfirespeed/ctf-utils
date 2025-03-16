from math import isqrt
from operator import index
# prefer SupportsIndex to SupportsInt as this prevents overleazous type coercion
# e.g. index(float) -> TypeError
from typing import SupportsIndex


isqrt_floor = isqrt


def isqrt_ceil(n: SupportsIndex) -> int:
    """
    https://docs.python.org/3/library/math.html#math.isqrt
    """
    return 1 + isqrt(index(n) - 1)


__all__ = ("isqrt_ceil", "isqrt_floor",)
