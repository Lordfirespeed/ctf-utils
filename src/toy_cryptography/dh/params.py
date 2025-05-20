from dataclasses import dataclass


@dataclass
class DiffieHellmanParams:
    prime: int
    generator: int


__all__ = ("DiffieHellmanParams",)
