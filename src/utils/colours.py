"""
See https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
Note 0x1b = 27, the ASCII character ordinal for 'Escape'.
"""

pink = "\x1b[95m"
reset = "\x1b[0m"

__all__ = ("pink", "reset",)
