# The contents of this file are largely based upon
# https://github.com/tqdm/tqdm/blob/0ed5d7f18fa3153834cbac0aa57e8092b217cc16/tqdm/tqdm.py
# Copyright 2015-2024 (c) Casper da Costa-Luis
# The referenced materials are licensed to Lordfirespeed under the terms of the MPL-2.0 license.

import sys
from typing import Never, Self

from utils.ansi import EscapeBuilder
from utils.ansi.control_sequence_terminators import cursor_up, cursor_down
from utils.typedefs import Writable, SupportsWrite

from .utils import disp_len
from .printer_abc import PrinterABC


class Printer(PrinterABC):
    """
    Manage the printing and in-place updating of some lines of characters.
    """

    def __init__(
        self,
        writable: Never | "SupportsWrite" | "Writable" = None,
        line_count: int = 1,
    ) -> None:
        if writable is None:
            writable = sys.stderr

        self.writable = writable
        self.flush = getattr(writable, "flush", lambda: None)
        if writable in (sys.stderr, sys.stdout):
            getattr(sys.stderr, 'flush', lambda: None)()
            getattr(sys.stdout, 'flush', lambda: None)()

        self.line_count = line_count

        self.last_len = 0
        self.alive = False

    def _write(self, value: str) -> None:
        self.writable.write(value)
        self.flush()

    def _print(self, value: str) -> None:
        len_value = disp_len(value)
        padding = " " * max(self.last_len - len_value, 0)
        self._write(f"\r{value}{padding}")
        self.last_len = len_value

    def _move_cursor_relatively(self, n: int | None) -> None:
        if n is None:
            return
        if n == 0:
            return
        if n > 5:
            # use control sequence to save bytes written
            control_sequence = EscapeBuilder() \
                .argue(n) \
                .finalize(cursor_down)
            # including content (the `\r`) is necessary, otherwise the cursor won't move onto the blank line
            self.writable.write(control_sequence + "\r")
            return
        if n > 0:
            # move cursor down by n lines using only newlines
            self.writable.write("\n" * n)
            return
        if n < 0:
            control_sequence = EscapeBuilder() \
                .argue(-n) \
                .finalize(cursor_up)
            self.writable.write(control_sequence)
            return

    def __call__(self, value: str, *, line_index: int = None):
        if not self.alive:
            raise Exception("Printer has not been opened")
        if line_index is None and (self.line_count == 1):
            line_index = 0
        if line_index is None:
            raise Exception("line position must be specified")
        if line_index < 0 or self.line_count <= line_index:
            raise Exception("specified line position is out of range")

        line_relative_position = -self.line_count + line_index
        self._move_cursor_relatively(line_relative_position)
        self._print(value)
        self._move_cursor_relatively(-line_relative_position)

    def open(self) -> None:
        self.alive = True
        self.writable.write('\n' * self.line_count)

    def close(self) -> None:
        self.alive = False

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


__all__ = ("Printer",)
