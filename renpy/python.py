# This file contains code that handles the execution of python code
# contained within the script file. It also handles rolling back the
# game state to some time in the past.

import renpy.game
import renpy.config
import renpy.object

import weakref

from compiler import parse
from compiler.pycodegen import ModuleCodeGenerator, ExpressionCodeGenerator
from compiler.misc import set_filename
import compiler.ast as ast


##### Code that replaces literals will calls to magic constructors.

def wrap_node(n):
    """
    Replaces literal lists and dictionaries, and list comprehensions,
    with calls to the appropriate Ren'Py constructors.
    """

    if isinstance(n, (ast.List, ast.ListComp)):
        n = ast.CallFunc(node=ast.Name('__renpy__list__'),
                         args=[ n ],
                         star_args=None,
                         dstar_args=None,
                         )

    elif isinstance(n, ast.Dict):
        n = ast.CallFunc(node=ast.Name('__renpy__dict__'),
                         args=[ n ],
                         star_args=None,
                         dstar_args=None,
                         )

    return n


def recursively_replace(o, func):
    """
    Walks through a compiler AST, calling the supplied function when a
    node is encountered, and replacing the node with the return value.
    """

    if isinstance(o, list):
        return [ recursively_replace(i, func) for i in o ]

    if isinstance(o, ast.Node):
        for k in vars(o):
            setattr(o, k, recursively_replace(getattr(o, k), func))

        return func(o)

    return o

def py_compile(source, mode):
    """
    Compiles the given source code using the supplied codegenerator.
    Lists, List Comprehensions, and Dictionaries are wrapped when
    appropriate.
    """

    tree = parse(source, mode)

    recursively_replace(tree, wrap_node)

    if mode == 'exec':
        set_filename("<none>", tree)
        cg = ModuleCodeGenerator(tree)
    else:
        set_filename("<none>", tree)
        cg = ExpressionCodeGenerator(tree)
        
    return cg.getCode()


##### Classes that are exported in place of the normal list, dict, and
##### object.

def mutator(method):

    def do_mutation(self, *args, **kwargs):

        mutated = renpy.game.log.mutated

        if id(self) not in mutated:
            mutated[id(self)] = ( weakref.ref(self), self.get_rollback())
        
        
        return method(self, *args, **kwargs)

    return do_mutation

class RevertableList(list):

    __delitem__ = mutator(list.__delitem__)
    __delslice__ = mutator(list.__delslice__)
    __setitem__ = mutator(list.__setitem__)
    __setslice__ = mutator(list.__setslice__)
    append = mutator(list.append)
    extend = mutator(list.extend)
    insert = mutator(list.insert)
    pop = mutator(list.pop)
    remove = mutator(list.remove)
    reverse = mutator(list.reverse)
    sort = mutator(list.sort)

    # TODO: Handle __iter__ (or not).
    
    
    def get_rollback(self):
        return self[:]

    def rollback(self, old):
        self[:] = old

class RevertableDict(dict):

    __delitem__ = mutator(dict.__delitem__)
    __setitem__ = mutator(dict.__setitem__)
    clear = mutator(dict.clear)
    pop = mutator(dict.pop)
    popitem = mutator(dict.popitem)
    values = mutator(dict.values)

    def copy(self):
        return RevertableDict(dict.copy(self))

    def get_rollback(self):
        return self.items()

    def rollback(self, old):
        self.clear()

        for k, v in old:
            self[k] = v

class RevertableObject(object):

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value

    def __delattr__(self, attr):
        del self.__dict__[attr]

    __setattr__ = mutator(__setattr__)
    __delattr__ = mutator(__delattr__)

    def get_rollback(self):
        return self.__dict__.copy()

    def rollback(self, old):
        self.__dict__.clear()
        self.__dict__.update(old)


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
    """

    def __init__(self):
        self.context = renpy.game.contexts[0].rollback_copy()
        self.objects = { }
        self.store = [ ]
        self.checkpoint = False

    def rollback(self):
        """
        This reverts the game state to the state it was in when this
        Rollback was first created.
        """

        for obj, roll in self.objects:
            obj.rollback(roll)

        for t in self.store:
            if len(t) == 2:
                k, v = t
                renpy.game.store[k] = v
            else:
                k, = t
                del renpy.game.store[k]

        renpy.game.contexts = [ self.context ]
        

class RollbackLog(renpy.object.Object):
    """
    This class manages the list of Rollback objects.

    @ivar log: The log of rollback objects.

    @ivar current: The current rollback object. (Equivalent to
    log[-1])

    Not serialized:
    
    @ivar old_store: A copy of the store as it was when begin was
    last called.

    @ivar mutated: A dictionary that maps object ids to a tuple of
    (weakref to object, information needed to rollback that object)
    """

    nosave = [ 'old_store', 'mutated' ]

    def __init__(self):
        self.log = [ ]
        self.current = None
        self.mutated = { }

    def after_setstate(self):
        self.mutated = { }

    def begin(self):
        """
        Called before a node begins executing, to indicate that the
        state needs to be saved for rollbacking.
        """

        # Prune the log, if necessary.
        if len(self.log) > renpy.config.rollback_maximum:
            self.log = self.log[renpy.config.rollback_prune:]

        self.current = Rollback()
        self.log.append(self.current)

        self.mutated = { }
        self.old_store = renpy.game.store.copy()

    def complete(self):
        """
        Called after a node is finished executing, before a save
        begins, or right before a rollback is attempted. This may be
        called more than once between calls to begin, and should always
        be called after an update to the store but before a rollback
        occurs.
        """

        new_store = renpy.game.store
        store = [ ]

        for k, v in self.old_store.iteritems():
            if k not in new_store or new_store[k] is not v:
                store.append((k, v))

        for k in new_store:
            if k not in self.old_store:
                store.append((k, ))

        self.current.store = store

        self.current.objects = [ ]
        
        for k, (ref, roll) in self.mutated.iteritems():

            obj = ref()
            if not obj:
                continue

            self.current.objects.append((obj, roll))
            

    def checkpoint(self):
        """
        Called to indicate that this is a checkpoint, which means
        that the user may want to rollback to just before this
        node.
        """
        
        self.current.checkpoint = True

    def rollback(self, checkpoints, force=False):
        """
        This rolls the system back to the first valid rollback point
        after having rolled back past the specified number of checkpoints.

        If we're currently executing code, it's expected that complete()
        will be called before a rollback is attempted.

        force makes us throw an exception if we can't find a place to stop
        rolling back, otherwise if we run out of log this call has no
        effect.
        """

        revlog = [ ]

        while self.log:
            rb = self.log.pop()
            revlog.append(rb)

            if rb.checkpoint:
                checkpoints -= 1

            if checkpoints <= 0:
                if renpy.game.script.has_label(rb.context.current):
                    break

        else:
            if force:
                raise Exception("Couldn't find a place to stop rolling back. Perhaps the ")
                
            # Otherwise, just give up.

            print "Can't find a place to rollback to. Not rolling back."

            revlog.reverse()
            self.log = revlog
            return

        for rb in revlog:
            rb.rollback()

        # Restart the game with the new state.
        raise renpy.game.RestartException()
                

def py_exec(source, hide=False):

    if hide:
        locals = { }
    else:
        locals = renpy.game.store


    exec py_compile(source, 'exec') in renpy.game.store, locals

def py_eval(source):
    source = source.strip()
    
    return eval(py_compile(source, 'eval'),
                renpy.game.store)
