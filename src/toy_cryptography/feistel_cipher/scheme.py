from dataclasses import dataclass
from typing import Callable, Sequence

from bitarray import frozenbitarray, bitarray
from bitarray.util import ba2int


type FeistelFunction = Callable[[bitarray, bitarray], bitarray]


@dataclass(frozen=True)
class FeistelText:
    left: frozenbitarray
    right: frozenbitarray

    def __post_init__(self):
        assert len(self.left) == len(self.right)
        if isinstance(self.left, bitarray):
            object.__setattr__(self, "left", frozenbitarray(self.left))
        if isinstance(self.right, bitarray):
            object.__setattr__(self, "right", frozenbitarray(self.right))

    @property
    def half_length(self):
        return len(self.left)

    @property
    def value_bits(self) -> frozenbitarray:
        return self.left + self.right

    @property
    def value_int(self) -> int:
        return ba2int(self.value_bits)


def encryption_round(text: FeistelText, round_key: bitarray, function: FeistelFunction) -> FeistelText:
    new_left = text.right
    new_right = text.left ^ function(text.right, round_key)
    return FeistelText(new_left, new_right)


def encrypt(text: FeistelText, round_keys: Sequence[bitarray], function: FeistelFunction) -> FeistelText:
    for round_key in round_keys:
        text = encryption_round(text, round_key, function)
    return text


def decryption_round(text: FeistelText, round_key: bitarray, function: FeistelFunction) -> FeistelText:
    new_right = text.left
    new_left = text.right ^ function(text.left, round_key)
    return FeistelText(new_left, new_right)


def decrypt(text: FeistelText, round_keys: Sequence[bitarray], function: FeistelFunction) -> FeistelText:
    for round_key in reversed(round_keys):
        text = decryption_round(text, round_key, function)
    return text


__all__ = ("FeistelText", "FeistelFunction", "encrypt", "decrypt",)
