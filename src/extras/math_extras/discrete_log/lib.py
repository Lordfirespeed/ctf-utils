from typing import NamedTuple, Self

from toy_cryptography.dh.params import DiffieHellmanParams


class Group(NamedTuple):
    modulus: int
    generator: int
    order: int

    @classmethod
    def from_dhparams(cls, params: DiffieHellmanParams) -> Self:
        return cls(params.prime, params.generator, params.prime - 1)


__all__ = ("Group",)
