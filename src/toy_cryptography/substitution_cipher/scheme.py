from bidict import bidict
from utils.typedefs import Bidict


type CipherKey = Bidict[str, str]


def encode(plaintext: str, key: CipherKey) -> str:
    assert plaintext.encode("ascii")
    result = bytearray(len(plaintext))
    cursor = 0
    while cursor < len(plaintext):
        character = plaintext[cursor]
        cipher_character = key.get(character, None)

        if cipher_character is None:
            result[cursor:cursor+1] = character.encode("ascii")
            cursor += 1
            continue

        result[cursor:cursor+1] = cipher_character.encode("ascii")
        cursor += 1

    return result.decode("ascii")


def decode(ciphertext: str, key: CipherKey) -> str:
    return encode(ciphertext, key.inverse)


def update_key(sink: CipherKey, source: CipherKey) -> CipherKey:
    sink = bidict(sink)
    for key, value in source.items():
        old_value = sink[key]
        old_key = sink.inverse[value]
        sink.forceput(key, value)
        sink.put(old_key, old_value)
    return sink


__all__ = ("CipherKey", "encode", "decode", "update_key")
