from dataclasses import dataclass
import re


# https://github.com/hynek/pem/blob/53484aaeffdf11fa6040866045a7ce6a5d4a94a4/src/pem/_core.py
# See https://tools.ietf.org/html/rfc1421
# and https://datatracker.ietf.org/doc/html/rfc4716 for space instead of fifth dash.
_PEM_RE = re.compile(
    b"""----[- ]BEGIN (?P<identifier>[\\w -]+)[- ]----\r?
(?P<payload>.+?)\r?
----[- ]END (?P=identifier)[- ]----\r?\n?""",
    re.DOTALL,
)


@dataclass
class PemObject:
    identifier: bytes
    content: bytes


def parse(content: str | bytes) -> list[PemObject]:
    if isinstance(content, str):
        content = content.encode()

    return [
        PemObject(match.group("identifier"), match.group("payload"))
        for match in _PEM_RE.finditer(content)
    ]


__all__ = ("PemObject", "parse",)
