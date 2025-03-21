from collections import UserDict
from collections.abc import ValuesView, KeysView, ItemsView
from typing import Any, Callable, Hashable, Iterator, Mapping, Self, overload

from utils.typedefs import SupportsRichComparison, SupportsRichComparisonT


class SortableDictKeysView[TKey, TValue](KeysView[TKey, TValue]):
    _mapping: "SortableDict[TKey, TValue]"

    def __init__(self, mapping: "SortableDict[TKey, TValue]"):
        assert isinstance(mapping, SortableDict)
        super().__init__(mapping)

    def __iter__(self) -> Iterator[TKey]:
        yield from self._mapping._order

    def __reversed__(self) -> Iterator[TKey]:
        yield from reversed(self._mapping._order)


class SortableDictValuesView[TKey, TValue](ValuesView[TKey, TValue]):
    _mapping: "SortableDict[TKey, TValue]"

    def __init__(self, mapping: "SortableDict[TKey, TValue]"):
        assert isinstance(mapping, SortableDict)
        super().__init__(mapping)

    def __iter__(self) -> Iterator[TValue]:
        for key in self._mapping._order:
            yield self._mapping[key]

    def __reversed__(self) -> Iterator[TValue]:
        for key in reversed(self._mapping._order):
            yield self._mapping[key]


class SortableDictItemsView[TKey, TValue](ItemsView[TKey, TValue]):
    _mapping: "SortableDict[TKey, TValue]"

    def __init__(self, mapping: "SortableDict[TKey, TValue]"):
        assert isinstance(mapping, SortableDict)
        super().__init__(mapping)

    def __iter__(self) -> Iterator[tuple[TKey, TValue]]:
        for key in self._mapping._order:
            yield key, self._mapping[key]

    def __reversed__(self) -> Iterator[tuple[TKey, TValue]]:
        for key in reversed(self._mapping._order):
            yield key, self._mapping[key]


class SortableDict[TKey: Hashable, TValue](UserDict[TKey, TValue]):
    _order: list[TKey]

    def __init__(self, data=None, /, **kwargs) -> None:
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
        return SortableDictKeysView(self)

    def values(self):
        return SortableDictValuesView(self)

    def items(self):
        return SortableDictItemsView(self)
    # endregion

    # region extra features
    @overload
    def sort(self: Mapping[SupportsRichComparisonT, Any], *, key: None = None, reverse: bool = False) -> None: ...
    @overload
    def sort(self, *, key: Callable[[TKey], SupportsRichComparison], reverse: bool = False) -> None: ...
    def sort(self, *, key = None, reverse = False) :
        self._order.sort(key=key, reverse=reverse)
    # endregion


__all__ = ("SortableDict",)
