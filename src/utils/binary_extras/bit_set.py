# Copyright (c) 2025 Lordfirespeed
# Lordfirespeed licenses the contents of this file to you under the terms of the GPL-2.0-only license.
#
# The contents of this file are largely based on
# https://github.com/openjdk/jdk/blob/f64f22b360f68df68ebb875bd0ef08ba61702952/src/java.base/share/classes/java/util/BitSet.java
# Copyright (c) 1995, 2024, Oracle and/or its affiliates. All rights reserved.
# Oracle and/or its affiliates license the referenced material to Lordfirespeed under the terms of the GPL-2.0-only license.

from operator import index
from typing import (
    ClassVar,
    Iterator,
    Literal,
    Self,
    SupportsIndex,
    overload,
)

from numpy import dtype, ndarray, uint64, zeros as array_of_zeros

from utils.typedefs import SupportsBool

from .bit_twiddling import (
    first_set_bit_index, last_set_bit_index,
)

type NDVector[T] = ndarray[int, dtype[T]]


class BitSet:
    """
    Implements a vector of bits (booleans) that grows as needed. Bits are indexed by integers.
    Indexed bits can be examined, set, or cleared.
    One BitSet may be used to modify the contents of another through logical AND, logical inclusive OR, and
    logical exclusive OR operations.

    By default, all bits are initially unset (zero, False).

    Every BitSet has a current size, which is the number of bits of space it is currently using.
    Note that the size is implementation-specific, so it may vary between implementations.
    The length of a BitSet relates to logical size and is defined implementation-agnostically.

    Unless otherwise noted, passing a `None` parameter to any of the methods in a BitSet will result in a
    TypeError.

    This implementation is not thread-safe; for multithreaded use, ensure access is synchronised.
    """

    address_bits_per_word: ClassVar[int] = 6
    """
    BitSets are packed into arrays of "words." Words are (NumPy) 64-bit unsigned integers, so a 6-bit integer is
    the minimum required to uniquely index a position in a word.
    """
    bits_per_word: ClassVar[int] = 1 << address_bits_per_word
    bit_index_mask: ClassVar[uint64] = uint64(bits_per_word - 1)

    word_mask: ClassVar[uint64] = ~uint64(0)

    # region 'private' implementation details

    @classmethod
    def _word_index(cls, bit_index: int) -> int:
        return bit_index >> cls.address_bits_per_word

    def _recalculate_words_in_use(self) -> None:
        for word_index in reversed(range(self._words_in_use)):
            if self._words[word_index] != 0:
                break
        else:
            self._words_in_use = 0
            return
        self._words_in_use = word_index + 1

    def _ensure_capacity(self, word_count: int) -> None:
        """
        Ensures the BitSet can accommodate the requested word count.
        """
        if len(self._words) >= word_count:
            return

        # double the capacity, or use the requested capacity
        new_word_count = max(2 * len(self._words), word_count)
        # missing entries are initialised to zero when an NDArray is enlarged
        # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.resize.html#numpy.ndarray.resize
        self._words.resize(new_word_count)

    def _expand_to(self, word_index: int) -> None:
        """
        Ensures the BitSet can accommodate a given word index, temporarily violating public-facing invariants.
        The caller must restore the invariants before returning to the user, possibly using _recalculate_words_in_use().
        """
        word_count = word_index + 1
        if self._words_in_use >= word_count:
            return

        self._ensure_capacity(word_count)
        self._words_in_use = word_count

    def _contract_to_fit(self) -> None:
        if self._words_in_use >= len(self._words):
            return
        self._words = self._words.resize(self._words_in_use)

    def _ensure_invariants(self) -> None:
        """
        These 'invariant' properties should be preserved by all public BitSet methods.
        """
        # BitSet should not have capacity for more words than are in use, except when space has been pre-allocated via user request
        assert (self._words_in_use == len(self._words)) or (self._words[self._words_in_use] == 0)
        # BitSet should have capacity for its in-use words
        assert self._words_in_use <= len(self._words)

        if self._words_in_use == 0:
            return

        # the penultimate in-use word should contain a set bit
        assert self._words[self._words_in_use - 1] != 0

    # endregion

    # region 'public' API/dunder methods

    def __init__(self, bit_length: int = None) -> None:
        self._size_is_sticky = bit_length is not None
        """
        Whether the BitSet word-size is user-specified; if so, BitSet should be less inclined to trim to fit,
        as it trusts the user has pre-allocated space intentionally.
        """
        bit_length = bit_length or self.bits_per_word
        word_length = self._word_index(bit_length - 1) + 1
        self._words: NDVector[uint64] = array_of_zeros(word_length, dtype=uint64)
        self._words_in_use = 0

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __copy__(self) -> Self:
        return self.copy()

    def __len__(self) -> int:
        return self.bits_length()

    @overload
    def __getitem__(self, bit_index: SupportsIndex) -> bool: ...

    @overload
    def __getitem__(self, bit_slice: slice) -> Self: ...

    def __getitem__(self, bit_target):
        if isinstance(bit_target, SupportsIndex):
            return self.get(bit_target)
        if isinstance(bit_target, slice):
            return self.get_region(bit_target)
        raise TypeError(f"BitSet indices must be slices or implement __index__, not {type(bit_target).__name__}")

    @overload
    def __setitem__(self, bit_index: SupportsIndex, value: SupportsBool) -> None: ...

    @overload
    def __setitem__(self, bit_slice: slice, value: SupportsBool) -> None: ...

    def __setitem__(self, bit_target, value) -> None:
        if isinstance(bit_target, SupportsIndex):
            return self.set(bit_target, value)
        if isinstance(bit_target, slice):
            return self.set_region(bit_target, value)
        raise TypeError(f"BitSet indices must be slices or implement __index__, not {type(bit_target).__name__}")

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, BitSet):
            return False

        self._ensure_invariants()
        other._ensure_invariants()

        if self._words_in_use != other._words_in_use:
            return False

        for self_word, other_word in zip(self._words, other._words):
            if self_word != other_word:
                return False

        return True

    # endregion

    # region 'public' API/methods/conversions

    def to_bytes(self) -> bytes:
        raise NotImplemented

    def to_byte_array(self) -> bytearray:
        raise NotImplemented

    def copy(self) -> Self:
        raise NotImplemented

    # endregion

    # region 'public' API/methods/assignment operators

    def flip(self, bit_index: SupportsIndex) -> None:
        bit_index = index(bit_index)
        if bit_index < 0:
            bit_index += len(self)
        if bit_index < 0:
            raise IndexError("BitSet index out of range")

        word_index = self._word_index(bit_index)
        self._expand_to(word_index)

        bit_index_in_word = bit_index & self.bit_index_mask
        self._words[word_index] ^= uint64(1) << bit_index_in_word

        self._recalculate_words_in_use()
        self._ensure_invariants()

    def flip_region(self, bit_slice: slice) -> None:
        raise NotImplemented

    def set(self, bit_index: SupportsIndex, value: SupportsBool = True) -> None:
        if value is False:
            return self.clear(bit_index)

        bit_index = index(bit_index)
        if bit_index < 0:
            bit_index += len(self)
        if bit_index < 0:
            raise IndexError("BitSet index out of range")

        word_index = self._word_index(bit_index)
        self._expand_to(word_index)

        bit_index_in_word = bit_index & self.bit_index_mask
        self._words[word_index] |= uint64(1) << bit_index_in_word

    def set_region(self, bit_slice: slice, value: SupportsBool = True) -> None:
        raise NotImplemented

    def clear(self, bit_index: SupportsIndex) -> None:
        bit_index = index(bit_index)
        if bit_index < 0:
            bit_index += len(self)
        if bit_index < 0:
            raise IndexError("BitSet index out of range")

        word_index = self._word_index(bit_index)
        if word_index >= self._words_in_use:
            return

        bit_index_in_word = bit_index & self.bit_index_mask
        self._words[word_index] &= ~(uint64(1) << bit_index_in_word)

        self._recalculate_words_in_use()
        self._ensure_invariants()

    def clear_region(self, bit_slice: slice) -> None:
        raise NotImplemented

    def clear_all(self) -> None:
        # https://stackoverflow.com/a/69890243/11045433
        self._words = array_of_zeros(len(self._words), dtype=uint64)
        self._words_in_use = 0

    # endregion

    # region 'public' API/methods/retrieval operators

    def bits_length(self) -> int:
        """
        Returns the 'logical size' of this BitSet - the index of its highest set bit plus one.
        Returns zero when the BitSet is clear.
        """
        if self._words_in_use == 0:
            return 0

        last_word_length = first_set_bit_index(self._words[self._words_in_use - 1]) + 1
        return (self.bits_per_word * (self._words_in_use - 1)) + last_word_length

    def bits_capacity(self) -> int:
        """
        Returns the number of bits of space in use by this BitSet.
        The maximum element in a BitSet is at index (size - 1).
        """
        return self.bits_per_word * len(self._words)

    def is_empty(self) -> bool:
        return self._words_in_use == 0

    def get(self, bit_index: SupportsIndex) -> bool:
        bit_index = index(bit_index)
        if bit_index < 0:
            bit_index += len(self)
        if bit_index < 0:
            raise IndexError("BitSet index out of range")

        self._ensure_invariants()

        word_index = self._word_index(bit_index)
        if word_index >= self._words_in_use:
            return False
        bit_index_in_word = bit_index & self.bit_index_mask
        masked_word = self._words[word_index] & (uint64(1) << bit_index_in_word)
        return bool(masked_word != 0)

    def get_region(self, bit_slice: slice) -> Self:
        raise NotImplemented

    def next_set_bit_index(self, from_index: SupportsIndex = None) -> int | Literal[-1]:
        """
        Find the index of the next '1' bit, starting from from_index (inclusive).
        """
        if from_index is None:
            from_index = 0
        from_index = index(from_index)
        if from_index < 0:
            from_index += len(self)
        if from_index < 0:
            raise IndexError("BitSet index out of range")

        self._ensure_invariants()

        word_index = self._word_index(from_index)
        if word_index >= self._words_in_use:
            return -1

        from_index_in_word = from_index & self.bit_index_mask
        word = self._words[word_index] & (self.word_mask << from_index_in_word)

        while True:
            if word != 0:
                return (word_index * self.bits_per_word) + last_set_bit_index(word)
            word_index += 1
            if word_index >= self._words_in_use:
                return -1
            word = self._words[word_index]

    def next_clear_bit_index(self, from_index: SupportsIndex = None) -> int:
        """
        Find the index of the next '0' bit, starting from from_index (inclusive).
        """
        if from_index is None:
            from_index = 0
        from_index = index(from_index)
        if from_index < 0:
            from_index += len(self)
        if from_index < 0:
            raise IndexError("BitSet index out of range")

        self._ensure_invariants()

        word_index = self._word_index(from_index)
        if word_index >= self._words_in_use:
            return from_index

        from_index_in_word = from_index & self.bit_index_mask
        word = ~(self._words[word_index]) & (self.word_mask << from_index_in_word)

        while True:
            if word != 0:
                return (word_index * self.bits_per_word) + last_set_bit_index(word)
            word_index += 1
            if word_index >= self._words_in_use:
                return word_index * self.bits_per_word
            word = ~(self._words[word_index])

    def previous_set_bit_index(self, from_index: SupportsIndex = None) -> int | Literal[-1]:
        """
        Find the index of the previous '1' bit, starting from from_index (exclusive).
        """
        if from_index is None:
            return len(self) - 1
        from_index = index(from_index)
        if from_index < 0:
            from_index += len(self)
        if from_index < 0:
            raise IndexError("BitSet index out of range")

        self._ensure_invariants()

        word_index = self._word_index(from_index)
        if word_index >= self._words_in_use:
            return len(self) - 1

        from_index_in_word = from_index & self.bit_index_mask
        word = self._words[word_index] & (self.word_mask >> (self.bits_per_word - from_index_in_word))

        while True:
            if word != 0:
                return (word_index * self.bits_per_word) + first_set_bit_index(word)
            word_index -= 1
            if word_index < 0:
                return -1
            word = self._words[word_index]

    def previous_clear_bit_index(self, from_index: SupportsIndex = None) -> int | Literal[-1]:
        """
        Find the index of the previous '0' bit, starting from from_index (exclusive).
        """
        if from_index is None:
            from_index = len(self)
        from_index = index(from_index)
        if from_index < 0:
            from_index += len(self)
        if from_index < 0:
            raise IndexError("BitSet index out of range")

        self._ensure_invariants()

        word_index = self._word_index(from_index)
        from_index_in_word = from_index & self.bit_index_mask
        if word_index >= self._words_in_use and from_index_in_word > 0:
            return from_index - 1
        elif word_index == self._words_in_use:
            word = 0
        else:
            word = ~self._words[word_index] & (self.word_mask >> (self.bits_per_word - from_index_in_word))

        while True:
            if word != 0:
                return (word_index * self.bits_per_word) + first_set_bit_index(word)
            word_index -= 1
            if word_index < 0:
                return -1
            word = ~self._words[word_index]

    def intersects(self, other: Self) -> bool:
        """
        Returns true if this BitSet has any set bits in common with the specified BitSet.
        Otherwise, returns False.
        """
        raise NotImplemented

    def cardinality(self) -> int:
        """
        Returns the number of set bits in this BitSet.
        """
        raise NotImplemented

    # endregion

    # region 'public' API/methods/binary operators

    def and_update(self, other: Self) -> None:
        raise NotImplemented

    def or_update(self, other: Self) -> None:
        raise NotImplemented

    def xor_update(self, other: Self) -> None:
        raise NotImplemented

    def difference_update(self, other: Self) -> None:
        raise NotImplemented

    def symmetric_difference_update(self, other: Self) -> None:
        raise NotImplemented

    # endregion

    # region 'public' API/methods/iterators

    def boolean_values(self) -> Iterator[bool]:
        cursor = 0
        while True:
            if cursor >= len(self):
                return
            yield self[cursor]
            cursor += 1

    def set_bit_indices(self) -> Iterator[int]:
        cursor = 0
        while True:
            set_bit_index = self.next_set_bit_index(cursor)
            if set_bit_index == -1:
                return
            cursor = set_bit_index + 1
            yield set_bit_index

    def clear_bit_indices(self) -> Iterator[int]:
        cursor = 0
        while True:
            clear_bit_index = self.next_clear_bit_index(cursor)
            if clear_bit_index >= len(self):
                return
            cursor = clear_bit_index + 1
            yield clear_bit_index

    # endregion


__all__ = ("BitSet",)
