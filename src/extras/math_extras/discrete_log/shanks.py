from typing import Iterable, TypeAlias

from extras.math_extras.discrete_log.lib import Group
from extras.math_extras.isqrt import isqrt_ceil

StepLookup: TypeAlias = dict[int, int]  # a mapping of value: step number


def shanks_discrete_log(group: Group, group_element: int) -> int:
    m = isqrt_ceil(int(group.order))

    def generate_giant_steps() -> Iterable[int]:
        nonlocal m

        giant_step = pow(group.generator, m, mod=group.modulus)
        cursor = 1
        yield cursor
        for step_count in range(1, m):
            cursor = (cursor * giant_step) % group.modulus
            yield cursor

    def generate_baby_steps() -> Iterable[int]:
        generator_inverse = pow(group.generator, -1, mod=group.modulus)
        cursor = group_element
        yield cursor
        for step_count in range(1, m):
            cursor = (cursor * generator_inverse) % group.modulus
            yield cursor

    giant_step_lookup: StepLookup = {}
    for giant_step_count, giant_step_group_element in enumerate(generate_giant_steps()):
        if giant_step_group_element in giant_step_lookup:
            break  # a cycle has been entered
        giant_step_lookup[giant_step_group_element] = giant_step_count

    for baby_step_count, baby_step_group_element in enumerate(generate_baby_steps()):
        giant_step_count = giant_step_lookup.get(baby_step_group_element, None)
        if giant_step_count is None:
            continue

        return (m * giant_step_count + baby_step_count) % (group.modulus - 1)

    raise Exception(
        f"No solution found. Prime: {group.modulus}; Generator: {group.generator}; Group element: {group_element}"
    )


__all__ = ("shanks_discrete_log",)
