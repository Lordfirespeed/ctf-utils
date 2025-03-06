import codecs
from binascii import hexlify, unhexlify


def to_hex_by_global_function() -> None:
    """
    https://docs.python.org/3/library/functions.html#hex
    """
    assert hex(0xffab12) == "0xffab12"


def to_hex_by_format_string() -> None:
    """
    https://docs.python.org/3/library/string.html#formatspec
    """
    assert f"{0xffab12:x}" == "ffab12"
    assert f"{0xffab12:#x}" == "0xffab12"
    assert f"{0xffab12:X}" == "FFAB12"
    assert f"{0xffab12:#X}" == "0XFFAB12"


def to_hex_by_bytes_instance_method() -> None:
    """
    https://docs.python.org/3/library/stdtypes.html#bytes.hex
    """
    assert b"\xff\xab\x12".hex() == "ffab12"


def from_hex_by_bytes_static_method() -> None:
    """
    https://docs.python.org/3/library/stdtypes.html#bytes.fromhex
    """
    assert bytes.fromhex("ffab12") == b"\xff\xab\x12"
    assert bytes.fromhex("Ff \n\t    aB \r12") == b"\xff\xab\x12"


def to_hex_by_binascii() -> None:
    """
    https://docs.python.org/3/library/binascii.html#binascii.hexlify
    """
    assert hexlify(b"\xff\xab\x12") == b"ffab12"


def from_hex_by_binascii() -> None:
    """
    https://docs.python.org/3/library/binascii.html#binascii.unhexlify
    """
    assert unhexlify("ffab12") == b"\xff\xab\x12"
    assert unhexlify(b"ffab12") == b"\xff\xab\x12"


def to_hex_by_codecs() -> None:
    """
    https://docs.python.org/3/library/codecs.html#binary-transforms
    Behaviour should exactly match `hexlify`
    """
    assert codecs.encode(b"\xff\xab\x12", "hex") == b"ffab12"


def from_hex_by_codecs() -> None:
    """
    https://docs.python.org/3/library/codecs.html#binary-transforms
    Behaviour should exactly match `unhexlify`
    """
    assert codecs.decode("ffab12", "hex") == b"\xff\xab\x12"
    assert codecs.decode(b"ffab12", "hex") == b"\xff\xab\x12"



def main() -> None:
    to_hex_by_global_function()
    to_hex_by_format_string()
    to_hex_by_bytes_instance_method()
    from_hex_by_bytes_static_method()
    to_hex_by_binascii()
    from_hex_by_binascii()
    to_hex_by_codecs()
    from_hex_by_codecs()


if __name__ == "__main__":
    main()
