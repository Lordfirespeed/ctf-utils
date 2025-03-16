from dataclasses import dataclass
from functools import reduce
from typing import Iterable

from .extended_euclidian_algorithm import extended_euclidian_algorithm


@dataclass
class Congruence:
    value: int
    modulus: int


def reduce_congruences(first: Congruence, second: Congruence) -> Congruence:
    extended_euclidian_result = extended_euclidian_algorithm(first.modulus, second.modulus)
    new_value = first.value * extended_euclidian_result.second_coefficient * second.modulus + second.value * extended_euclidian_result.first_coefficient * first.modulus
    new_modulus = first.modulus * second.modulus
    new_value %= new_modulus
    if abs(negative_new_value := new_value - new_modulus) < new_value:
        new_value = negative_new_value
    return Congruence(new_value, new_modulus)


def solve_congruences(congruences: Iterable[Congruence]) -> int:
    """
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    Given a system of congruences, find the unique integer (modulo $N$, the product of all congruences' moduli)
    which satisfies the system.
    """
    total_congruence = reduce(reduce_congruences, congruences)
    return total_congruence.value % total_congruence.modulus


__all__ = ("Congruence", "reduce_congruences", "solve_congruences",)
