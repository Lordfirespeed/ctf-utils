from copy import copy
from typing import Sequence, NewType

from extras.collections_extras import bidict, sortabledict
from utils.data.monograms import english_text_letter_frequencies

from .scheme import CipherKey


CharacterProportions = NewType("CharacterProportions", sortabledict[str, float])


def analyse_character_proportions(text: str) -> CharacterProportions:
    character_counts = dict[str, int]()
    text_length = 0

    for character in text:
        if character.isspace():
            continue
        text_length += 1
        character_count = character_counts.get(character, 0)
        character_count += 1
        character_counts[character] = character_count

    character_frequencies = sortabledict({character: (count / text_length) for character, count in character_counts.items()})
    character_frequencies.sort_by_value(reverse=True)
    return CharacterProportions(character_frequencies)


def letters_ordered_by_frequency(proportions: CharacterProportions) -> Sequence[str]:
    proportions.sort_by_value(reverse=True)
    return [letter for letter in proportions.keys()]


def infer_cipher_key(
    ciphertext_proportions: CharacterProportions,
    reference: CharacterProportions = None,
) -> CipherKey:
    if reference is None:
        reference = english_text_letter_frequencies

    reference_letter_order = letters_ordered_by_frequency(reference)
    ciphertext_proportions = copy(ciphertext_proportions)
    for plaintext_character in reference_letter_order:
        proportion = ciphertext_proportions.get(plaintext_character, 0)
        ciphertext_proportions[plaintext_character] = proportion
    text_letter_order = letters_ordered_by_frequency(ciphertext_proportions)

    return bidict(zip(reference_letter_order, text_letter_order))


__all__ = (
    "CharacterProportions",
    "analyse_character_proportions",
    "letters_ordered_by_frequency",
    "infer_cipher_key",
)
