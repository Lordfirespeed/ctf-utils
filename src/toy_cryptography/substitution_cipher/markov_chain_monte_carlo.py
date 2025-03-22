"""
https://www.ams.org/journals/bull/2009-46-02/S0273-0979-08-01238-X/S0273-0979-08-01238-X.pdf
"""
import asyncio
import itertools
from string import ascii_lowercase
from typing import Callable, NewType

from gmpy2 import mpq

from extras.random_extras import sysrandom
from extras.collections_extras import bidict, sortabledict
from utils.data.bigrams import load_lowercase_bigrams_dataset
from utils.reprint import Printer

from .scheme import CipherKey, decode


BigramProportions = NewType("BigramProportions", sortabledict[str, mpq])
Plausibility = NewType("Plausibility", mpq)


async def load_english_bigram_proportions() -> BigramProportions:
    lowercase_bigram_frequencies = await load_lowercase_bigrams_dataset()
    total_frequency = sum(lowercase_bigram_frequencies.values())
    lowercase_bigram_proportions = BigramProportions(sortabledict[str, mpq]())
    for bigram, frequency in lowercase_bigram_frequencies.items():
        lowercase_bigram_proportions[bigram] = mpq(frequency, total_frequency)
    return lowercase_bigram_proportions


english_bigram_proportions = asyncio.run(load_english_bigram_proportions())


def plausibility(plaintext: str, reference: BigramProportions = None) -> Plausibility:
    if len(plaintext) < 2:
        raise ValueError
    if reference is None:
        reference = english_bigram_proportions

    accumulator = mpq(1)
    cursor = 0
    while cursor + 1 < len(plaintext):
        bigram = plaintext[cursor:cursor+2]
        bigram_proportion = reference[bigram]
        accumulator *= bigram_proportion
        cursor += 1

    return Plausibility(accumulator)


def maximise_plaintext_plausibility(
    ciphertext: str,
    initial_key: CipherKey,
    reference: BigramProportions = None,
) -> CipherKey:
    plaintext_alphabet = sorted(initial_key.values())
    current_key = bidict(initial_key)

    type Swap = (str, str)

    def random_swap() -> Swap:
        nonlocal plaintext_alphabet
        return sysrandom.sample(plaintext_alphabet, 2)

    def apply_swap(swap: Swap) -> None:
        """Note that applying a swap for a second time is functionally equivalent to 'undoing' the swap."""
        nonlocal current_key
        first, second = swap
        first_image = current_key[first]
        second_image = current_key[second]
        current_key.forceput(first, second_image)
        current_key.put(second, first_image)

    def compute_current_plausibility() -> Plausibility:
        nonlocal ciphertext, current_key, reference
        plaintext = decode(ciphertext, current_key)
        return plausibility(plaintext, reference)

    def print_status(iteration: int, printer: Callable[[str], None]) -> None:
        plaintext_preview = decode(ciphertext[:25], current_key)
        printer(f"epoch {iteration:5}: '{plaintext_preview}...'")

    def main_loop(printer: Callable[[str], None]):
        current_plausibility = compute_current_plausibility()
        iterations_without_acceptance = 0
        for iteration_index in itertools.count():
            if iteration_index % 100 == 0:
                print_status(iteration_index, printer)
            if iterations_without_acceptance >= 350:
                break
            swap = random_swap()
            apply_swap(swap)
            new_plausibility = compute_current_plausibility()
            if new_plausibility > current_plausibility:
                current_plausibility = new_plausibility
                iterations_without_acceptance = 0
                continue
            if sysrandom.coin_flip(p=(new_plausibility/current_plausibility)):
                current_plausibility = new_plausibility
                iterations_without_acceptance = 0
                continue
            apply_swap(swap)
            iterations_without_acceptance += 1

    with Printer() as printer:
        main_loop(printer)

    return current_key


__all__ = ("BigramProportions", "Plausibility", "plausibility", "maximise_plaintext_plausibility",)


def main():
    from .analyser import ciphertext, analyse_character_frequencies, infer_cipher_key
    ciphertext_character_frequency = analyse_character_frequencies(ciphertext)
    cipher_key = infer_cipher_key(ciphertext_character_frequency)
    better_key = maximise_plaintext_plausibility(ciphertext, cipher_key)
    print(better_key)
    print("".join(better_key[c] for c in ascii_lowercase))


if __name__ == "__main__":
    main()
