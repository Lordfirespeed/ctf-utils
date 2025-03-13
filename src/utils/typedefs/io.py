from _typeshed import SupportsWrite, SupportsFlush


class Writable(SupportsFlush, SupportsWrite):
    pass


__all__ = ("SupportsFlush", "SupportsWrite", "Writable",)
