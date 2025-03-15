from collections import deque
from operator import index
from typing import NamedTuple, SupportsIndex


class ExtendedEuclidianAlgorithmResult[TA: SupportsIndex, TB: SupportsIndex](NamedTuple):
    """
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

    The coefficients are of Bézout's identity, integers x and y such that
    ax + by = gcd(a, b)
    """
    first: TA  # a
    second: TB  # b
    gcd: int  # gcd(a, b)
    first_coefficient: int  # x
    second_coefficient: int  # y


def extended_euclidian_algorithm[TA: SupportsIndex, TB: SupportsIndex](
    first: TA,
    second: TB,
) -> ExtendedEuclidianAlgorithmResult[TA, TB]:
    r = deque((index(first), index(second)), maxlen=2)
    s = deque((1, 0), maxlen=2)
    t = deque((0, 1), maxlen=2)

    while r[-1] > 0:
        q = r[-2] // r[-1]
        r.append(r[-2] - q * r[-1])
        s.append(s[-2] - q * s[-1])
        t.append(t[-2] - q * t[-1])

    return ExtendedEuclidianAlgorithmResult(first, second, r[-2], s[-2], t[-2])


__all__ = ("ExtendedEuclidianAlgorithmResult", "extended_euclidian_algorithm",)
