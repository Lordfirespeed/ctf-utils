import codecs
from string import ascii_lowercase, ascii_uppercase
from unicodedata import normalize as normalise

from ugrapheme import graphemes

ascii_lowercase_b_thru_y = ascii_lowercase[1:-1]
ascii_uppercase_b_thru_y = ascii_uppercase[1:-1]

accents_for_b_thru_y = (
    (u"\u0307",),  # B
    (u"\u0327",),  # C
    (u"\u0331", u"\u0332"),  # D
    (u"\u0301",),  # E
    (u"\u032e",),  # F
    (u"\u030b",),  # G
    (u"\u0330",),  # H
    (u"\u0309",),  # I
    (u"\u0313",),  # J
    (u"\u0323",),  # K
    (u"\u0306",),  # L
    (u"\u030c",),  # M
    (u"\u0302",),  # N
    (u"\u030a",),  # O
    (u"\u032f",),  # P
    (u"\u0324",),  # Q
    (u"\u0311",),  # R
    (u"\u0303",),  # S
    (u"\u0304",),  # T
    (u"\u0308",),  # U
    (u"\u0300",),  # V
    (u"\u030f",),  # W
    (u"\u033d",),  # X
    (u"\u0326",),  # Y
)

character_relation = (
    ("A", "A"),
    *((character, f"A{accent}") for character, accents in zip(ascii_uppercase_b_thru_y, accents_for_b_thru_y) for accent in accents),
    ("Z", u"\u023a"),
    ("a", "a"),
    *((character, f"a{accent}") for character, accents in zip(ascii_lowercase_b_thru_y, accents_for_b_thru_y) for accent in accents),
    ("z", u"\u2c65"),
)

normalised_character_relation = tuple(
    (ascii_character, normalise("NFC", scream_assignment)) for ascii_character, scream_assignment in character_relation
)
normalised_character_relation_inverse = (
    (scream_assignment, ascii_character) for ascii_character, scream_assignment in normalised_character_relation
)

screamify_lookup = dict(normalised_character_relation)
unscreamify_lookup = dict(normalised_character_relation_inverse)


def _screamify(value: str) -> bytes:
    input_bytes = bytearray(value, "ascii")
    cursor = 0
    for character in value:
        scream_assignment = screamify_lookup.get(character, None)
        if scream_assignment is None:
            cursor += 1
            continue
        scream_assignment_bytes = scream_assignment.encode("utf-8")
        input_bytes[cursor:cursor+1] = scream_assignment_bytes
        cursor += len(scream_assignment_bytes)
    return bytes(input_bytes)


def _unscreamify(value: bytes | str) -> str:
    if isinstance(value, str):
        value = normalise("NFC", value)
        value_bytes = bytearray(value, "utf-8")
    elif isinstance(value, bytes):
        value_bytes = bytearray(value)
        value = value.decode("utf-8")
    else:
        raise ValueError
    cursor = 0
    for grapheme in graphemes(value):
        grapheme_byte_length = len(grapheme.encode("utf-8"))
        ascii_character = unscreamify_lookup.get(grapheme, None)
        if ascii_character is None:
            cursor += grapheme_byte_length
            continue
        ascii_character_bytes = ascii_character.encode("ascii")
        value_bytes[cursor:cursor+grapheme_byte_length] = ascii_character_bytes
        cursor += 1
    return value_bytes.decode("ascii")


def screamify(value: str) -> str:
    return _screamify(value).decode("utf-8")


def unscreamify(value: str) -> str:
    return _unscreamify(value)


class XKCDScreamCodec(codecs.Codec):
    def encode(self, value: str, errors ="strict") -> (bytes, int):
        return _screamify(value), len(value)

    def decode(self, value: bytes, errors ="strict") -> (str, int):
        return _unscreamify(value), len(value)


__all__ = ("XKCDScreamCodec", "screamify", "unscreamify",)
