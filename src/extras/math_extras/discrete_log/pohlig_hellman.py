from typing import NamedTuple

from extras.math_extras.chinese_remainder_theorem import Congruence, solve_congruences
from extras.math_extras.discrete_log.lib import Group
from extras.math_extras.discrete_log.pollards_rho import pollard_rho_discrete_log
from extras.math_extras.discrete_log.shanks import shanks_discrete_log
from extras.math_extras.factorise import prime_factorise


def basic_discrete_log_for_group_of_prime_order(group: Group, group_element: int) -> int:
    if group.order >= 100:
        return pollard_rho_discrete_log(group, group_element)
    return shanks_discrete_log(group, group_element)


class PrimePower(NamedTuple):
    prime: int
    exponent: int


class GroupOfPrimePowerOrder(NamedTuple):
    modulus: int
    generator: int
    order: PrimePower


def pohlig_hellman_discrete_log_for_group_of_prime_power_order(
    group: GroupOfPrimePowerOrder, group_element: int
) -> int:
    """
    https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm#Groups_of_prime-power_order
    """
    x = 0
    subproblem_generator = pow(group.generator, pow(group.order.prime, group.order.exponent - 1), mod=group.modulus)

    for k in range(group.order.exponent):
        subproblem_group = Group(group.modulus, subproblem_generator, group.order.prime)
        subproblem_group_element = pow(
            ((pow(pow(group.generator, x, mod=group.modulus), -1, mod=group.modulus) * group_element) % group.modulus),
            pow(group.order.prime, group.order.exponent - 1 - k), mod=group.modulus
        )
        subproblem_group_element_discrete_log = basic_discrete_log_for_group_of_prime_order(
            subproblem_group, subproblem_group_element
        )
        x += pow(group.order.prime, k) * subproblem_group_element_discrete_log
        x %= group.modulus
    return x


def pohlig_hellman_discrete_log(group: Group, group_element: int) -> int:
    """
    Solves an instance of the discrete logarithm problem:
    Given a (large) prime $p$, a generator $g$ for the multiplicative group of integers modulo $p$,
    and a group element $A$, find the exponent $a$ which satisfies $g^a = A mod p$.
    """
    assert group.order == group.modulus - 1
    factorisation = prime_factorise(group.order)
    congruences = []
    for prime_factor, exponent in factorisation.items():
        q = pow(prime_factor, exponent)
        magic_number = group.order // q
        subproblem_generator = pow(group.generator, magic_number, mod=group.modulus)
        subproblem_group = GroupOfPrimePowerOrder(
            group.modulus, subproblem_generator, PrimePower(prime_factor, exponent)
        )
        subproblem_group_element = pow(group_element, magic_number, mod=group.modulus)
        congruence_value = pohlig_hellman_discrete_log_for_group_of_prime_power_order(
            subproblem_group, subproblem_group_element
        )
        congruences.append(Congruence(congruence_value, q))
    return solve_congruences(congruences)


__all__ = ("pohlig_hellman_discrete_log",)
