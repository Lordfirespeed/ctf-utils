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


def bigram_plausibility(plaintext: str, reference: BigramProportions = None) -> Plausibility:
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


class PlaintextPlausibilityMaximiser:

    type Swap = (str, str)
    type MutableCipherKey = bidict[str, str]

    def __init__(
        self,
        ciphertext: str,
        initial_key: CipherKey,
        reference: BigramProportions = None,
    ) -> None:
        self.ciphertext = ciphertext
        self.plaintext_alphabet = sorted(initial_key.values())
        self.current_key = bidict(initial_key)
        self.reference = reference
        self.current_plausibility = self.compute_plausibility(self.current_key)
        self.steps = 0
        self.steps_without_acceptance = 0

    def random_swap(self) -> Swap:
        return sysrandom.sample(self.plaintext_alphabet, 2)

    @staticmethod
    def apply_swap(swap: Swap, key: MutableCipherKey):
        """Note that applying a swap for a second time is functionally equivalent to 'undoing' the swap."""
        first, second = swap
        first_image = key[first]
        second_image = key[second]
        key.forceput(first, second_image)
        key.put(second, first_image)

    def compute_plausibility(self, key: CipherKey) -> Plausibility:
        plaintext = decode(self.ciphertext, key)
        return bigram_plausibility(plaintext, self.reference)

    def print_status(self, iteration: int, printer: Callable[[str], None]) -> None:
        plaintext_preview = decode(self.ciphertext[:25], self.current_key)
        printer(f"epoch {iteration:5}: '{plaintext_preview}...'")

    def step(self) -> None:
        swap = self.random_swap()
        self.apply_swap(swap, self.current_key)
        new_plausibility = self.compute_plausibility(self.current_key)

        def accept() -> None:
            self.current_plausibility = new_plausibility
            self.steps += 1
            self.steps_without_acceptance = 0

        def reject() -> None:
            self.apply_swap(swap, self.current_key)
            self.steps += 1
            self.steps_without_acceptance += 1

        if new_plausibility > self.current_plausibility:
            accept()
            return
        if sysrandom.coin_flip(p=(new_plausibility / self.current_plausibility)):
            accept()
            return

        reject()

    def main_loop(self, printer: Callable[[str], None], threshold: int = 350) -> None:
        while True:
            if self.steps % 100 == 0:
                self.print_status(self.steps, printer)
            if self.steps_without_acceptance >= threshold:
                break
            self.step()

    def many_steps(self, *, count: int) -> None:
        target = self.steps + count
        while self.steps < target:
            self.step()


def maximise_plaintext_plausibility(
    ciphertext: str,
    initial_key: CipherKey,
    reference: BigramProportions = None,
) -> CipherKey:
    maximiser = PlaintextPlausibilityMaximiser(
        ciphertext,
        initial_key,
        reference,
    )
    with Printer() as printer:
        try:
            maximiser.main_loop(printer)
        except KeyboardInterrupt:
            pass
    return maximiser.current_key


__all__ = ("BigramProportions", "Plausibility", "bigram_plausibility", "maximise_plaintext_plausibility",)


def main():
    from .analyser import ciphertext, analyse_character_proportions, infer_cipher_key
    ciphertext_character_frequency = analyse_character_proportions(ciphertext)
    cipher_key = infer_cipher_key(ciphertext_character_frequency)
    better_key = maximise_plaintext_plausibility(ciphertext, cipher_key)
    print(better_key)
    print("".join(better_key[c] for c in ascii_lowercase))


if __name__ == "__main__":
    main()
