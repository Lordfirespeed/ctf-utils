from typing import Self

from .printer_abc import PrinterABC


class NoOpPrinter(PrinterABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __call__(self, value: str, *args, **kwargs) -> None:
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
