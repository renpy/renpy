# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Optional

import __future__

import marshal
import random
import weakref
import re
import sys
import time
import io
import types
import copyreg
import functools

import renpy

# A set of flags that indicate dict should run in future-compatible mode.
FUTURE_FLAGS = (__future__.CO_FUTURE_DIVISION | __future__.CO_FUTURE_WITH_STATEMENT) # type: ignore

##############################################################################
# Monkeypatch copy_reg to work around a change in the class that RevertableSet
# is based on.

def _reconstructor(cls, base, state):
    if (cls is RevertableSet) and (base is object):
        base = set
        state = [ ]

    if base is object:
        obj = object.__new__(cls)
    else:
        obj = base.__new__(cls, state) # type: ignore
        if base.__init__ != object.__init__:
            base.__init__(obj, state)

    return obj


copyreg._reconstructor = _reconstructor # type: ignore


# This is set to True whenever a mutation occurs. The save code uses
# this to check to see if a background-save is valid.
mutate_flag = True

# In Python 2 functools.wraps does not check for the existence of WRAPPER_ASSIGNMENTS elements,
# so for the C-defined methods we have AttributeError: 'method_descriptor' object has no attribute '__module__'.
# To work around this, we only keep attributes that surely exist.
if PY2:
    def _method_wrapper(method):
        return functools.wraps(method, ("__name__", "__doc__"), ())
else:
    _method_wrapper = functools.wraps # type: ignore

def mutator(method):

    @_method_wrapper(method)
    def do_mutation(self, *args, **kwargs):

        global mutate_flag

        mutated = renpy.game.log.mutated

        if id(self) not in mutated:
            mutated[id(self)] = (weakref.ref(self), self._clean())
            mutate_flag = True

        return method(self, *args, **kwargs)

    return do_mutation


class CompressedList(object):
    """
    Compresses the changes in a queue-like list. What this does is to try
    to find a central sub-list for which has objects in both lists. It
    stores the location of that in the new list, and then elements before
    and after in the sub-list.

    This only really works if the objects in the list are unique, but the
    results are efficient even if this doesn't work.
    """

    def __init__(self, old, new):

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
            self.post = [ ]

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

    def decompress(self, new):
        return self.pre + new[self.start:self.end] + self.post

    def __repr__(self):
        return "<CompressedList {} [{}:{}] {}>".format(
            self.pre,
            self.start,
            self.end,
            self.post)


class RevertableList(list):

    def __init__(self, *args):
        log = renpy.game.log

        if log is not None:
            log.mutated[id(self)] = None

        list.__init__(self, *args)

    __delitem__ = mutator(list.__delitem__)
    if PY2:
        __delslice__ = mutator(list.__delslice__) # type: ignore
    __setitem__ = mutator(list.__setitem__)
    if PY2:
        __setslice__ = mutator(list.__setslice__) # type: ignore
    __iadd__ = mutator(list.__iadd__)
    __imul__ = mutator(list.__imul__)
    append = mutator(list.append)
    extend = mutator(list.extend)
    insert = mutator(list.insert)
    pop = mutator(list.pop)
    remove = mutator(list.remove)
    reverse = mutator(list.reverse)
    sort = mutator(list.sort)

    def wrapper(method): # type: ignore

        @_method_wrapper(method)
        def newmethod(*args, **kwargs):
            l = method(*args, **kwargs) # type: ignore
            if l is NotImplemented:
                return l
            return RevertableList(l)

        return newmethod

    __add__ = wrapper(list.__add__) # type: ignore
    if PY2:
        __getslice__ = wrapper(list.__getslice__) # type: ignore
    __mul__ = wrapper(list.__mul__) # type: ignore
    __rmul__ = wrapper(list.__rmul__) # type: ignore

    del wrapper

    def __getitem__(self, index):
        rv = list.__getitem__(self, index)

        if isinstance(index, slice):
            return RevertableList(rv)
        else:
            return rv

    def copy(self):
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


def revertable_range(*args):
    return RevertableList(range(*args))


def revertable_sorted(*args, **kwargs):
    return RevertableList(sorted(*args, **kwargs))


class RevertableDict(dict):

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

    if PY2:

        def keys(self):
            rv = dict.keys(self)

            if (sys._getframe(1).f_code.co_flags & FUTURE_FLAGS) != FUTURE_FLAGS:
                rv = RevertableList(rv)

            return rv

        def values(self):
            rv = dict.values(self)

            if (sys._getframe(1).f_code.co_flags & FUTURE_FLAGS) != FUTURE_FLAGS:
                rv = RevertableList(rv)

            return rv

        def items(self):
            rv = dict.items(self)

            if (sys._getframe(1).f_code.co_flags & FUTURE_FLAGS) != FUTURE_FLAGS:
                rv = RevertableList(rv)

            return rv

    else:
        itervalues = dict.values
        iterkeys = dict.keys
        iteritems = dict.items

        def has_key(self, key):
            return (key in self)

        # https://peps.python.org/pep-0584 methods
        def __or__(self, other):
            if not isinstance(other, dict):
                return NotImplemented
            rv = RevertableDict(self)
            rv.update(other)
            return rv

        def __ror__(self, other):
            if not isinstance(other, dict):
                return NotImplemented
            rv = RevertableDict(other)
            rv.update(self)
            return rv

        def __ior__(self, other):
            self.update(other)
            return self

    def copy(self):
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


class RevertableDefaultDict(RevertableDict):
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

    def __init__(self, default_factory=None, *args, **kwargs):
        self.default_factory = default_factory
        super(RevertableDefaultDict, self).__init__(*args, **kwargs)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)

        rv = self.default_factory()
        self[key] = rv
        return rv



class RevertableSet(set):

    def __setstate__(self, state):
        if isinstance(state, tuple):
            self.update(state[0].keys())
        else:
            self.update(state)

    def __getstate__(self):
        rv = ({ i : True for i in self},)
        return rv

    # Required to ensure that getstate and setstate are called.
    __reduce__ = object.__reduce__
    __reduce_ex__ = object.__reduce_ex__

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

    def wrapper(method): # type: ignore

        @_method_wrapper(method)
        def newmethod(*args, **kwargs):
            rv = method(*args, **kwargs) # type: ignore
            if isinstance(rv, set):
                return RevertableSet(rv)
            else:
                return rv

        return newmethod

    __and__ = wrapper(set.__and__) # type: ignore
    __sub__ = wrapper(set.__sub__) # type: ignore
    __xor__ = wrapper(set.__xor__) # type: ignore
    __or__ = wrapper(set.__or__) # type: ignore
    copy = wrapper(set.copy) # type: ignore
    difference = wrapper(set.difference) # type: ignore
    intersection = wrapper(set.intersection) # type: ignore
    symmetric_difference = wrapper(set.symmetric_difference) # type: ignore
    union = wrapper(set.union) # type: ignore

    del wrapper

    def _clean(self):
        return list(self)

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        set.clear(self)
        set.update(self, compressed)


class RevertableObject(object):
    # All RenPy's objects have  __dict__, so _rollback is fast, i.e
    # one update, not iterating over all attributes.
    # __weakref__ should exist, so mutator can work.
    # Other slots are forbidden because they cannot be reverted in easy way.
    # For more details, see https://github.com/renpy/renpy/pull/3282
    # __slots__ = ("__weakref__", "__dict__")

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
            raise TypeError("Classes with __slots__ do not support rollback. "
                            "To create a class with slots, inherit from python_object instead.")

    __setattr__ = mutator(object.__setattr__)
    __delattr__ = mutator(object.__delattr__)

    def _clean(self):
        return self.__dict__.copy()

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        self.__dict__.clear()
        self.__dict__.update(compressed)


class MultiRevertable(object):
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
        rv = [ ]

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

    @_method_wrapper(method)
    def do_checkpoint(self, *args, **kwargs):

        renpy.game.context().force_checkpoint = True

        return method(self, *args, **kwargs)

    return do_checkpoint


def list_wrapper(method):

    @_method_wrapper(method)
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

    setstate = checkpointing(mutator(random.Random.setstate))

    if PY2:
        jumpahead = checkpointing(mutator(random.Random.jumpahead)) # type: ignore
    else:
        choices = list_wrapper(random.Random.choices)
    sample = list_wrapper(random.Random.sample)

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
        self.stack = [ ]

    if not PY2:
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
