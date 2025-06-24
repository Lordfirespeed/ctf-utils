import asyncio
import csv
import itertools
from typing import NewType

from gmpy2 import mpq

from definitions import project_cache_dirname
from extras.collections_extras import sortabledict
from utils.data import word_list
from utils.data.bigrams import load_lowercase_bigrams_dataset


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


"""
this models the combination lock whose passcode we wish to crack.

each entry should be an iterable of allowed characters for the corresponding character position in the lock's passcode.

this program is unlikely to be helpful for cracking locks which permit entry of any alphabetical character in all
positions; it's most applicable when a lock only permits entry of a small subset of characters in each position.
"""
letter_options = [
    "MWBCPTLS",
    "IOUHRTAE",
    "RNTSOIVL",
    "DTHSIKVA",
    "AEONLRCS",
    "NDGRWTEY",
]

async def main():
    async with word_list("english-words") as english_words:
        potential_words = set(word for word in english_words if len(word) == len(letter_options))

    letter_combinations = ("".join(letters).lower() for letters in itertools.product(*letter_options))
    words = [combination for combination in letter_combinations if combination in potential_words]
    words.sort(key=bigram_plausibility, reverse=True)

    with open(project_cache_dirname/"alphabetical-combination-lock-crack-results.txt", "w", newline="") as results_handle:
        results_writer = csv.writer(results_handle, quoting=csv.QUOTE_NONE)
        for word in words:
            results_writer.writerow((word,))


if __name__ == "__main__":
    asyncio.run(main())
