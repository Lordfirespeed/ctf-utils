from .generic import WordList
from random import choices


def random_phrase(word_list: WordList, word_count: int) -> str:
    words = choices(word_list, k=word_count)
    return " ".join(words)


__all__ = ("random_phrase",)
