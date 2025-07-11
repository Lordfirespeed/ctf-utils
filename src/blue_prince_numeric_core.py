import dataclasses
import itertools
from string import ascii_lowercase
from operator import add as op_add, sub as op_sub, mul as op_mul
from typing import Callable, Sequence


def op_div(a: int, b: int) -> int:
    result, remainder = divmod(a, b)
    if remainder != 0:
        raise ValueError
    return result


@dataclasses.dataclass(frozen=True)
class Operator:
    apply: Callable[[int, int], int]
    symbol: str

    def __repr__(self):
        return self.symbol


add = Operator(op_add, "+")
sub = Operator(op_sub, "-")
mul = Operator(op_mul, "*")
div = Operator(op_div, "/")


def evaluate_expression(operands: Sequence[int], operators: Sequence[Operator]) -> int:
    assert len(operands) == len(operators)
    accumulator = 0
    for operand, operator in zip(operands, operators):
        accumulator = operator.apply(accumulator, operand)
    return accumulator


def format_expression(operands: Sequence[int], operators: Sequence[Operator]) -> str:
    assert len(operands) == len(operators)
    return ", ".join(f"{operator} {operand}" for operand, operator in zip(operands, operators))


all_operators_set = {add, sub, mul, div}


def numeric_core(numbers: Sequence[int], verbose=False) -> int:
    fixed_operations = (add,)
    remaining_operator_choices = all_operators_set.difference(fixed_operations)

    smallest_whole_number = None

    for rest_operations in itertools.permutations(remaining_operator_choices):
        operations = (*fixed_operations, *rest_operations)
        try:
            result = evaluate_expression(numbers, operations)
        except ValueError:
            result = None

        if verbose:
            print(f"{format_expression(numbers, operations)} -> {result}")

        if result is None or result < 0:
            continue
        if smallest_whole_number is not None and result > smallest_whole_number:
            continue
        smallest_whole_number = int(result)

    if len(str(smallest_whole_number)) > 3:
        raise NotImplementedError(f"got number: {smallest_whole_number}. recurse here once number splitting is understood")

    return smallest_whole_number


if __name__ == "__main__":
    print(numeric_core([1000, 200, 11, 2]))
