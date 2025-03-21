from collections import UserDict
from collections.abc import ValuesView, KeysView, ItemsView
from typing import Any, Callable, Iterable, Iterator, Mapping, Self, overload

from utils.typedefs import (
    SupportsKeysAndGetItem,
    SupportsRichComparison,
    SupportsRichComparisonT,
)


class sortabledict_keys[TKey, TValue](KeysView[TKey, TValue]):
    _mapping: "sortabledict[TKey, TValue]"

    def __init__(self, mapping: "sortabledict[TKey, TValue]"):
        assert isinstance(mapping, sortabledict)
        super().__init__(mapping)

    def __iter__(self) -> Iterator[TKey]:
        yield from self._mapping._order

    def __reversed__(self) -> Iterator[TKey]:
        yield from reversed(self._mapping._order)


class sortabledict_values[TKey, TValue](ValuesView[TKey, TValue]):
    _mapping: "sortabledict[TKey, TValue]"

    def __init__(self, mapping: "sortabledict[TKey, TValue]"):
        assert isinstance(mapping, sortabledict)
        super().__init__(mapping)

    def __iter__(self) -> Iterator[TValue]:
        for key in self._mapping._order:
            yield self._mapping[key]

    def __reversed__(self) -> Iterator[TValue]:
        for key in reversed(self._mapping._order):
            yield self._mapping[key]


class sortabledict_items[TKey, TValue](ItemsView[TKey, TValue]):
    _mapping: "sortabledict[TKey, TValue]"

    def __init__(self, mapping: "sortabledict[TKey, TValue]"):
        assert isinstance(mapping, sortabledict)
        super().__init__(mapping)

    def __iter__(self) -> Iterator[tuple[TKey, TValue]]:
        for key in self._mapping._order:
            yield key, self._mapping[key]

    def __reversed__(self) -> Iterator[tuple[TKey, TValue]]:
        for key in reversed(self._mapping._order):
            yield key, self._mapping[key]


class sortabledict[TKey, TValue](UserDict[TKey, TValue]):
    _order: list[TKey]

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self: dict[str, TValue], /, **kwargs: TValue) -> None: ...
    @overload
    def __init__(self, __map: SupportsKeysAndGetItem[TKey, TValue]) -> None: ...
    @overload
    def __init__(self: dict[str, TValue], __map: SupportsKeysAndGetItem[str, TValue], /, **kwargs: TValue) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[tuple[TKey, TValue]]) -> None: ...
    @overload
    def __init__(self: dict[str, TValue], __iterable: Iterable[tuple[str, TValue]], /, **kwargs: TValue) -> None: ...
    def __init__(self, data = None, /, **kwargs) -> None:
        self._order = []
        super().__init__(data, **kwargs)

    # region modification (UserDict)
    def __setitem__(self, key, value) -> None:
        if not key in self.data:
            self._order.append(key)
        self.data[key] = value

    def __delitem__(self, key) -> None:
        if key in self.data:
            index = self._order.index(key)
            del self._order[index]
        del self.data[key]

    def __ior__(self, other) -> Self:
        self.update(other)
        return self
    # endregion

    # region views/iteration
    def __iter__(self):
        return iter(self.keys())

    def keys(self):
        # todo: the 'keys' view should also implement a semi-mutable list view interface
        # re-ordering should be permitted but e.g. deletion, insertion, replacement forbidden
        return sortabledict_keys(self)

    def values(self):
        return sortabledict_values(self)

    def items(self):
        return sortabledict_items(self)
    # endregion

    # region extra features
    @overload
    def sort(self: Mapping[SupportsRichComparisonT, Any], *, key: None = None, reverse: bool = False) -> None: ...
    @overload
    def sort(self, *, key: Callable[[TKey], SupportsRichComparison], reverse: bool = False) -> None: ...
    def sort(self, *, key = None, reverse = False) :
        self._order.sort(key=key, reverse=reverse)
    # endregion


__all__ = ("sortabledict",)
