from collections import UserDict
from collections.abc import ValuesView, KeysView, ItemsView
from typing import Any, Callable, Iterable, Iterator, Mapping, Self, overload, override

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
    def __setitem__(self, key: TKey, value: TValue) -> None:
        if not key in self.data:
            self._order.append(key)
        self.data[key] = value

    def __delitem__(self, key: TKey) -> None:
        if key in self.data:
            index = self._order.index(key)
            del self._order[index]
        del self.data[key]

    @overload
    def __ior__(self, __mapping: SupportsKeysAndGetItem[TKey, TValue]) -> Self: ...
    @overload
    def __ior__(self, __iterable: Iterable[tuple[TKey, TValue]]) -> Self: ...
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

    # region type hints that shouldn't be necessary but are
    def __getitem__(self, item: TKey) -> TValue:
        return super().__getitem__(item)

    @overload
    def get(self, key: TKey, /) -> TValue | None: ...  # noqa
    @overload
    def get(self, key: TKey, default: TValue, /) -> TValue: ...  # noqa
    @overload
    def get[TDefault](self, key: TKey, default: TDefault, /) -> TValue | TDefault: ...  # noqa
    def get(self, key, default = None, /):
        return super().get(key, default=default)
    # endregion

    # region extra features
    @overload
    def sort(self: Mapping[SupportsRichComparisonT, Any], *, key: None = None, reverse: bool = False) -> None: ...
    @overload
    def sort(self, *, key: Callable[[TKey], SupportsRichComparison], reverse: bool = False) -> None: ...
    def sort(self, *, key = None, reverse = False) :
        self._order.sort(key=key, reverse=reverse)

    def sort_by_value(self: "sortabledict[Any, SupportsRichComparisonT]", reverse: bool = False) -> None:
        self.sort(key=self.get, reverse=reverse)
    # endregion

    # region stringify
    def __repr__(self):
        assignments = (f"{key!r}: {value!r}" for key, value in self.items())
        return f"{{{", ".join(assignments)}}}"

    def __str__(self):
        return repr(self)
    # endregion

    # region copy
    @override
    def copy(self):
        return sortabledict(self.data)

    def __copy__(self):
        return self.copy()
    # endregion


__all__ = ("sortabledict",)
