"""
See: https://docs.python.org/3/library/codecs.html

Particularly:
- https://docs.python.org/3/library/codecs.html#standard-encodings
- https://docs.python.org/3/library/codecs.html#python-specific-encodings
"""
import codecs

from extras.codecs_extras import XKCDScreamCodec


def mix_codecs() -> None:
    print("-- mix codecs --")
    original = u"Bláithín"
    print(f"{original = }")
    utf8_encoded_bytes = codecs.encode(original, "utf-8")
    print(f"{utf8_encoded_bytes = }")
    latin1_decoded = codecs.decode(utf8_encoded_bytes, "latin-1")
    print(f"{latin1_decoded = }")


def search_my_codecs(name: str) -> codecs.CodecInfo | None:
    if name in {"xkcd-scream", "xkcd_scream", "xkcdscream"}:
        codec = XKCDScreamCodec()
        return codecs.CodecInfo(
            name="xkcd-scream",
            encode=codec.encode,
            decode=codec.decode,
        )
    return None


def register_codec_search_function() -> None:
    codecs.register(search_my_codecs)


def use_registered_codec() -> None:
    print("-- use self-registered codec --")
    original = u"fooBARbaz"
    print(f"{original = }")
    scream_encoded_bytes = codecs.encode(original, "xkcd-scream")
    print(f"{scream_encoded_bytes = }")
    scream_encoded = scream_encoded_bytes.decode("utf-8")
    print(f"{scream_encoded = }")
    round_trip = codecs.decode(scream_encoded_bytes, "xkcd-scream")
    print(f"{round_trip = }")


def main():
    mix_codecs()
    register_codec_search_function()
    use_registered_codec()


if __name__ == "__main__":
    main()
