from abc import ABC, abstractmethod
from typing import Self


class PrinterABC(ABC):
    @abstractmethod
    def __call__(self, value: str) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


__all__ = ("PrinterABC",)
