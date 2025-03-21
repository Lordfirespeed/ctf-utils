from .shed import SupportsWrite, SupportsFlush


class Writable(SupportsFlush, SupportsWrite):
    pass


__all__ = ("Writable",)
