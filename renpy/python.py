# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

# Import the python ast module, not ours.
ast = __import__("ast", { })

import marshal
import random
import weakref
import re
import sets
import sys

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
        self.old = { }

        # The set of variables in this StoreDict that changed since the
        # end of the init phase.
        self.ever_been_changed = set()

    def begin(self):
        """
        Called to mark the start of a rollback period.
        """

        self.old = dict(self)

    def get_changes(self):
        """
        For every key that has changed since begin() was called, returns a
        dictionary mapping the key to its value when begin was called, or
        deleted if it did not exist when begin was called.

        As a side-effect, updates self.ever_been_changed.
        """

        rv = { }

        for k in self:
            if k not in self.old:
                rv[k] = deleted

        for k, v in self.old.iteritems():

            new_v = self.get(k, deleted)

            if new_v is not v:
                rv[k] = v

        for k in rv:
            self.ever_been_changed.add(k)

        return rv


# A map from the name of a store dict to the corresponding StoreDict object.
store_dicts = { }

def create_store(name):
    """
    Creates the store with `name`.
    """

    name = str(name)

    if name in store_dicts:
        return

    # Create the dict.
    d = StoreDict()
    store_dicts[name] = d

    # Set the name.
    d["__name__"] = name
    d["__package__"] = name

    # Set up the default contents of the store.
    eval("1", d)

    for k, v in renpy.minstore.__dict__.iteritems():
        if k not in d:
            d[k] = v

    # Create the corresponding module.
    sys.modules[name] = StoreModule(d)

    # If we're a module in the store, add us to the store.
    if name.startswith("store."):
        store_dicts["store"][name[6:]] = sys.modules[name]

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


        for k, v in store_dicts.iteritems():
            self.store[k] = dict(v)
            self.old[k] = dict(v.old)
            self.ever_been_changed[k] = set(v.ever_been_changed)

    def restore(self):

        for k, sd in store_dicts.iteritems():

            sd.clear()
            sd.update(self.store[k])

            sd.old.clear()
            sd.old.update(self.old[k])

            sd.ever_been_changed.clear()
            sd.ever_been_changed.update(self.ever_been_changed[k])



clean_store_backup = None

def make_clean_stores():
    """
    Copy the clean stores.
    """

    global clean_store_backup

    for _k, v in store_dicts.iteritems():

        v.old.clear()
        v.ever_been_changed.clear()

    clean_store_backup = StoreBackup()

def clean_stores():
    """
    Revert the store to the clean copy.
    """

    clean_store_backup.restore()

##### Code that computes reachable objects, which is used to filter
##### the rollback list before rollback or serialization.

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

    if isinstance(obj, NoRollback):
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


##### Code that replaces literals will calls to magic constructors.

class WrapNode(ast.NodeTransformer):

    def visit_ListComp(self, n):
        return ast.Call(
            func = ast.Name(
                id="__renpy__list__",
                ctx=ast.Load()
                ),
            args = [ self.generic_visit(n) ],
            keywords = [ ],
            starargs = None,
            kwargs = None)

    def visit_List(self, n):
        if not isinstance(n.ctx, ast.Load):
            return self.generic_visit(n)

        return ast.Call(
            func = ast.Name(
                id="__renpy__list__",
                ctx=ast.Load()
                ),
            args = [ self.generic_visit(n) ],
            keywords = [ ],
            starargs = None,
            kwargs = None)

    def visit_Dict(self, n):

        return ast.Call(
            func = ast.Name(
                id="__renpy__dict__",
                ctx=ast.Load()
                ),
            args = [ self.generic_visit(n) ],
            keywords = [ ],
            starargs = None,
            kwargs = None)

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

def py_compile(source, mode, filename='<none>', lineno=1):
    """
    Compiles the given source code using the supplied codegenerator.
    Lists, List Comprehensions, and Dictionaries are wrapped when
    appropriate.

    @param source: The source code, as a string.

    @param mode: 'exec' or 'eval'.

    @param filename: The filename that the source code is taken from.

    @param lineno: The line number of the first line of the source code.
    """

    if isinstance(source, ast.Module):
        return compile(source, filename, mode)

    if isinstance(source, renpy.ast.PyExpr):
        filename = source.filename
        lineno = source.linenumber

    source = unicode(source)
    source = source.replace("\r", "")
    source = escape_unicode(source)

    try:
        line_offset = lineno - 1

        tree = ast.parse(source, filename, mode)

        tree = wrap_node.visit(tree)

        ast.fix_missing_locations(tree)
        ast.increment_lineno(tree, lineno - 1)

        line_offset = 0

        return compile(tree, filename, mode)

    except SyntaxError, e:

        if e.lineno is not None:
            e.lineno += line_offset

        raise e

def py_compile_exec_bytecode(source, **kwargs):
    code = py_compile(source, 'exec', **kwargs)
    return marshal.dumps(code)


def py_compile_eval_bytecode(source, **kwargs):
    source = source.strip()
    code = py_compile(source, 'eval', **kwargs)
    return marshal.dumps(code)



##### Classes that are exported in place of the normal list, dict, and
##### object.

# This is set to True whenever a mutation occurs. The save code uses
# this to check to see if a background-save is valid.
mutate_flag = True

def mutator(method):

    def do_mutation(self, *args, **kwargs):

        global mutate_flag

        mutated = renpy.game.log.mutated #@UndefinedVariable

        if id(self) not in mutated:
            mutated[id(self)] = ( weakref.ref(self), self.get_rollback())
            mutate_flag = True

        return method(self, *args, **kwargs)

    return do_mutation

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

    def wrapper(method): # E0213 @NoSelf
        def newmethod(*args, **kwargs):
            return RevertableList(method(*args, **kwargs)) # E1102

        return newmethod

    __add__ = wrapper(list.__add__)
    __getslice__ = wrapper(list.__getslice__)
    __mul__ = wrapper(list.__mul__)
    __rmul__ = wrapper(list.__rmul__)

    del wrapper

    def get_rollback(self):
        return self[:]

    def rollback(self, old):
        self[:] = old

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

    def list_wrapper(method): # E0213 @NoSelf
        def newmethod(*args, **kwargs):
            return RevertableList(method(*args, **kwargs)) # E1102

        return newmethod

    keys = list_wrapper(dict.keys)
    values = list_wrapper(dict.values)
    items = list_wrapper(dict.items)

    del list_wrapper

    def copy(self):
        rv = RevertableDict()
        rv.update(self)
        return rv

    def get_rollback(self):
        return self.items()

    def rollback(self, old):
        self.clear()

        for k, v in old:
            self[k] = v

class RevertableSet(sets.Set):

    def __init__(self, *args):
        log = renpy.game.log

        if log is not None:
            log.mutated[id(self)] = None

        sets.Set.__init__(self, *args)

    __iand__ = mutator(sets.Set.__iand__)
    __ior__ = mutator(sets.Set.__ior__)
    __isub__ = mutator(sets.Set.__isub__)
    __ixor__ = mutator(sets.Set.__ixor__)
    add = mutator(sets.Set.add)
    clear = mutator(sets.Set.clear)
    difference_update = mutator(sets.Set.difference_update)
    discard = mutator(sets.Set.discard)
    intersection_update = mutator(sets.Set.intersection_update)
    pop = mutator(sets.Set.pop)
    remove = mutator(sets.Set.remove)
    symmetric_difference_update = mutator(sets.Set.symmetric_difference_update)
    union_update = mutator(sets.Set.union_update)
    update = mutator(sets.Set.update)

    def wrapper(method): # E0213 @NoSelf
        def newmethod(*args, **kwargs):
            rv = method(*args, **kwargs) # E1102
            if isinstance(rv, sets.Set):
                return RevertableSet(rv)
            else:
                return rv

        return newmethod

    __and__ = wrapper(sets.Set.__and__)
    __copy__ = wrapper(sets.Set.__copy__)
    __deepcopy__ = wrapper(sets.Set.__deepcopy__)
    __sub__ = wrapper(sets.Set.__sub__)
    __xor__ = wrapper(sets.Set.__xor__)
    __or__ = wrapper(sets.Set.__or__)
    copy = wrapper(sets.Set.copy)
    difference = wrapper(sets.Set.difference)
    intersection = wrapper(sets.Set.intersection)
    symmetric_difference = wrapper(sets.Set.symmetric_difference)
    union = wrapper(sets.Set.union)

    del wrapper

    def get_rollback(self):
        return list(self)

    def rollback(self, old):
        sets.Set.clear(self)
        sets.Set.update(self, old)


class RevertableObject(object):

    def __new__(cls, *args, **kwargs):
        self = super(RevertableObject, cls).__new__(cls, *args, **kwargs)

        log = renpy.game.log
        if log is not None:
            log.mutated[id(self)] = None

        return self

    def __setattr__(self, attr, value):
        object.__setattr__(self, attr, value)

    def __delattr__(self, attr):
        object.__delattr__(self, attr)

    __setattr__ = mutator(__setattr__)
    __delattr__ = mutator(__delattr__)

    def get_rollback(self):
        return self.__dict__.copy()

    def rollback(self, old):
        self.__dict__.clear()
        self.__dict__.update(old)


##### An object that handles deterministic randomness, or something.

class DetRandom(random.Random):

    def __init__(self):
        super(DetRandom, self).__init__()
        self.stack = [ ]

    def random(self):

        if self.stack:
            rv = self.stack.pop()
        else:
            rv = super(DetRandom, self).random()

        renpy.game.log.current.random.append(rv)
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

rng = DetRandom()

##### This is the code that actually handles the logging and managing
##### of the rollbacks.

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

    __version__ = 2

    def __init__(self):

        super(Rollback, self).__init__()

        self.context = renpy.game.context().rollback_copy()
        self.objects = [ ]
        self.checkpoint = False
        self.purged = False
        self.random = [ ]
        self.forward = None

        # A map of maps name -> (variable -> value)
        self.stores = { }

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
                    print "Removing unreachable:", o

                    pass

        self.objects = new_objects

        return True


    def rollback(self):
        """
        This reverts the game state to the state it was in when this
        Rollback was first created.
        """

        for obj, roll in reversed(self.objects):
            if roll is not None:
                obj.rollback(roll)

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

        renpy.game.contexts.pop()
        renpy.game.contexts.append(self.context)

        rng.pushback(self.random)


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

    __version__ = 3


    nosave = [ 'old_store', 'mutated' ]

    def __init__(self):

        super(RollbackLog, self).__init__()

        self.log = [ ]
        self.current = None
        self.mutated = { }
        self.rollback_limit = 0
        self.rollback_is_fixed = False
        self.fixed_rollback_boundary = None
        self.forward = [ ]
        self.old_store = { }

        # Did we just do a roll forward?
        self.rolled_forward = False

        # Reset the RNG on the creation of a new game.
        rng.reset()

    def after_setstate(self):
        self.mutated = { }
        self.rolled_forward = False

    def after_upgrade(self, version):
        if version < 2:
            self.ever_been_changed = { "store" : set(self.ever_been_changed) }
        if version < 3:
            self.rollback_is_fixed = False
            self.fixed_rollback_boundary = None

    def begin(self):
        """
        Called before a node begins executing, to indicate that the
        state needs to be saved for rollbacking.
        """

        context = renpy.game.context()
        if not context.rollback:
            return

        # If the transient scene list is not empty, then we do
        # not begin a new rollback, as the TSL will be purged
        # after a rollback is complete.
        if not context.scene_lists.transient_is_empty():
            return

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
        self.log.append(self.current)

        self.mutated = { }

        # Flag a mutation as having happened. This is used by the
        # save code.
        global mutate_flag
        mutate_flag = True

        self.rolled_forward = False

        # Reset the point that changes are relative to.
        for sd in store_dicts.itervalues():
            sd.begin()

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

                    (ref, roll) = v

                    obj = ref()
                    if obj is None:
                        continue

                    self.current.objects.append((obj, roll))

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

    def checkpoint(self, data=None, keep_rollback=False):
        """
        Called to indicate that this is a checkpoint, which means
        that the user may want to rollback to just before this
        node.
        """

        if self.current.checkpoint:
            return

        if not renpy.game.context().rollback:
            return

        if self.rollback_limit < renpy.config.hard_rollback_limit:
            self.rollback_limit += 1

        self.current.checkpoint = True

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

    def block(self):
        """
        Called to indicate that the user should not be able to rollback
        through this checkpoint.
        """

        self.rollback_limit = 0

    def fix_rollback(self):
        if not self.rollback_is_fixed and len(self.log) > 1:
            self.fixed_rollback_boundary = self.log[-2].context.current

    def can_rollback(self):
        """
        Returns True if we can rollback.
        """

        return self.rollback_limit > 0

    def rollback(self, checkpoints, force=False, label=None, greedy=True):
        """
        This rolls the system back to the first valid rollback point
        after having rolled back past the specified number of checkpoints.

        If we're currently executing code, it's expected that complete()
        will be called before a rollback is attempted.

        force makes us throw an exception if we can't find a place to stop
        rolling back, otherwise if we run out of log this call has no
        effect.

        @param label: The label that is called in the game script
        after rollback has finished, if it exists.

        `greedy`
            If true, rollback will keep going until just after the last
            checkpoint. If False, it will stop immediately before the
            current statement.
        """

        # If we have exceeded the rollback limit, and don't have force,
        # give up.
        if checkpoints and not self.rollback_limit > 0 and not force:
            return

        self.purge_unreachable(self.get_roots())

        revlog = [ ]

        # Find the place to roll back to.
        while self.log:
            rb = self.log.pop()
            revlog.append(rb)

            if rb.checkpoint:
                checkpoints -= 1
                self.rollback_limit -= 1

            if checkpoints <= 0:
                if renpy.game.script.has_label(rb.context.current):
                    break

        else:
            if force:
                raise Exception("Couldn't find a place to stop rolling back. Perhaps the script changed in an incompatible way?")

            # Otherwise, just give up.

            print "Can't find a place to rollback to. Not rolling back."

            revlog.reverse()
            self.log = self.log + revlog
            return

        # Try to rollback to just after the previous checkpoint.
        while greedy and self.log:

            rb = self.log[-1]

            if rb.checkpoint:
                break

            if not renpy.game.script.has_label(rb.context.current):
                break

            if self.rollback_limit <= 0:
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

        # Actually roll things back.
        for rb in revlog:
            rb.rollback()

            if rb.context.current == self.fixed_rollback_boundary:
                self.rollback_is_fixed = True

            if rb.forward is not None:
                self.forward.insert(0, (rb.context.current, rb.forward))

        # Disable the next transition, as it's pointless. (Only when not used with a label.)
        renpy.game.interface.suppress_transition = True

        # If necessary, reset the RNG.
        if force:
            rng.reset()
            self.forward = [ ]

        # Flag that we're in the transition immediately after a rollback.
        renpy.game.after_rollback = True

        # Stop the sounds.
        renpy.audio.audio.rollback()

        renpy.game.contexts.extend(other_contexts)

        # Restart the context or the top context.
        if replace_context:
            raise renpy.game.RestartTopContext(label)
        else:
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
        renpy.display.screen.before_restart() # @UndefinedVariable

        # Set us up as the game log.
        renpy.game.log = self

        clean_stores()

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
        self.rollback(0, force=True, label=label, greedy=False)

        # Because of the rollback, we never make it this far.


def py_exec_bytecode(bytecode, hide=False, globals=None, locals=None, store="store"): #@ReservedAssignment

    if hide:
        locals = { } #@ReservedAssignment

    if globals is None:
        globals = store_dicts[store] #@ReservedAssignment

    if locals is None:
        locals = globals #@ReservedAssignment

    exec bytecode in globals, locals


def py_exec(source, hide=False, store=None):

    if store is None:
        store = store_dicts["store"]

    if hide:
        locals = { } #@ReservedAssignment
    else:
        locals = store #@ReservedAssignment

    exec py_compile(source, 'exec') in store, locals


def py_eval_bytecode(bytecode, globals=None, locals=None): #@ReservedAssignment

    if globals is None:
        globals = store_dicts["store"] #@ReservedAssignment

    if locals is None:
        locals = globals #@ReservedAssignment

    return eval(bytecode, globals, locals)

def py_eval(source, globals=None, locals=None): #@ReservedAssignment

    if globals is None:
        globals = store_dicts["store"] #@ReservedAssignment

    if locals is None:
        locals = globals #@ReservedAssignment

    return eval(py_compile(source, 'eval'), globals, locals)


# This was used to proxy accesses to the store. Now it's kept around to deal
# with cases where it might have leaked into a pickle.
class StoreProxy(object):

    def __getattr__(self, k):
        return getattr(renpy.store, k) #@UndefinedVariable

    def __setattr__(self, k, v):
        setattr(renpy.store, k, v) #@UndefinedVariable

    def __delattr__(self, k):
        delattr(renpy.store, k) #@UndefinedVariable


# Code for pickling bound methods.
def method_pickle(method):
    name = method.im_func.__name__

    obj = method.im_self

    if obj is None:
        obj = method.im_class

    return method_unpickle, (obj, name)

def method_unpickle(obj, name):
    return getattr(obj, name)

import copy_reg
import types
copy_reg.pickle(types.MethodType, method_pickle, method_unpickle)
