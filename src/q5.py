from copy import replace
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Generator, Iterable

from bitarray import bitarray, frozenbitarray
from bitarray.util import int2ba, ba2int


substitute_schedule = (
    0b0000, 0b1011, 0b0101, 0b0001, 0b0110, 0b1000, 0b1101, 0b0100,
    0b1111, 0b0111, 0b0010, 0b1100, 0b1001, 0b0011, 0b1110, 0b1010,
)
def substitute(value: bitarray) -> bitarray:
    assert len(value) == 4
    value_index = ba2int(value)
    substitution = substitute_schedule[value_index]
    return int2ba(substitution, length=4)


def bitarrays_of_length(length: int) -> Generator[bitarray]:
    for value in range(0, pow(2, length)):
        yield int2ba(value, length=length)


def compute_truth_probability(
    inputs: Iterable[bitarray],
    operation: Callable[[bitarray], bitarray],
    equation: Callable[[bitarray, bitarray], bool],
) -> Fraction:
    """
    Compute the probability of equation(x, operation(x)) evaluating 'true' over some inputs.
    """
    truth_count = 0
    input_count = 0
    for input in inputs:
        output = operation(input)
        input_count += 1
        truth_count += equation(input, output)
    return Fraction(truth_count, input_count)


@dataclass(frozen=True)
class AffineFunction:
    bit_mask: frozenbitarray
    negated: bool

    def evaluate(self, input: bitarray) -> bool:
        assert len(input) == len(self.bit_mask)
        # XOR-ing a big sequence of bits together is equivalent to counting 1s mod 2
        true_count = (input & self.bit_mask).count(1) + self.negated
        return bool(true_count % 2)

    def __call__(self, input: bitarray) -> bool:
        return self.evaluate(input)

    def __str__(self):
        literals = [f"x_{i}" for i, v in enumerate(self.bit_mask) if v]
        if self.negated: literals.append("1")
        return " ^ ".join(literals)


def non_negated_affine_functions_on_inputs_of_length(length: int) -> Generator[AffineFunction]:
    for mask in bitarrays_of_length(length):
        yield AffineFunction(frozenbitarray(mask), False)


def compute_most_biased_affine_function_for_output_bit(
    output_bit_index: int,
    inputs: Iterable[bitarray],
    operation: Callable[[bitarray], bitarray],
    expressions: Iterable[AffineFunction],
):
    """
    Find the affine expression which maximises prob(operation(x)[output_bit_index] == expression(x)) over some inputs.
    """
    inputs = list(inputs)

    def candidate_equation(candidate: AffineFunction):
        def equation(input: bitarray, output: bitarray):
            return output[output_bit_index] == candidate(input)
        return equation

    def compute_candidate_truth_probability(candidate: AffineFunction):
        return compute_truth_probability(inputs, operation, candidate_equation(candidate))

    def compute_candidate_bias(candidate: AffineFunction):
        truth_probability = compute_candidate_truth_probability(candidate)
        bias = abs(truth_probability - Fraction(1, 2))
        return bias

    most_biased_candidate = max(expressions, key=compute_candidate_bias)
    if compute_candidate_truth_probability(most_biased_candidate) < Fraction(1, 2):
        most_biased_candidate = replace(most_biased_candidate, negated=True)
    return most_biased_candidate


def main():
    for bit_index in range(4):
        most_biased_affine_function_for_bit = compute_most_biased_affine_function_for_output_bit(
            bit_index,
            bitarrays_of_length(4),
            substitute,
            non_negated_affine_functions_on_inputs_of_length(4),
        )
        print(f"y_{bit_index} = {most_biased_affine_function_for_bit}")


if __name__ == "__main__":
    main()
