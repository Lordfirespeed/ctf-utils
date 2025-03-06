from abc import abstractmethod
from typing import Protocol

__all__ = (
    "SupportsBool",
    "SupportsCopy",
)


class SupportsBool(Protocol):
    """An ABC with one abstract method __bool__."""

    __slots__ = ()

    @abstractmethod
    def __bool__(self) -> bool:
        pass


class SupportsCopy(Protocol):
    """An ABC with one abstract method __copy__."""

    __slots__ = ()

    @abstractmethod
    def __copy__[T](self: T) -> T:
        pass
