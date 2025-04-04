from extras.collections_extras import sortabledict


# https://en.wikipedia.org/wiki/Letter_frequency
english_text_letter_frequencies = sortabledict[str, float]({
    "a": 0.082,
    "b": 0.015,
    "c": 0.028,
    "d": 0.043,
    "e": 0.127,
    "f": 0.022,
    "g": 0.020,
    "h": 0.061,
    "i": 0.070,
    "j": 0.0015,
    "k": 0.0077,
    "l": 0.040,
    "m": 0.024,
    "n": 0.067,
    "o": 0.075,
    "p": 0.019,
    "q": 0.00095,
    "r": 0.060,
    "s": 0.063,
    "t": 0.091,
    "u": 0.028,
    "v": 0.0098,
    "w": 0.024,
    "x": 0.0098,
    "y": 0.02,
    "z": 0.074,
})
english_text_letter_frequencies.sort_by_value(reverse=True)


__all__ = ("english_text_letter_frequencies",)
