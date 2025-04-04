from dataclasses import dataclass
from typing import Callable, Sequence

from extras.binary_extras import binlify, unbinlify


type FeistelFunction = Callable[[int, int], int]


@dataclass(frozen=True)
class FeistelText:
    left: int
    right: int
    half_length: int

    @property
    def value(self) -> int:
        left_digits = binlify(self.left, self.half_length)
        right_digits = binlify(self.right, self.half_length)
        digits = [*left_digits, *right_digits]
        return unbinlify(digits)


def encryption_round(text: FeistelText, round_key: int, function: FeistelFunction) -> FeistelText:
    new_left = text.right
    new_right = text.left ^ function(text.right, round_key)
    return FeistelText(new_left, new_right, text.half_length)


def encrypt(text: FeistelText, round_keys: Sequence[int], function: FeistelFunction) -> FeistelText:
    for round_key in round_keys:
        text = encryption_round(text, round_key, function)
    return text


def decryption_round(text: FeistelText, round_key: int, function: FeistelFunction) -> FeistelText:
    new_right = text.left
    new_left = text.right ^ function(text.left, round_key)
    return FeistelText(new_left, new_right, text.half_length)


def decrypt(text: FeistelText, round_keys: Sequence[int], function: FeistelFunction) -> FeistelText:
    for round_key in reversed(round_keys):
        text = decryption_round(text, round_key, function)
    return text


__all__ = ("FeistelText", "FeistelFunction", "encrypt", "decrypt",)
