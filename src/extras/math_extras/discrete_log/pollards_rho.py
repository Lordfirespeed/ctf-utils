import functools
from copy import copy
from dataclasses import dataclass
from random import randrange
from typing import Callable, TypeAlias

from extras.math_extras.discrete_log.lib import Group

StepLookup: TypeAlias = dict[int, int]  # a mapping of value: step number


@dataclass
class PollardRhoDiscreteLogRabbit:
    x: int
    s: int
    t: int


Logarithmiser: TypeAlias = Callable[[Group, int], int]


@functools.cache
def make_pollard_rho_discrete_logarithmiser(s_seed: int = 0, t_seed: int = 0) -> Logarithmiser:
    def logarithmiser(group: Group, group_element: int) -> int:
        class Rabbit(PollardRhoDiscreteLogRabbit):
            def step_first_case(self) -> None:
                self.x = (self.x * group.generator) % group.modulus
                self.s = (self.s + 1) % group.order

            def step_second_case(self) -> None:
                self.x = (self.x * group_element) % group.modulus
                self.t = (self.t + 1) % group.order

            def step_third_case(self) -> None:
                self.x = pow(self.x, 2, mod=group.modulus)
                self.s = (2 * self.s) % group.order
                self.t = (2 * self.t) % group.order

            def pseudorandom_step(self) -> None:
                partition = self.x % 3
                if partition == 0:
                    self.step_first_case()
                    return
                if partition == 1:
                    self.step_second_case()
                    return
                if partition == 2:
                    self.step_third_case()
                    return

        # x = generator^s * group_element^t (mod modulus)
        initial_x = (pow(group.generator, s_seed, mod=group.modulus) * pow(
            group_element, t_seed, mod=group.modulus
        )) % group.modulus
        first = Rabbit(x=initial_x, s=s_seed, t=t_seed)
        second = copy(first)

        while True:
            first.pseudorandom_step()
            second.pseudorandom_step()
            second.pseudorandom_step()
            if first.x == second.x:
                break

        remainder = (first.t - second.t) % group.order
        if remainder == 0:
            other_logarithmiser = make_pollard_rho_discrete_logarithmiser(
                s_seed=randrange(2, group.order),
                t_seed=randrange(2, group.order),
            )
            return other_logarithmiser(group, group_element)
        return (pow(remainder, -1, mod=group.order) * (second.s - first.s)) % group.order

    return logarithmiser


pollard_rho_discrete_log = make_pollard_rho_discrete_logarithmiser()


__all__ = ("pollard_rho_discrete_log", "make_pollard_rho_discrete_logarithmiser",)
