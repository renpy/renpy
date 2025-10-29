# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains code that handles the execution of python code
# contained within the script file. It also handles rolling back the
# game state to some time in the past.

from typing import AbstractSet, Any, TYPE_CHECKING, Callable, Iterable, Protocol, SupportsIndex, overload

import __future__

import random
import weakref
import copyreg
import functools

import renpy

# A set of flags that indicate dict should run in future-compatible mode.
FUTURE_FLAGS = __future__.division.compiler_flag | __future__.with_statement.compiler_flag

##############################################################################
# Monkeypatch copy_reg to work around a change in the class that RevertableSet
# is based on.


def _reconstructor(cls, base, state):
    if (cls is RevertableSet) and (base is object):
        base = set
        state = []

    if base is object:
        obj = object.__new__(cls)
    else:
        obj = base.__new__(cls, state)  # type: ignore
        if base.__init__ != object.__init__:
            base.__init__(obj, state)

    return obj


copyreg._reconstructor = _reconstructor  # type: ignore

mutate_flag: bool = True
"""
This is set to True whenever a mutation occurs. The background save code uses
this to check to see if store has changed after save started.
"""


def mutator(method):
    @functools.wraps(method)
    def do_mutation(self, *args, **kwargs):
        global mutate_flag

        mutated = renpy.game.log.mutated

        if id(self) not in mutated:
            mutated[id(self)] = (weakref.ref(self), self._clean())
            mutate_flag = True

        return method(self, *args, **kwargs)

    return do_mutation


class CompressedList:
    """
    Compresses the changes in a queue-like list. What this does is to try
    to find a central sub-list for which has objects in both lists. It
    stores the location of that in the new list, and then elements before
    and after in the sub-list.

    This only really works if the objects in the list are unique, but the
    results are efficient even if this doesn't work.
    """

    pre: list[Any]
    start: int
    end: int
    post: list[Any]

    def __init__(self, old: list[Any], new: list[Any]):
        # Pick out a pivot element near the center of the list.
        new_center = (len(new) - 1) // 2
        new_pivot = new[new_center]

        # Find an element in the old list corresponding to the pivot.
        old_half = (len(old) - 1) // 2

        for i in range(0, old_half + 1):
            if old[old_half - i] is new_pivot:
                old_center = old_half - i
                break

            if old[old_half + i] is new_pivot:
                old_center = old_half + i
                break
        else:
            # If we couldn't, give up.
            self.pre = old
            self.start = 0
            self.end = 0
            self.post = []

            return

        # Figure out the position of the overlap in the center of the two lists.
        new_start = new_center
        new_end = new_center + 1

        old_start = old_center
        old_end = old_center + 1

        len_new = len(new)
        len_old = len(old)

        while new_start and old_start and (new[new_start - 1] is old[old_start - 1]):
            new_start -= 1
            old_start -= 1

        while (new_end < len_new) and (old_end < len_old) and (new[new_end] is old[old_end]):
            new_end += 1
            old_end += 1

        # Now that we have this, we can put together the object.
        self.pre = list.__getitem__(old, slice(0, old_start))
        self.start = new_start
        self.end = new_end
        self.post = list.__getitem__(old, slice(old_end, len_old))

    def decompress(self, new: list[Any]) -> list[Any]:
        return self.pre + new[self.start : self.end] + self.post

    def __repr__(self):
        return f"<CompressedList {self.pre} [{self.start}:{self.end}] {self.post}>"


class RevertableList[T](list[T]):
    if not TYPE_CHECKING:

        def __init__(self, *args):
            log = renpy.game.log

            if log is not None:
                log.mutated[id(self)] = None

            list.__init__(self, *args)

        __delitem__ = mutator(list.__delitem__)
        __setitem__ = mutator(list.__setitem__)
        __iadd__ = mutator(list.__iadd__)
        __imul__ = mutator(list.__imul__)
        append = mutator(list.append)
        extend = mutator(list.extend)
        insert = mutator(list.insert)
        pop = mutator(list.pop)
        remove = mutator(list.remove)
        reverse = mutator(list.reverse)
        sort = mutator(list.sort)

    def __add__[S](self, other: list[S]) -> "RevertableList[T | S]":
        # Python list would raise if other is not a list.
        return RevertableList(super().__add__(other))

    # FIXME: No __radd__ method here, which probably is incorrect.

    def __mul__(self, other: SupportsIndex) -> "RevertableList[T]":
        # Python list would raise if other could not be converted to int.
        return RevertableList(super().__mul__(other))

    def __rmul__(self, other: SupportsIndex) -> "RevertableList[T]":
        # Python list would raise if other could not be converted to int.
        return RevertableList(super().__rmul__(other))

    @overload
    def __getitem__(self, index: SupportsIndex) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> "RevertableList[T]": ...

    def __getitem__(self, index: SupportsIndex | slice):
        if isinstance(index, slice):
            return RevertableList(super().__getitem__(index))
        else:
            return super().__getitem__(index)

    def copy(self) -> "RevertableList[T]":
        return self[:]

    def clear(self):
        del self[:]

    def _clean(self):
        """
        Gets a clean copy of this object before any mutation occurs.
        """

        return self[:]

    def _compress(self, clean):
        """
        Takes a clean copy of this object, compresses it, and returns compressed
        information that can be passed to rollback.
        """

        if not self or not clean:
            return clean

        if renpy.config.list_compression_length is None:
            return clean

        if len(self) < renpy.config.list_compression_length or len(clean) < renpy.config.list_compression_length:
            return clean

        return CompressedList(clean, self)

    def _rollback(self, compressed):
        """
        Rolls this object back, using the information created by _compress.

        Since compressed can come from a save file, this method also has to
        recognize and deal with old data.
        """

        if isinstance(compressed, CompressedList):
            self[:] = compressed.decompress(self)
        else:
            self[:] = compressed


if TYPE_CHECKING:

    @overload
    def revertable_range(start: SupportsIndex, /) -> RevertableList[int]: ...

    @overload
    def revertable_range(
        start: SupportsIndex, stop: SupportsIndex, step: SupportsIndex = ..., /
    ) -> RevertableList[int]: ...

    class SupportsDunderLT(Protocol):
        def __lt__(self, other: Any, /) -> bool: ...

    class SupportsDunderGT(Protocol):
        def __gt__(self, other: Any, /) -> bool: ...

    type SupportsRichComparison = SupportsDunderLT | SupportsDunderGT

    @overload
    def revertable_sorted[T: SupportsRichComparison](
        iterable: Iterable[T],
        /,
        *,
        key: None = None,
        reverse: bool = False,
    ) -> RevertableList[T]: ...
    @overload
    def revertable_sorted[T](
        iterable: Iterable[T],
        /,
        *,
        key: Callable[[T], SupportsRichComparison],
        reverse: bool = False,
    ) -> RevertableList[T]: ...


def revertable_range(*args):
    return RevertableList(range(*args))


def revertable_sorted(*args, **kwargs):
    return RevertableList(sorted(*args, **kwargs))


class RevertableDict[KT, VT](dict[KT, VT]):
    if not TYPE_CHECKING:

        def __init__(self, *args, **kwargs):
            log = renpy.game.log

            if log is not None:
                log.mutated[id(self)] = None

            dict.__init__(self, *args, **kwargs)

        __delitem__ = mutator(dict.__delitem__)
        __setitem__ = mutator(dict.__setitem__)
        clear = mutator(dict.clear)
        pop = mutator(dict.pop)
        popitem = mutator(dict.popitem)
        setdefault = mutator(dict.setdefault)
        update = mutator(dict.update)

        itervalues = dict.values
        iterkeys = dict.keys
        iteritems = dict.items

        def has_key(self, key):
            return key in self

    def __or__[KT2, VT2](self, other: dict[KT2, VT2]) -> "RevertableDict[KT | KT2, VT | VT2]":
        if not isinstance(other, dict):
            return NotImplemented

        return RevertableDict(super().__or__(other))

    def __ror__[KT2, VT2](self, other: dict[KT2, VT2]) -> "RevertableDict[KT | KT2, VT | VT2]":
        if not isinstance(other, dict):
            return NotImplemented

        return RevertableDict(super().__ror__(other))

    def __ior__(self, other: dict[KT, VT] | Iterable[tuple[KT, VT]]) -> "RevertableDict[KT, VT]":
        self.update(other)
        return self

    def copy(self) -> "RevertableDict[KT, VT]":
        rv = RevertableDict()
        rv.update(self)
        return rv

    def _clean(self):
        return list(self.items())

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        self.clear()

        for k, v in compressed:
            self[k] = v


class RevertableDefaultDict[KT, VT](RevertableDict[KT, VT]):
    """
    :doc: rollbackclasses
    :name: defaultdict
    :args: (default_factory, /, *args, **kwargs)

    This is a revertable version of collections.defaultdict. It takes a
    factory function. If a key is accessed that does not exist, the `default_factory`
    function is called with the key as an argument, and the result is
    returned.

    While the default_factory attribute is present on this object, it does not
    participate in rollback, and so should not be changed.
    """

    default_factory: Callable[[], VT] | None

    # Typeshed actually have more correct overloads, but for our case, we only
    # care about str: VT when kwargs are present, and KT: VT if not.
    @overload
    def __init__(
        self: "RevertableDefaultDict[str, VT]",  # pyright: ignore[reportInvalidTypeVarUse]
        default_factory: Callable[[], VT] | None = None,
        iterable: dict[str, VT] | Iterable[tuple[str, VT]] = (),
        /,
        **kwargs: VT,
    ): ...

    @overload
    def __init__(
        self,
        default_factory: Callable[[], VT] | None = None,
        iterable: dict[KT, VT] | Iterable[tuple[KT, VT]] = (),
        /,
    ): ...

    def __init__(self, default_factory=None, *args, **kwargs):
        self.default_factory = default_factory
        super(RevertableDefaultDict, self).__init__(*args, **kwargs)

    def __missing__(self, key) -> VT:
        if self.default_factory is None:
            raise KeyError(key)

        rv = self.default_factory()
        self[key] = rv
        return rv


class RevertableSet[T](set[T]):
    def __setstate__(self, state):
        if isinstance(state, tuple):
            self.update(state[0].keys())
        else:
            self.update(state)

    def __getstate__(self):
        rv = ({i: True for i in self},)
        return rv

    # Required to ensure that getstate and setstate are called.
    __reduce__ = object.__reduce__
    __reduce_ex__ = object.__reduce_ex__

    if not TYPE_CHECKING:

        def __init__(self, *args):
            log = renpy.game.log

            if log is not None:
                log.mutated[id(self)] = None

            set.__init__(self, *args)

        __iand__ = mutator(set.__iand__)
        __ior__ = mutator(set.__ior__)
        __isub__ = mutator(set.__isub__)
        __ixor__ = mutator(set.__ixor__)
        add = mutator(set.add)
        clear = mutator(set.clear)
        difference_update = mutator(set.difference_update)
        discard = mutator(set.discard)
        intersection_update = mutator(set.intersection_update)
        pop = mutator(set.pop)
        remove = mutator(set.remove)
        symmetric_difference_update = mutator(set.symmetric_difference_update)
        union_update = mutator(set.update)
        update = mutator(set.update)

    # Wrap return set into RevertableSet for creator methods.
    def __and__(self, other: AbstractSet[Any]) -> "RevertableSet[T]":
        rv = super().__and__(other)
        if isinstance(rv, set):
            return RevertableSet(rv)
        else:
            return rv

    def __or__[T2](self, other: AbstractSet[T2]) -> "RevertableSet[T | T2]":
        rv = super().__or__(other)
        if isinstance(rv, set):
            return RevertableSet(rv)
        else:
            return rv

    def __sub__(self, other: AbstractSet[Any]) -> "RevertableSet[T]":
        rv = super().__sub__(other)
        if isinstance(rv, set):
            return RevertableSet(rv)
        else:
            return rv

    def __xor__[T2](self, other: AbstractSet[T2]) -> "RevertableSet[T | T2]":
        rv = super().__xor__(other)
        if isinstance(rv, set):
            return RevertableSet(rv)
        else:
            return rv

    # FIXME: No __r...__ methods here, which probably is incorrect.

    def copy(self) -> "RevertableSet[T]":
        return RevertableSet(self)

    def difference(self, *s: Iterable[Any]) -> "RevertableSet[T]":
        return RevertableSet(super().difference(*s))

    def intersection(self, *s: Iterable[Any]) -> "RevertableSet[T]":
        return RevertableSet(super().intersection(*s))

    def symmetric_difference(self, s: Iterable[Any]) -> "RevertableSet[T]":
        return RevertableSet(super().symmetric_difference(s))

    def union(self, *s: Iterable[Any]) -> "RevertableSet[T]":
        return RevertableSet(super().union(*s))

    def _clean(self):
        return list(self)

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        set.clear(self)
        set.update(self, compressed)


class RevertableObject:
    # All RenPy's objects have  __dict__, so _rollback is fast, i.e
    # one update, not iterating over all attributes.
    # __weakref__ should exist, so mutator can work.
    # Other slots are forbidden because they cannot be reverted in easy way.
    # For more details, see https://github.com/renpy/renpy/pull/3282
    # __slots__ = ("__weakref__", "__dict__")

    if not TYPE_CHECKING:

        def __new__(cls, *args, **kwargs):
            self = super(RevertableObject, cls).__new__(cls)

            log = renpy.game.log
            if log is not None:
                log.mutated[id(self)] = None

            return self

        def __init__(self, *args, **kwargs):
            if (args or kwargs) and renpy.config.developer:
                raise TypeError("object() takes no parameters.")

    def __init_subclass__(cls):
        if renpy.config.developer and "__slots__" in cls.__dict__:
            raise TypeError(
                "Classes with __slots__ do not support rollback. "
                "To create a class with slots, inherit from python_object instead."
            )

        super().__init_subclass__()

    if not TYPE_CHECKING:
        __setattr__ = mutator(object.__setattr__)
        __delattr__ = mutator(object.__delattr__)

    def _clean(self):
        return self.__dict__.copy()

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        self.__dict__.clear()
        self.__dict__.update(compressed)


class MultiRevertable:
    """
    :doc: rollbackclasses
    :name: MultiRevertable

    MultiRevertable is a mixin class that allows an object to inherit
    from more than one kind of revertable object. To use it, from MultiRevertable,
    then from the revertable classes you want to inherit from.

    For example::

        class MyDict(MultiRevertable, dict, object):
            pass

    will create an class that will rollback both its dict contents and
    object fields.
    """

    def _rollback_types(self):
        rv = []

        for i in self.__class__.__mro__:
            if i is MultiRevertable:
                continue

            if "_rollback" in i.__dict__:
                rv.append(i)

        return rv

    def _clean(self):
        return tuple(i._clean(self) for i in self._rollback_types())

    def _compress(self, clean):
        return tuple(i._compress(self, c) for i, c in zip(self._rollback_types(), clean))

    def _rollback(self, compressed):
        for i, c in zip(self._rollback_types(), compressed):
            i._rollback(self, c)


def checkpointing(method):
    @functools.wraps(method)
    def do_checkpoint(self, *args, **kwargs):
        renpy.game.context().force_checkpoint = True

        return method(self, *args, **kwargs)

    return do_checkpoint


def list_wrapper(method):
    @functools.wraps(method)
    def newmethod(*args, **kwargs):
        l = method(*args, **kwargs)
        return RevertableList(l)

    return newmethod


class RollbackRandom(random.Random):
    """
    This is used for Random objects returned by renpy.random.Random.
    """

    def __init__(self):
        log = renpy.game.log

        if log is not None:
            log.mutated[id(self)] = None

        super(RollbackRandom, self).__init__()

    def _clean(self):
        return self.getstate()

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        super(RollbackRandom, self).setstate(compressed)

    if not TYPE_CHECKING:
        setstate = checkpointing(mutator(random.Random.setstate))

    choices = list_wrapper(random.Random.choices)
    sample = list_wrapper(random.Random.sample)

    if not TYPE_CHECKING:
        getrandbits = checkpointing(mutator(random.Random.getrandbits))
        seed = checkpointing(mutator(random.Random.seed))
        random = checkpointing(mutator(random.Random.random))

    def Random(self, seed=None):
        """
        Returns a new RNG object separate from the main one.
        """

        if seed is None:
            seed = self.random()

        new = RollbackRandom()
        new.seed(seed)
        return new


class DetRandom(random.Random):
    """
    This is renpy.random.
    """

    def __init__(self):
        super(DetRandom, self).__init__()
        self.stack = []

    choices = list_wrapper(random.Random.choices)
    sample = list_wrapper(random.Random.sample)

    def random(self):
        if self.stack:
            rv = self.stack.pop()
        else:
            rv = super(DetRandom, self).random()

        log = renpy.game.log

        if log.current is not None:
            log.current.random.append(rv)

        renpy.game.context().force_checkpoint = True

        return rv

    def pushback(self, l):
        """
        Pushes the random numbers in l onto the stack so they will be generated
        in the order given.
        """

        ll = l[:]
        ll.reverse()

        self.stack.extend(ll)

    def reset(self):
        """
        Resets the RNG, removing all of the pushbacked numbers.
        """

        del self.stack[:]

    def Random(self, seed=None):
        """
        Returns a new RNG object separate from the main one.
        """

        if seed is None:
            seed = self.random()

        new = RollbackRandom()
        new.seed(seed)
        return new
