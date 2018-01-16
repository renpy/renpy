# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

# Import the python ast module, not ours.
ast = __import__("ast", { })

# Import the future module itself.
import __future__

import marshal
import random
import weakref
import re
import sys
import time

import renpy.audio

##############################################################################
# Code that implements the store.

# Deleted is a singleton object that's used to represent an object that has
# been deleted from the store.


class StoreDeleted(object):

    def __reduce__(self):
        return "deleted"


deleted = StoreDeleted()


class StoreModule(object):
    """
    This class represents one of the modules containing the store of data.
    """

    # Set our dict to be the StoreDict. Then proxy over setattr and delattr,
    # since Python won't call them by default.

    def __reduce__(self):
        return (get_store_module, (self.__name__,))

    def __init__(self, d):
        object.__setattr__(self, "__dict__", d)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __delattr__(self, key):
        del self.__dict__[key]

# Used to unpickle a store module.


def get_store_module(name):
    return sys.modules[name]


from renpy.pydict import DictItems, find_changes

EMPTY_DICT = { }


class StoreDict(dict):
    """
    This class represents the dictionary of a store module. It logs
    sets and deletes.
    """

    def __reduce__(self):
        raise Exception("Cannot pickle a reference to a store dictionary.")

    def __init__(self):

        # The value of this dictionary at the start of the current
        # rollback period (when begin() was last called).
        self.old = DictItems(self)

        # The set of variables in this StoreDict that changed since the
        # end of the init phase.
        self.ever_been_changed = set()

    def reset(self):
        """
        Called to reset this to its initial conditions.
        """

        self.ever_been_changed = set()
        self.clear()
        self.old = DictItems(self)

    def begin(self):
        """
        Called to mark the start of a rollback period.
        """

        self.old = DictItems(self)

    def get_changes(self):
        """
        For every key that has changed since begin() was called, returns a
        dictionary mapping the key to its value when begin was called, or
        deleted if it did not exist when begin was called.

        As a side-effect, updates self.ever_been_changed.
        """

        new = DictItems(self)
        rv = find_changes(self.old, new, deleted)
        self.old = new

        if rv is None:
            return EMPTY_DICT

        for k in rv:
            self.ever_been_changed.add(k)

        return rv


# A map from the name of a store dict to the corresponding StoreDict object.
# This isn't reset during a reload, so store objects stay the same in modules.
store_dicts = { }

# Same, for module objects.
store_modules = { }

# The store dicts that have been cleared and initialized during the current
# run.
initialized_store_dicts = set()


def create_store(name):
    """
    Creates the store with `name`.
    """

    parent, _, var = name.rpartition('.')

    if parent:
        create_store(parent)

    name = str(name)

    if name in initialized_store_dicts:
        return

    initialized_store_dicts.add(name)

    # Create the dict.
    d = store_dicts.setdefault(name, StoreDict())
    d.reset()

    # Set the name.
    d["__name__"] = name
    d["__package__"] = name

    # Set up the default contents of the store.
    eval("1", d)

    for k, v in renpy.minstore.__dict__.iteritems():
        if k not in d:
            d[k] = v

    # Create or reuse the corresponding module.
    if name in store_modules:
        sys.modules[name] = store_modules[name]
    else:
        store_modules[name] = sys.modules[name] = StoreModule(d)

    if parent:
        store_dicts[parent][var] = sys.modules[name]


class StoreBackup():
    """
    This creates a copy of the current store, as it was at the start of
    the current statement.
    """

    def __init__(self):

        # The contents of the store for each store.
        self.store = { }

        # The contents of old for each store.
        self.old = { }

        # The contents of ever_been_changed for each store.
        self.ever_been_changed = { }

        for k in store_dicts:
            self.backup_one(k)

    def backup_one(self, name):

        d = store_dicts[name]

        self.store[name] = dict(d)
        self.old[name] = d.old.as_dict()
        self.ever_been_changed[name] = set(d.ever_been_changed)

    def restore_one(self, name):
        sd = store_dicts[name]

        sd.clear()
        sd.update(self.store[name])

        sd.old = DictItems(self.old[name])

        sd.ever_been_changed.clear()
        sd.ever_been_changed.update(self.ever_been_changed[name])

    def restore(self):

        for k in store_dicts:
            self.restore_one(k)


clean_store_backup = None


def make_clean_stores():
    """
    Copy the clean stores.
    """

    global clean_store_backup

    for _k, v in store_dicts.iteritems():

        v.ever_been_changed.clear()
        v.begin()

    clean_store_backup = StoreBackup()


def clean_stores():
    """
    Revert the store to the clean copy.
    """

    clean_store_backup.restore()


def clean_store(name):
    """
    Reverts the named store to its clean copy.
    """

    if not name.startswith("store."):
        name = "store." + name

    clean_store_backup.restore_one(name)


def reset_store_changes(name):

    if not name.startswith("store."):
        name = "store." + name

    sd = store_dicts[name]
    sd.begin()

# Code that computes reachable objects, which is used to filter
# the rollback list before rollback or serialization.


class NoRollback(object):
    """
    :doc: norollback class

    Instances of classes inheriting from this class do not participate in
    rollback. Objects reachable through an instance of a NoRollback class
    only participate in rollback if they are reachable through other paths.
    """

    pass


# parents = [ ]

def reached(obj, reachable, wait):
    """
    @param obj: The object that was reached.
    @param path: The path from the store via which it was reached.

    `reachable`
        A map from id(obj) to int. The int is 1 if the object was reached
        normally, and 0 if it was reached, but inherits from NoRollback.

    """

    if wait:
        wait()

    idobj = id(obj)

    if idobj in reachable:
        return

    if isinstance(obj, (NoRollback, real_file)):  # @UndefinedVariable
        reachable[idobj] = 0
        return

    reachable[idobj] = 1

    # Since the store module is the roots, there's no need to
    # look into it.
    if isinstance(obj, StoreModule):
        return

    # parents.append(obj)

    try:
        # Treat as fields, indexed by strings.
        for v in vars(obj).itervalues():
            reached(v, reachable, wait)
    except:
        pass

    try:
        # Treat as iterable
        if not isinstance(obj, basestring):
            for v in obj.__iter__():
                reached(v, reachable, wait)
    except:
        pass

    try:
        # Treat as dict.
        for v in obj.itervalues():
            reached(v, reachable, wait)
    except:
        pass

    # parents.pop()


def reached_vars(store, reachable, wait):
    """
    Marks everything reachable from the variables in the store
    or from the context info objects as reachable.

    @param store: A map from variable name to variable value.
    @param reachable: A dictionary mapping reached object ids to
    the path by which the object was reached.
    """

    for v in store.itervalues():
        reached(v, reachable, wait)

    for c in renpy.game.contexts:
        reached(c.info, reachable, wait)
        reached(c.music, reachable, wait)
        for d in c.dynamic_stack:
            for v in d.itervalues():
                reached(v, reachable, wait)


# Code that replaces literals will calls to magic constructors.

class WrapNode(ast.NodeTransformer):

    def visit_ClassDef(self, n):
        n = self.generic_visit(n)

        if not n.bases:
            n.bases.append(ast.Name(id="object", ctx=ast.Load()))

        return n

    def visit_SetComp(self, n):
        return ast.Call(
            func=ast.Name(
                id="__renpy__set__",
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_Set(self, n):

        return ast.Call(
            func=ast.Name(
                id="__renpy__set__",
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_ListComp(self, n):
        return ast.Call(
            func=ast.Name(
                id="__renpy__list__",
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_List(self, n):
        if not isinstance(n.ctx, ast.Load):
            return self.generic_visit(n)

        return ast.Call(
            func=ast.Name(
                id="__renpy__list__",
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_DictComp(self, n):
        return ast.Call(
            func=ast.Name(
                id="__renpy__dict__",
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_Dict(self, n):

        return ast.Call(
            func=ast.Name(
                id="__renpy__dict__",
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)


wrap_node = WrapNode()


def set_filename(filename, offset, tree):
    """Set the filename attribute to filename on every node in tree"""
    worklist = [tree]
    while worklist:
        node = worklist.pop(0)
        node.filename = filename

        lineno = getattr(node, 'lineno', None)
        if lineno is not None:
            node.lineno = lineno + offset

        worklist.extend(node.getChildNodes())


unicode_re = re.compile(ur'[\u0080-\uffff]')


def unicode_sub(m):
    """
    If the string s contains a unicode character, make it into a
    unicode string.
    """

    s = m.group(0)

    if not unicode_re.search(s):
        return s

    prefix = m.group(1)
    sep = m.group(2)
    body = m.group(3)

    if "u" not in prefix and "U" not in prefix:
        prefix = 'u' + prefix

    rv = prefix + sep + body + sep

    return rv


string_re = re.compile(r'([uU]?[rR]?)("""|"|\'\'\'|\')((\\.|.)*?)\2')


def escape_unicode(s):
    if unicode_re.search(s):
        s = string_re.sub(unicode_sub, s)

    return s


# Flags used by py_compile.
old_compile_flags = ( __future__.nested_scopes.compiler_flag
                      | __future__.with_statement.compiler_flag
                      )

new_compile_flags = (  old_compile_flags
                       | __future__.absolute_import.compiler_flag
                       | __future__.print_function.compiler_flag
                       | __future__.unicode_literals.compiler_flag
                       )


# A cache for the results of py_compile.
py_compile_cache = { }

# An old version of the same, that's preserved across reloads.
old_py_compile_cache = { }


def py_compile(source, mode, filename='<none>', lineno=1, ast_node=False, cache=True):
    """
    Compiles the given source code using the supplied codegenerator.
    Lists, List Comprehensions, and Dictionaries are wrapped when
    appropriate.

    `source`
        The source code, as a either a string, pyexpr, or ast module
        node.

    `mode`
        One of "exec" or "eval".

    `filename`
        The filename the source comes from. If a pyexpr is given, the
        filename embedded in the pyexpr is used.

    `lineno`
        The line number of the first line of source code. If a pyexpr is
        given, the filename embedded in the pyexpr is used.

    `ast_node`
        Rather than returning compiled bytecode, returns the AST object
        that would be used.
    """

    if ast_node:
        cache = False

    if isinstance(source, ast.Module):
        return compile(source, filename, mode)

    if isinstance(source, renpy.ast.PyExpr):
        filename = source.filename
        lineno = source.linenumber

    if cache:
        key = (lineno, filename, unicode(source), mode, renpy.script.MAGIC)

        rv = py_compile_cache.get(key, None)
        if rv is not None:
            return rv

        rv = old_py_compile_cache.get(key, None)
        if rv is not None:
            old_py_compile_cache[key] = rv
            return rv

        bytecode = renpy.game.script.bytecode_oldcache.get(key, None)
        if bytecode is not None:

            renpy.game.script.bytecode_newcache[key] = bytecode
            rv = marshal.loads(bytecode)
            py_compile_cache[key] = rv
            return rv

    source = unicode(source)
    source = source.replace("\r", "")
    source = escape_unicode(source)

    try:
        line_offset = lineno - 1

        try:
            flags = new_compile_flags
            tree = compile(source, filename, mode, ast.PyCF_ONLY_AST | flags, 1)
        except:
            flags = old_compile_flags
            tree = compile(source, filename, mode, ast.PyCF_ONLY_AST | flags, 1)

        tree = wrap_node.visit(tree)

        ast.fix_missing_locations(tree)
        ast.increment_lineno(tree, lineno - 1)

        line_offset = 0

        if ast_node:
            return tree.body

        rv = compile(tree, filename, mode, flags, 1)

        if cache:
            py_compile_cache[key] = rv
            renpy.game.script.bytecode_newcache[key] = marshal.dumps(rv)
            renpy.game.script.bytecode_dirty = True

        return rv

    except SyntaxError, e:

        if e.lineno is not None:
            e.lineno += line_offset

        raise e


def py_compile_exec_bytecode(source, **kwargs):
    code = py_compile(source, 'exec', cache=False, **kwargs)
    return marshal.dumps(code)


def py_compile_eval_bytecode(source, **kwargs):
    source = source.strip()
    code = py_compile(source, 'eval', cache=False, **kwargs)
    return marshal.dumps(code)


# Classes that are exported in place of the normal list, dict, and
# object.

# This is set to True whenever a mutation occurs. The save code uses
# this to check to see if a background-save is valid.
mutate_flag = True


def mutator(method):

    def do_mutation(self, *args, **kwargs):

        global mutate_flag

        mutated = renpy.game.log.mutated  # @UndefinedVariable

        if id(self) not in mutated:
            mutated[id(self)] = ( weakref.ref(self), self._clean())
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
        self.pre = list.__getslice__(old, 0, old_start)
        self.start = new_start
        self.end = new_end
        self.post = list.__getslice__(old, old_end, len_old)

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
    __delslice__ = mutator(list.__delslice__)
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

    def wrapper(method):  # E0213 @NoSelf
        def newmethod(*args, **kwargs):
            l = method(*args, **kwargs)
            return RevertableList(l)

        return newmethod

    __add__ = wrapper(list.__add__)
    __getslice__ = wrapper(list.__getslice__)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError("can't multiply sequence by non-int of type '{}'.".format(type(other).__name__))

        return RevertableList(list.__mul__(self, other))

    __rmul__ = __mul__

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

    def list_wrapper(method):  # E0213 @NoSelf
        def newmethod(*args, **kwargs):
            return RevertableList(method(*args, **kwargs))  # E1102

        return newmethod

    keys = list_wrapper(dict.keys)
    values = list_wrapper(dict.values)
    items = list_wrapper(dict.items)

    del list_wrapper

    def copy(self):
        rv = RevertableDict()
        rv.update(self)
        return rv

    def _clean(self):
        return self.items()

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        self.clear()

        for k, v in compressed:
            self[k] = v


class RevertableSet(set):

    def __setstate__(self, state):
        if isinstance(state, tuple):
            self.update(state[0].keys())
        else:
            self.update(state)

    def __getstate__(self):
        rv = ({ i : True for i in self}, )
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

    def wrapper(method):  # @NoSelf
        def newmethod(*args, **kwargs):
            rv = method(*args, **kwargs)
            if isinstance(rv, (set, frozenset)):
                return RevertableSet(rv)
            else:
                return rv

        return newmethod

    __and__ = wrapper(set.__and__)
    __sub__ = wrapper(set.__sub__)
    __xor__ = wrapper(set.__xor__)
    __or__ = wrapper(set.__or__)
    copy = wrapper(set.copy)
    difference = wrapper(set.difference)
    intersection = wrapper(set.intersection)
    symmetric_difference = wrapper(set.symmetric_difference)
    union = wrapper(set.union)

    del wrapper

    def _clean(self):
        return list(self)

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        set.clear(self)
        set.update(self, compressed)


class RevertableObject(object):

    def __new__(cls, *args, **kwargs):
        self = super(RevertableObject, cls).__new__(cls)

        log = renpy.game.log
        if log is not None:
            log.mutated[id(self)] = None

        return self

    def __init__(self, *args, **kwargs):
        if (args or kwargs) and renpy.config.developer:
            raise TypeError("object() takes no parameters.")

    def __setattr__(self, attr, value):
        object.__setattr__(self, attr, value)

    def __delattr__(self, attr):
        object.__delattr__(self, attr)

    __setattr__ = mutator(__setattr__)
    __delattr__ = mutator(__delattr__)

    def _clean(self):
        return self.__dict__.copy()

    def _compress(self, clean):
        return clean

    def _rollback(self, compressed):
        self.__dict__.clear()
        self.__dict__.update(compressed)


# An object that handles deterministic randomness, or something.

class DetRandom(random.Random):

    def __init__(self):
        super(DetRandom, self).__init__()
        self.stack = [ ]

    def random(self):

        if self.stack:
            rv = self.stack.pop()
        else:
            rv = super(DetRandom, self).random()

        log = renpy.game.log

        if log.current is not None:
            log.current.random.append(rv)

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

        self.stack = [ ]

    def Random(self, seed=None):
        """
        Returns a new RNG object separate from the main one.
        """

        new = DetRandom()
        new.seed(seed)
        return new


rng = DetRandom()

# This is the code that actually handles the logging and managing
# of the rollbacks.

generation = time.time()
serial = 0


class Rollback(renpy.object.Object):
    """
    Allows the state of the game to be rolled back to the point just
    before a node began executing.

    @ivar context: A shallow copy of the context we were in before
    we started executing the node. (Shallow copy also includes
    a copy of the associated SceneList.)

    @ivar objects: A list of tuples, each containing an object and a
    token of information that, when passed to the rollback method on
    that object, causes that object to rollback.

    @ivar store: A list of updates to store that will cause the state
    of the store to be rolled back to the start of node
    execution. This is a list of tuples, either (key, value) tuples
    representing a value that needs to be assigned to a key, or (key,)
    tuples that mean the key should be deleted.

    @ivar checkpoint: True if this is a user-visible checkpoint,
    false otherwise.

    @ivar purged: True if purge_unreachable has already been called on
    this Rollback, False otherwise.

    @ivar random: A list of random numbers that were generated during the
    execution of this element.
    """

    __version__ = 4

    identifier = None

    def __init__(self):

        super(Rollback, self).__init__()

        self.context = renpy.game.context().rollback_copy()

        self.objects = [ ]
        self.purged = False
        self.random = [ ]
        self.forward = None

        # A map of maps name -> (variable -> value)
        self.stores = { }

        # If true, we retain the data in this rollback when a load occurs.
        self.retain_after_load = False

        # True if this is a checkpoint we can roll back to.
        self.checkpoint = False

        # True if this is a hard checkpoint, where the rollback counter
        # decreases.
        self.hard_checkpoint = False

        # A unique identifier for this rollback object.

        global serial
        self.identifier = (generation, serial)
        serial += 1

    def after_upgrade(self, version):

        if version < 2:
            self.stores = { "store" : { } }

            for i in self.store:
                if len(i) == 2:
                    k, v = i
                    self.stores["store"][k] = v
                else:
                    k, = i
                    self.stores["store"][k] = deleted

        if version < 3:
            self.retain_after_load = False

        if version < 4:
            self.hard_checkpoint = self.checkpoint

    def purge_unreachable(self, reachable, wait):
        """
        Adds objects that are reachable from the store of this
        rollback to the set of reachable objects, and purges
        information that is stored about totally unreachable objects.

        Returns True if this is the first time this method has been
        called, or False if it has already been called once before.
        """

        if self.purged:
            return False

        self.purged = True

        # Add objects reachable from the stores. (Objects that might be
        # unreachable at the moment.)
        for changes in self.stores.itervalues():
            for _k, v in changes.iteritems():
                if v is not deleted:
                    reached(v, reachable, wait)

        # Add in objects reachable through the context.
        reached(self.context.info, reachable, wait)
        for d in self.context.dynamic_stack:
            for v in d.itervalues():
                reached(v, reachable, wait)

        # Add in objects reachable through displayables.
        reached(self.context.scene_lists.get_all_displayables(), reachable, wait)

        # Purge object update information for unreachable objects.
        new_objects = [ ]

        for o, rb in self.objects:
            if reachable.get(id(o), 0):
                new_objects.append((o, rb))
                reached(rb, reachable, wait)
            else:
                if renpy.config.debug:
                    print("Removing unreachable:", o, file=renpy.log.real_stdout)
                    pass

        self.objects = new_objects

        return True

    def rollback(self):
        """
        Reverts the state of the game to what it was at the start of the
        previous checkpoint.
        """

        for obj, roll in reversed(self.objects):
            if roll is not None:
                obj._rollback(roll)

        for name, changes in self.stores.iteritems():
            store = store_dicts.get(name, None)
            if store is None:
                return

            for name, value in changes.iteritems():
                if value is deleted:
                    if name in store:
                        del store[name]
                else:
                    store[name] = value

        rng.pushback(self.random)

        renpy.game.contexts.pop()
        renpy.game.contexts.append(self.context)

    def rollback_control(self):
        """
        This rolls back only the control information, while leaving
        the data information intact.
        """

        renpy.game.contexts.pop()
        renpy.game.contexts.append(self.context)


class RollbackLog(renpy.object.Object):
    """
    This class manages the list of Rollback objects.

    @ivar log: The log of rollback objects.

    @ivar current: The current rollback object. (Equivalent to
    log[-1])

    @ivar rollback_limit: The number of steps left that we can
    interactively rollback.

    Not serialized:

    @ivar mutated: A dictionary that maps object ids to a tuple of
    (weakref to object, information needed to rollback that object)
    """

    __version__ = 5

    nosave = [ 'old_store', 'mutated', 'identifier_cache' ]
    identifier_cache = None

    def __init__(self):

        super(RollbackLog, self).__init__()

        self.log = [ ]
        self.current = None
        self.mutated = { }
        self.rollback_limit = 0
        self.rollback_is_fixed = False
        self.checkpointing_suspended = False
        self.fixed_rollback_boundary = None
        self.forward = [ ]
        self.old_store = { }

        # Did we just do a roll forward?
        self.rolled_forward = False

        # Reset the RNG on the creation of a new game.
        rng.reset()

        # True if we should retain data from here to the next checkpoint
        # on load.
        self.retain_after_load_flag = False

        # Has there been an interaction since the last time this log was
        # reset?
        self.did_interaction = True

    def after_setstate(self):
        self.mutated = { }
        self.rolled_forward = False

    def after_upgrade(self, version):
        if version < 2:
            self.ever_been_changed = { "store" : set(self.ever_been_changed) }
        if version < 3:
            self.rollback_is_fixed = False
            self.fixed_rollback_boundary = None
        if version < 4:
            self.retain_after_load_flag = False

        if version < 5:

            # We changed what the rollback limit represents, so recompute it
            # here.
            if self.rollback_limit:
                nrbl = 0

                for rb in self.log[-self.rollback_limit:]:
                    if rb.hard_checkpoint:
                        nrbl += 1

                self.rollback_limit = nrbl

    def begin(self, force=False):
        """
        Called before a node begins executing, to indicate that the
        state needs to be saved for rollbacking.
        """

        self.identifier_cache = None

        context = renpy.game.context()

        if not context.rollback:
            return

        # We only begin a checkpoint if the previous statement reached a checkpoint,
        # or an interaction took place. (Or we're forced.)
        if (not force) and (self.current and not self.current.checkpoint) and (not self.did_interaction):
            return

        self.did_interaction = False

        if self.current is not None:
            self.complete()
        else:
            for sd in store_dicts.itervalues():
                sd.begin()

        # If the log is too long, prune it.
        if len(self.log) > renpy.config.rollback_length:
            self.log = self.log[-renpy.config.rollback_length:]

        # check for the end of fixed rollback
        if self.log and self.log[-1] == self.current:

            if self.current.context.current == self.fixed_rollback_boundary:
                self.rollback_is_fixed = False

            elif self.rollback_is_fixed and not self.forward:
                # A lack of rollback data in fixed rollback mode ends rollback.
                self.fixed_rollback_boundary = self.current.context.current
                self.rollback_is_fixed = False

        self.current = Rollback()
        self.current.retain_after_load = self.retain_after_load_flag

        self.log.append(self.current)

        self.mutated = { }

        # Flag a mutation as having happened. This is used by the
        # save code.
        global mutate_flag
        mutate_flag = True

        self.rolled_forward = False

    def complete(self):
        """
        Called after a node is finished executing, before a save
        begins, or right before a rollback is attempted. This may be
        called more than once between calls to begin, and should always
        be called after an update to the store but before a rollback
        occurs.
        """

        # Update self.current.stores with the changes from each store.
        # Also updates .ever_been_changed.
        for name, sd in store_dicts.iteritems():
            self.current.stores[name] = sd.get_changes()

        # Update the list of mutated objects and what we need to do to
        # restore them.

        for _i in xrange(4):

            self.current.objects = [ ]

            try:
                for _k, v in self.mutated.iteritems():

                    if v is None:
                        continue

                    (ref, clean) = v

                    obj = ref()
                    if obj is None:
                        continue

                    compressed = obj._compress(clean)
                    self.current.objects.append((obj, compressed))

                break

            except RuntimeError:
                # This can occur when self.mutated is changed as we're
                # iterating over it.
                pass

    def get_roots(self):
        """
        Return a map giving the current roots of the store. This is a
        map from a variable name in the store to the value of that
        variable. A variable is only in this map if it has ever been
        changed since the init phase finished.
        """

        rv = { }

        for store_name, sd in store_dicts.iteritems():
            for name in sd.ever_been_changed:
                if name in sd:
                    rv[store_name + "." + name] = sd[name]
                else:
                    rv[store_name + "." + name] = deleted

        for i in reversed(renpy.game.contexts[1:]):
            i.pop_dynamic_roots(rv)

        return rv

    def purge_unreachable(self, roots, wait=None):
        """
        This is called to purge objects that are unreachable from the
        roots from the object rollback lists inside the Rollback entries.

        This should be called immediately after complete(), so that there
        are no changes queued up.
        """

        reachable = { }

        reached_vars(roots, reachable, wait)

        revlog = self.log[:]
        revlog.reverse()

        for i in revlog:
            if not i.purge_unreachable(reachable, wait):
                break

    def in_rollback(self):
        if self.forward:
            return True
        else:
            return False

    def in_fixed_rollback(self):
        return self.rollback_is_fixed

    def forward_info(self):
        """
        Returns the current forward info, if any.
        """

        if self.forward:

            name, data = self.forward[0]

            if self.current.context.current == name:
                return data

        return None

    def checkpoint(self, data=None, keep_rollback=False, hard=True):
        """
        Called to indicate that this is a checkpoint, which means
        that the user may want to rollback to just before this
        node.
        """

        if self.checkpointing_suspended:
            hard = False

        self.retain_after_load_flag = False

        if self.current.checkpoint:
            return

        if not renpy.game.context().rollback:
            return

        self.current.checkpoint = True

        if hard and (not self.current.hard_checkpoint):
            if self.rollback_limit < renpy.config.hard_rollback_limit:
                self.rollback_limit += 1
            self.current.hard_checkpoint = hard

        if self.in_fixed_rollback() and self.forward:
            # use data from the forward stack
            fwd_name, fwd_data = self.forward[0]
            if self.current.context.current == fwd_name:
                self.current.forward = fwd_data
                self.forward.pop(0)
            else:
                self.current.forward = data
                self.forward = [ ]

        elif data is not None:
            if self.forward:
                # If the data is the same, pop it from the forward stack.
                # Otherwise, clear the forward stack.
                fwd_name, fwd_data = self.forward[0]

                if (self.current.context.current == fwd_name
                        and data == fwd_data
                        and (keep_rollback or self.rolled_forward)
                    ):
                    self.forward.pop(0)
                else:
                    self.forward = [ ]

            # Log the data in case we roll back again.
            self.current.forward = data

    def suspend_checkpointing(self, flag):
        """
        Called to temporarily suspend checkpointing, so any rollback
        will jump to prior to this statement
        """

        self.checkpointing_suspended = flag

    def block(self):
        """
        Called to indicate that the user should not be able to rollback
        through this checkpoint.
        """

        self.rollback_limit = 0

    def retain_after_load(self):
        """
        Called to return data from this statement until the next checkpoint
        when the game is loaded.
        """

        self.retain_after_load_flag = True
        self.current.retain_after_load = True

    def fix_rollback(self):
        if not self.rollback_is_fixed and len(self.log) > 1:
            self.fixed_rollback_boundary = self.log[-2].context.current

    def can_rollback(self):
        """
        Returns True if we can rollback.
        """

        return self.rollback_limit > 0

    def rollback(self, checkpoints, force=False, label=None, greedy=True, on_load=False, abnormal=True):
        """
        This rolls the system back to the first valid rollback point
        after having rolled back past the specified number of checkpoints.

        If we're currently executing code, it's expected that complete()
        will be called before a rollback is attempted.

        force makes us throw an exception if we can't find a place to stop
        rolling back, otherwise if we run out of log this call has no
        effect.

        `label`
            A label that is called after rollback has finished, if the
            label exists.

        `greedy`
            If true, rollback will keep going until just after the last
            checkpoint. If False, it will stop immediately before the
            current statement.

        `on_load`
            Should be true if this rollback is being called in response to a
            load. Used to implement .retain_after_load()

        `abnormal`
            If true, treats this as an abnormal event, suppresisng rollback
            and so on.
        """

        # If we have exceeded the rollback limit, and don't have force,
        # give up.
        if checkpoints and (self.rollback_limit <= 0) and (not force):
            return

        self.suspend_checkpointing(False)
        # will always rollback to before suspension

        self.purge_unreachable(self.get_roots())

        revlog = [ ]

        # Find the place to roll back to.
        while self.log:
            rb = self.log.pop()
            revlog.append(rb)

            if rb.hard_checkpoint:
                self.rollback_limit -= 1

            if rb.hard_checkpoint or (on_load and rb.checkpoint):
                checkpoints -= 1

            if checkpoints <= 0:
                if renpy.game.script.has_label(rb.context.current):
                    break

        else:
            if force:
                raise Exception("Couldn't find a place to stop rolling back. Perhaps the script changed in an incompatible way?")

            # Otherwise, just give up.

            print("Can't find a place to rollback to. Not rolling back.")

            revlog.reverse()
            self.log = self.log + revlog
            return

        force_checkpoint = False

        # Try to rollback to just after the previous checkpoint.
        while greedy and self.log:

            rb = self.log[-1]

            if not renpy.game.script.has_label(rb.context.current):
                break

            if rb.checkpoint:

                # If the last checkpoint is a label, it's likely the start label.
                # go back to it.
                if isinstance(rb.context.current, basestring):
                    force_checkpoint = True
                    revlog.append(self.log.pop())

                break

            revlog.append(self.log.pop())

        # Decide if we're replacing the current context (rollback command),
        # or creating a new set of contexts (loading).
        if renpy.game.context().rollback:
            replace_context = False
            other_contexts = [ ]
        else:
            replace_context = True
            other_contexts = renpy.game.contexts[1:]
            renpy.game.contexts = renpy.game.contexts[0:1]

        if on_load and revlog[-1].retain_after_load:
            retained = revlog.pop()
        else:
            retained = None

        # Actually roll things back.
        for rb in revlog:
            rb.rollback()

            if rb.context.current == self.fixed_rollback_boundary:
                self.rollback_is_fixed = True

            if rb.forward is not None:
                self.forward.insert(0, (rb.context.current, rb.forward))

        if retained is not None:
            retained.rollback_control()
            self.log.append(retained)

        # Disable the next transition, as it's pointless. (Only when not used with a label.)
        renpy.game.interface.suppress_transition = abnormal

        # If necessary, reset the RNG.
        if force:
            rng.reset()
            self.forward = [ ]

        # Flag that we're in the transition immediately after a rollback.
        renpy.game.after_rollback = abnormal

        # Stop the sounds.
        renpy.audio.audio.rollback()

        # Stop any hiding in progress.
        for i in renpy.game.contexts:
            i.scene_lists.remove_all_hidden()

        renpy.game.contexts.extend(other_contexts)

        # Restart the context or the top context.
        if replace_context:

            if force_checkpoint:
                renpy.game.contexts[0].force_checkpoint = True

            raise renpy.game.RestartTopContext(label)

        else:

            if force_checkpoint:
                renpy.game.context().force_checkpoint = True

            raise renpy.game.RestartContext(label)

    def freeze(self, wait=None):
        """
        This is called to freeze the store and the log, in preparation
        for serialization. The next call on log should either be
        unfreeze (called after a serialization reload) or discard_freeze()
        (called after the save is complete).
        """

        # Purge unreachable objects, so we don't save them.
        self.complete()
        roots = self.get_roots()
        self.purge_unreachable(roots, wait=wait)

        # The current is not purged.
        self.current.purged = False

        return roots

    def discard_freeze(self):
        """
        Called to indicate that we will not be restoring from the
        frozen state.
        """

    def unfreeze(self, roots, label=None):
        """
        Used to unfreeze the game state after a load of this log
        object. This call will always throw an exception. If we're
        lucky, it's the one that indicates load was successful.

        @param roots: The roots returned from freeze.

        @param label: The label that is jumped to in the game script
        after rollback has finished, if it exists.
        """

        # Fix up old screens.
        renpy.display.screen.before_restart()  # @UndefinedVariable

        # Set us up as the game log.
        renpy.game.log = self

        clean_stores()
        renpy.translation.init_translation()

        for name, value in roots.iteritems():

            if "." in name:
                store_name, name = name.rsplit(".", 1)
            else:
                store_name = "store"

            if store_name not in store_dicts:
                continue

            store = store_dicts[store_name]
            store.ever_been_changed.add(name)

            if value is deleted:
                if name in store:
                    del store[name]
            else:
                store[name] = value

        # Now, rollback to an acceptable point.

        greedy = renpy.session.pop("_greedy_rollback", False)
        self.rollback(0, force=True, label=label, greedy=greedy, on_load=True)

        # Because of the rollback, we never make it this far.

    def build_identifier_cache(self):

        if self.identifier_cache is not None:
            return

        rollback_limit = self.rollback_limit
        checkpoints = 1

        self.identifier_cache = { }

        for i in reversed(self.log):

            if i.identifier is not None:
                if renpy.game.script.has_label(i.context.current):
                    self.identifier_cache[i.identifier] = checkpoints

            if i.hard_checkpoint:
                checkpoints += 1

            if i.checkpoint:
                rollback_limit -= 1

            if not rollback_limit:
                break

    def get_identifier_checkpoints(self, identifier):
        self.build_identifier_cache()
        return self.identifier_cache.get(identifier, None)


def py_exec_bytecode(bytecode, hide=False, globals=None, locals=None, store="store"):  # @ReservedAssignment

    if hide:
        locals = { }  # @ReservedAssignment

    if globals is None:
        globals = store_dicts[store]  # @ReservedAssignment

    if locals is None:
        locals = globals  # @ReservedAssignment

    exec bytecode in globals, locals


def py_exec(source, hide=False, store=None):

    if store is None:
        store = store_dicts["store"]

    if hide:
        locals = { }  # @ReservedAssignment
    else:
        locals = store  # @ReservedAssignment

    exec py_compile(source, 'exec') in store, locals


def py_eval_bytecode(bytecode, globals=None, locals=None):  # @ReservedAssignment

    if globals is None:
        globals = store_dicts["store"]  # @ReservedAssignment

    if locals is None:
        locals = globals  # @ReservedAssignment

    return eval(bytecode, globals, locals)


def py_eval(code, globals=None, locals=None):  # @ReservedAssignment
    if isinstance(code, basestring):
        code = py_compile(code, 'eval')

    return py_eval_bytecode(code, globals, locals)


def raise_at_location(e, loc):
    """
    Raises `e` (which must be an Exception object) at location `loc`.

    `loc`
        A location, which should be a (filename, line_number) tuple.
    """

    filename, line = loc

    node = ast.parse("raise e", filename)
    ast.increment_lineno(node, line - 1)
    code = compile(node, filename, 'exec')

    # PY3 - need to change to exec().
    exec code in { "e" : e }


# This was used to proxy accesses to the store. Now it's kept around to deal
# with cases where it might have leaked into a pickle.
class StoreProxy(object):

    def __getattr__(self, k):
        return getattr(renpy.store, k)  # @UndefinedVariable

    def __setattr__(self, k, v):
        setattr(renpy.store, k, v)  # @UndefinedVariable

    def __delattr__(self, k):
        delattr(renpy.store, k)  # @UndefinedVariable


# Code for pickling bound methods.
def method_pickle(method):
    name = method.im_func.__name__

    obj = method.im_self

    if obj is None:
        obj = method.im_class

    return method_unpickle, (obj, name)


def method_unpickle(obj, name):
    return getattr(obj, name)

# Code for pickling modules.


def module_pickle(module):
    if renpy.config.developer:
        raise Exception("Could not pickle {!r}.".format(module))

    return module_unpickle, (module.__name__,)


def module_unpickle(name):
    return __import__(name)


import copy_reg
import types

copy_reg.pickle(types.MethodType, method_pickle)
copy_reg.pickle(types.ModuleType, module_pickle)
