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

from typing import (
    Any,
    Callable,
    ClassVar,
    Protocol,
    Iterable,
    Sequence,
    AbstractSet,
    SupportsIndex,
    TypeGuard,
    TYPE_CHECKING,
    final,
    overload,
)

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


##############################################################################
class RevertableType(Protocol):
    """
    Protocol that defines the methods that a revertable type must implement.

    Apart from the methods defined here, the class must also be weak-referencable.
    """

    type Clean = Any
    type Compressed = Any

    def _clean(self) -> Clean:
        """
        Gets a representation of this object before any mutation in current
        rollback session.

        This is not necessarily a pickleable object.

        Commonly, this is a shallow copy of the object.
        """

        raise NotImplementedError

    def _compress(self, clean: Clean) -> Compressed:
        """
        Takes a result of `_clean` and returns a possibly compressed version of
        the data that would be stored in rollback data, and should be pickleable.
        """

        raise NotImplementedError

    def _rollback(self, compressed: Compressed) -> None:
        """
        Rolls this object back, using the information created by `_compress`.

        Since compressed can come from a save file, this method also has to
        recognize and deal with old data.
        """

        raise NotImplementedError


def is_revertable(obj: object | type) -> TypeGuard[RevertableType]:
    """
    Returns True if `obj` implements the RevertableType protocol.
    """

    # At runtime we make a weak check to reduce the overhead of runtime_checkable
    # protocol.
    if not isinstance(obj, type):
        obj = type(obj)

    return callable(getattr(obj, "_rollback", None))


mutate_flag: bool = True
"""
This is set to True whenever a mutation occurs. The background save code uses
this to check to see if store has changed after save started.
"""


def _object_born(obj: RevertableType):
    log = renpy.game.log

    if log is not None:
        # Init to None so we don't call _clean for an object that could be
        # destroyed before rollback session ends. If user rolls back here,
        # it would be deleted from anywhere it was referenced.
        log.mutated[id(obj)] = None


def _creator(base: type):
    """
    Helper function to wrap base class constructor and prevent mutations
    registeration before new rollback session starts.
    """

    method = base.__init__

    @functools.wraps(method)
    def do_init(self, *args, **kwargs):
        _object_born(self)
        method(self, *args, **kwargs)

    return do_init


def _object_mutated(obj: RevertableType):
    global mutate_flag

    mutated = renpy.game.log.mutated

    if id(obj) not in mutated:
        mutated[id(obj)] = (weakref.ref(obj), obj._clean())
        mutate_flag = True


def _mutator(method: Callable):
    """
    Helper function to wrap methods that mutate object to get clean state before
    any mutation occurs in current rollback session.
    """

    @functools.wraps(method)
    def do_mutation(self, *args, **kwargs):
        _object_mutated(self)
        return method(self, *args, **kwargs)

    return do_mutation


@final
class CompressedList[T]:
    """
    Compresses the changes in a queue-like list. What this does is to try
    to find a central sub-list for which has objects in both lists. It
    stores the location of that in the new list, and then elements before
    and after in the sub-list.

    This only really works if the objects in the list are unique, but the
    results are efficient even if this doesn't work.
    """

    pre: list[T]
    start: int
    end: int
    post: list[T]

    def __new__(cls, old: list[T], new: list[T]) -> "list[T] | CompressedList[T]":
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
            return old

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
        self = object.__new__(cls)
        self.pre = list.__getitem__(old, slice(0, old_start))
        self.start = new_start
        self.end = new_end
        self.post = list.__getitem__(old, slice(old_end, len_old))
        return self

    def decompress(self, new: list[T]) -> list[T]:
        return self.pre + new[self.start : self.end] + self.post

    def __repr__(self):
        return f"<CompressedList {self.pre} [{self.start}:{self.end}] {self.post}>"


class RevertableList[T](list[T]):
    # Mutations does not change the signature of those methods, so let IDE
    # show the original.
    if not TYPE_CHECKING:
        __init__ = _creator(list)

        __delitem__ = _mutator(list.__delitem__)
        __setitem__ = _mutator(list.__setitem__)
        __iadd__ = _mutator(list.__iadd__)
        __imul__ = _mutator(list.__imul__)
        append = _mutator(list.append)
        extend = _mutator(list.extend)
        insert = _mutator(list.insert)
        pop = _mutator(list.pop)
        remove = _mutator(list.remove)
        reverse = _mutator(list.reverse)
        sort = _mutator(list.sort)
        clear = _mutator(list.clear)

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

    def __getitem__(self, index: SupportsIndex | slice) -> "RevertableList[T] | T":
        if isinstance(index, slice):
            return RevertableList(super().__getitem__(index))
        else:
            return super().__getitem__(index)

    def copy(self) -> "RevertableList[T]":
        return RevertableList(self)

    if TYPE_CHECKING:
        type Clean = list[T]
        type Compressed = list[T] | CompressedList[T]

    def _clean(self) -> "Clean":
        return super().copy()

    def _compress(self, clean: "Clean") -> "Compressed":
        if not self or not clean:
            return clean

        list_compression_length = renpy.config.list_compression_length
        if list_compression_length is None:
            return clean

        if len(self) < list_compression_length or len(clean) < list_compression_length:
            return clean

        return CompressedList(clean, self)

    def _rollback(self, compressed: "Compressed"):
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
        __init__ = _creator(dict)

        __delitem__ = _mutator(dict.__delitem__)
        __setitem__ = _mutator(dict.__setitem__)
        clear = _mutator(dict.clear)
        pop = _mutator(dict.pop)
        popitem = _mutator(dict.popitem)
        setdefault = _mutator(dict.setdefault)
        update = _mutator(dict.update)

        # Keep some Python 2 methods for compatibility with old games.
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
        return RevertableDict(self)

    if TYPE_CHECKING:
        type Clean = list[tuple[KT, VT]]
        type Compressed = Clean

    def _clean(self) -> "Clean":
        return list(self.items())

    def _compress(self, clean: "Clean") -> "Compressed":
        return clean

    def _rollback(self, compressed: "Compressed"):
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
    # Also, see https://github.com/python/typeshed/pull/11780 for why there is
    # pyright ignore.
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

    def __init__(self, default_factory=None, iterable=(), /, **kwargs):
        self.default_factory = default_factory
        super().__init__(iterable, **kwargs)

    def __missing__(self, key: KT) -> VT:
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
        __init__ = _creator(set)

        __iand__ = _mutator(set.__iand__)
        __ior__ = _mutator(set.__ior__)
        __isub__ = _mutator(set.__isub__)
        __ixor__ = _mutator(set.__ixor__)
        add = _mutator(set.add)
        clear = _mutator(set.clear)
        difference_update = _mutator(set.difference_update)
        discard = _mutator(set.discard)
        intersection_update = _mutator(set.intersection_update)
        pop = _mutator(set.pop)
        remove = _mutator(set.remove)
        symmetric_difference_update = _mutator(set.symmetric_difference_update)
        update = _mutator(set.update)

        union_update = _mutator(set.update)

    # Can not be in non-typing block above because we change return type.
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

    if TYPE_CHECKING:
        type Clean = list[T]
        type Compressed = Clean

    def _clean(self) -> "Clean":
        return list(self)

    def _compress(self, clean: "Clean") -> "Compressed":
        return clean

    def _rollback(self, compressed: "Compressed"):
        super().clear()
        super().update(compressed)


class RevertableObject:
    # All RenPy's objects have __dict__, so _rollback is fast, i.e
    # one update, not iterating over all attributes.
    # __weakref__ should exist, so mutator can work.
    # Other slots are forbidden because it will complicate rollback too much.
    # For more details, see https://github.com/renpy/renpy/pull/3282

    def __new__(cls, *args, **kwargs):
        self = super(RevertableObject, cls).__new__(cls)

        _object_born(self)

        return self

    def __init__(self, *args, **kwargs):
        if renpy.config.developer and (args or kwargs):
            raise TypeError("object() takes no arguments")

    def __init_subclass__(cls):
        if renpy.config.developer and cls.__dict__.get("__slots__", ()):
            err = TypeError("nonempty __slots__ not supported for subtype of 'renpy.revertable.RevertableObject'")
            err.add_note("To create a class with slots, inherit from python_object instead.")
            raise err

        super().__init_subclass__()

    if not TYPE_CHECKING:
        __setattr__ = _mutator(object.__setattr__)
        __delattr__ = _mutator(object.__delattr__)
    else:
        type Clean = dict[str, Any]
        type Compressed = Clean

    def _clean(self) -> "Clean":
        return self.__dict__.copy()

    def _compress(self, clean: "Clean") -> "Compressed":
        return clean

    def _rollback(self, compressed: "Compressed"):
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

    _rollback_types: ClassVar[tuple[type[RevertableType]]]

    def __init_subclass__(cls):
        rv = []

        for i in cls.__mro__:
            if i is MultiRevertable:
                continue

            if is_revertable(i):
                rv.append(i)

        cls._rollback_types = tuple(rv)

        super().__init_subclass__()

    if TYPE_CHECKING:
        type Clean = tuple[Any, ...]
        type Compressed = Clean

    def _clean(self) -> "Clean":
        return tuple(i._clean(self) for i in self._rollback_types)

    def _compress(self, clean: "Clean") -> "Compressed":
        return tuple(i._compress(self, c) for i, c in zip(self._rollback_types, clean))

    def _rollback(self, compressed: "Compressed"):
        for i, c in zip(self._rollback_types, compressed):
            i._rollback(self, c)


def _checkpointing(method):
    """
    Helper function to wrap methods that not only mutate object, but also
    set a force checkpoint in current interaction.
    """

    @functools.wraps(method)
    def do_checkpoint(self, *args, **kwargs):
        renpy.game.context().force_checkpoint = True

        _object_mutated(self)

        return method(self, *args, **kwargs)

    return do_checkpoint


class RollbackRandom(random.Random):
    """
    This is used for Random objects returned by renpy.random.Random.
    """

    if not TYPE_CHECKING:
        __init__ = _creator(random.Random)

        setstate = _checkpointing(random.Random.setstate)

        getrandbits = _checkpointing(random.Random.getrandbits)
        seed = _checkpointing(random.Random.seed)
        random = _checkpointing(random.Random.random)

    def choices[T](
        self,
        population: Sequence[T],
        weights: Sequence[float] | None = None,
        *,
        cum_weights: Sequence[float] | None = None,
        k: int = 1,
    ) -> RevertableList[T]:
        return RevertableList(super().choices(population, weights, cum_weights=cum_weights, k=k))

    def sample[T](
        self,
        population: Sequence[T],
        k: int,
        *,
        counts: Iterable[int] | None = None,
    ) -> RevertableList[T]:
        return RevertableList(super().sample(population, k, counts=counts))

    def Random(self, seed: float | None = None) -> "RollbackRandom":
        """
        Returns a new RNG object separate from the main one.
        """

        if seed is None:
            seed = self.random()

        new = RollbackRandom()
        new.seed(seed)
        return new

    if TYPE_CHECKING:
        type Clean = tuple[Any, ...]
        type Compressed = Clean

    def _clean(self) -> "Clean":
        return self.getstate()

    def _compress(self, clean: "Clean") -> "Compressed":
        return clean

    def _rollback(self, compressed: "Compressed"):
        super(RollbackRandom, self).setstate(compressed)


class DetRandom(random.Random):
    """
    This is a class that lives in `renpy.rollback.rng` and referenced by user
    with `renpy.random`.

    This is essentially a wrapper of `random.Random` where after rollback it
    will produce the same random numbers.
    """

    def __init__(self):
        super().__init__()

        self.stack: list[float] = []

    def choices[T](
        self,
        population: Sequence[T],
        weights: Sequence[float] | None = None,
        *,
        cum_weights: Sequence[float] | None = None,
        k: int = 1,
    ) -> RevertableList[T]:
        return RevertableList(super().choices(population, weights, cum_weights=cum_weights, k=k))

    def sample[T](
        self,
        population: Sequence[T],
        k: int,
        *,
        counts: Iterable[int] | None = None,
    ) -> RevertableList[T]:
        return RevertableList(super().sample(population, k, counts=counts))

    def random(self) -> float:
        if self.stack:
            rv = self.stack.pop()
        else:
            rv = super().random()

        log = renpy.game.log

        if log.current is not None:
            log.current.random.append(rv)

        renpy.game.context().force_checkpoint = True

        return rv

    def pushback(self, numbers: list[float], /):
        """
        Pushes the random numbers onto the stack so they will be generated
        in the order given.
        """

        self.stack.extend(reversed(numbers))

    def reset(self):
        """
        Resets the RNG, removing all of the pushbacked numbers.
        """

        self.stack.clear()

    def Random(self, seed: float | None = None):
        """
        Returns a new RNG object separate from the main one.
        """

        return RollbackRandom()
