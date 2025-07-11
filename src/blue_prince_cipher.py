from string import ascii_lowercase
from typing import Sequence

from blue_prince_numeric_core import numeric_core

ciphertext = """
pigs sand mail date head
clam peak heat joya well
toad card will tape legs
tree road maid slab rock
hand vase safe clay toes
"""
lines = ciphertext.strip().splitlines()
sentences = [line.split() for line in lines]


def digits_from(word: str) -> Sequence[int]:
    return tuple(ascii_lowercase.index(char) + 1 for char in word)


sentences_words_digits = [[digits_from(word) for word in sentence] for sentence in sentences]
sentences_words_numeric_cores = [[numeric_core(digits) for digits in words_digits] for words_digits in sentences_words_digits]
sentences_words_chars = [[ascii_lowercase[numeric_core - 1] for numeric_core in words_numeric_cores] for words_numeric_cores in sentences_words_numeric_cores]
plaintext_words = ["".join(words_chars) for words_chars in sentences_words_chars]


if __name__ == "__main__":
    print(plaintext_words)
    # ['still', 'waler', 'tints', 'blank', 'books']
    # the 'l' is a mistake from the devs
    # correct plaintext: "still water tints blank books"
