"""
See
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands
"""

escape = b"\x1b"
"""all escape sequences are prefixed with `ESC`."""

control_sequence_introducer = escape + b"["
"""most useful escape sequences begin with `ESC [`, the 'CSI', and are terminated by a byte in the range 0x40-0x7E."""

delimiter = b";"
"""escape sequence arguments are semicolon-delimited."""

__all__ = (
    "escape",
    "control_sequence_introducer",
    "delimiter",
)
