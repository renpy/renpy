# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

# NOTE:
# When updating this file, consider if lint.py or warp.py also need
# updating.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Optional, Any

import renpy

import hashlib
import re
import time


def statement_name(name):
    """
    Reports the name of this statement to systems like window auto.
    """

    for i in renpy.config.statement_callbacks:
        i(name)


def next_node(n):
    """
    Indicates the next node that should be executed. When a statement
    can crash, this should be set as early as possible, so that ignore
    can bring us there.
    """

    renpy.game.context().next_node = n


class ParameterInfo(object):
    """
    This class is used to store information about parameters to a
    label.
    """

    positional_only = [ ]
    keyword_only = [ ]

    def __init__(self, parameters, positional, extrapos, extrakw, last_posonly=None, first_kwonly=None):

        # A list of (parameter name, default value) pairs.
        # The default value is either None (if there is none)
        # or a string which when evaluated results in the actual value
        self.parameters = parameters

        # A list, giving the names of the positional parameters
        # to this function, in order.
        self.positional = positional

        # A variable that takes the extra positional arguments, if
        # any. None if no such variable exists.
        # If there is *args, this is "args".
        self.extrapos = extrapos

        # A variable that takes the extra keyword arguments, if
        # any. None if no such variable exists.
        # If there is **properties, this is "properties".
        self.extrakw = extrakw

        # The parameters which are positional-only, see
        # https://www.python.org/dev/peps/pep-0570/
        # Empty if / not present.
        if last_posonly is None:
            self.positional_only = [ ]
        else:
            rv = [ ]
            for param in parameters:
                rv.append(param)
                if param[0] == last_posonly:
                    break

            self.positional_only = rv

        # The parameters which are keyword-only, see
        # https://www.python.org/dev/peps/pep-3102/
        # Empty if * nor *args are present, or if there are no parameters after them.
        if first_kwonly is None:
            self.keyword_only = [ ]
        else:
            rv = [ ]
            for param in reversed(parameters):
                rv.append(param)
                if param[0] == first_kwonly:
                    break

            rv.reverse()
            self.keyword_only = rv

    def apply(self, args, kwargs, ignore_errors=False):
        """
        Applies `args` and `kwargs` to these parameters. Returns
        a dictionary that can be used to update an enclosing
        scope.

        `ignore_errors`
            If true, errors will be ignored, and this function will do the
            best job it can.
        """

        rv = { }

        if args is None:
            args = [ ]

        if kwargs is None:
            kwargs = renpy.python.RevertableDict()
        else:
            # Prevent original kwargs changes
            kwargs = kwargs.copy()

        parameters = self.parameters
        # Handle empty parameters in a fast way
        if not parameters:

            if self.extrakw:
                rv[self.extrakw] = kwargs

            elif kwargs and (not ignore_errors):
                if not kwargs.pop("_ignore_extra_kwargs", False):
                    raise TypeError(
                        "Unexpected keyword arguments: %s" %
                        ", ".join("'%s'" % i for i in kwargs))

            if self.extrapos:
                rv[self.extrapos] = tuple(args)

            elif args and (not ignore_errors):
                raise TypeError("Too many arguments in call (expected 0, got %d)." % len(args))

            return rv

        # Fill positional-only slots and check whether its passed as keyword
        slots = iter(self.positional_only)
        argsi = iter(args)
        missed_pos = [ ]
        posonly_keyword = [ ]
        for value in argsi:
            try:
                name, _ = next(slots)
            except StopIteration:
                argsi = iter([ value ] + list(argsi))
                break

            if name in kwargs:
                posonly_keyword.append(name)

            rv[name] = value

        # Some parameters left
        else:
            for name, default in slots:
                if name in kwargs:
                    posonly_keyword.append(name)

                if default is not None:
                    rv[name] = renpy.python.py_eval(default)
                else:
                    missed_pos.append(name)

            argsi = iter([])

        # Report positional-only as keyword if we have not **kwargs
        if posonly_keyword and self.extrakw is None:
            if not ignore_errors:
                raise TypeError(
                    "Some positional-only arguments passed as keyword arguments: %s" %
                    ", ".join("'%s'" % i for i in posonly_keyword))
            else:
                for name in posonly_keyword:
                    kwargs.pop(name)

        # Fill positional_or_keyword slots with left args
        poskw_slots = parameters[len(self.positional_only):-len(self.keyword_only) or None]
        slots = iter(poskw_slots)
        extraargs = [ ]
        duplicated_names = [ ]
        for value in argsi:
            try:
                name, _ = next(slots)
            except StopIteration:
                extraargs = [ value ] + list(argsi)
                break

            rv[name] = value

            if name in kwargs:
                kwargs.pop(name)
                duplicated_names.append(name)

        # Some parameters left
        else:
            for name, default in slots:
                if name in kwargs:
                    rv[name] = kwargs.pop(name)
                elif default is not None:
                    rv[name] = renpy.python.py_eval(default)
                else:
                    missed_pos.append(name)

        # Report missing positional parameters
        if missed_pos and (not ignore_errors):
            raise TypeError(
                "Missing required positional arguments: %s" %
                ", ".join("'%s'" % i for i in missed_pos))

        if self.extrapos:
            rv[self.extrapos] = tuple(extraargs)

        # Report extra positional arguments
        elif extraargs and (not ignore_errors):
            positional = self.positional_only + poskw_slots
            required = len([i for i in positional if i[1] is None])
            total = len(positional)

            if total == required:
                expected = str(total)
            else:
                expected = "from %d to %d" % (required, total)

            raise TypeError(
                "Too many arguments in call (expected %s, got %d)." %
                (expected, len(args)))

        # Report duplicated positional parameters
        if duplicated_names and (not ignore_errors):
            raise TypeError(
                "Got multiple values for arguments: %s" %
                ", ".join("'%s'" % i for i in duplicated_names))

        # Fill keyword-only parameters
        missed_kw = [ ]
        for name, default in self.keyword_only:
            if name in kwargs:
                rv[name] = kwargs.pop(name)
            elif default is not None:
                rv[name] = renpy.python.py_eval(default)
            else:
                missed_kw.append(name)

        # Report missing keyword-only parameters
        if missed_kw and (not ignore_errors):
            raise TypeError(
                "Missing required keyword-only arguments: %s" %
                ", ".join("'%s'" % i for i in missed_kw))

        if self.extrakw:
            rv[self.extrakw] = kwargs

        elif kwargs and (not ignore_errors):
            if not kwargs.pop("_ignore_extra_kwargs", False):
                raise TypeError(
                    "Unexpected keyword arguments: %s" %
                    ", ".join("'%s'" % i for i in kwargs))

        return rv


def apply_arguments(parameters, args, kwargs, ignore_errors=False):

    if parameters is None:
        if (args or kwargs) and not ignore_errors:
            raise Exception("Arguments supplied, but parameter list not present")
        else:
            return { }

    return parameters.apply(args, kwargs, ignore_errors)


class ArgumentInfo(renpy.object.Object):

    __version__ = 1
    starred_indexes = set()
    doublestarred_indexes = set()

    def after_upgrade(self, version):
        if version < 1:
            arguments = self.arguments
            extrapos = self.extrapos # type: ignore
            extrakw = self.extrakw # type: ignore
            length = len(arguments) + bool(extrapos) + bool(extrakw)
            if extrapos:
                self.starred_indexes = { length - 1 }
                arguments.append((None, extrapos))

            if extrakw:
                self.doublestarred_indexes = { length - 1 }
                arguments.append((None, extrakw))

            if extrapos and extrakw:
                self.starred_indexes = { length - 2 }

    def __init__(self, arguments, starred_indexes=None, doublestarred_indexes=None):

        # A list of (keyword, expression) pairs. If an argument doesn't
        # have a keyword, it's thought of as positional.
        self.arguments = arguments

        # Indexes of arguments to be considered as * unpacking
        self.starred_indexes = starred_indexes or set()

        # Indexes of arguments to be considered as ** unpacking.
        self.doublestarred_indexes = doublestarred_indexes or set()

    def evaluate(self, scope=None):
        """
        Evaluates the arguments, returning a tuple of arguments and a
        dictionary of keyword arguments.
        """

        args = [ ]
        kwargs = renpy.revertable.RevertableDict()

        for i, (k, v) in enumerate(self.arguments):
            value = renpy.python.py_eval(v, locals=scope)

            if i in self.starred_indexes:
                args.extend(value)

            elif i in self.doublestarred_indexes:
                kwargs.update(value)

            elif k is not None:
                kwargs[k] = value
            else:
                args.append(value)

        return tuple(args), kwargs

    def get_code(self):

        l = [ ]

        for i, (keyword, expression) in enumerate(self.arguments):

            if i in self.starred_indexes:
                l.append("*" + expression)

            elif i in self.doublestarred_indexes:
                l.append("**" + expression)

            elif keyword is not None:
                l.append("{}={}".format(keyword, expression))
            else:
                l.append(expression)

        return "(" + ", ".join(l) + ")"


EMPTY_PARAMETERS = ParameterInfo([ ], [ ], None, None, None, None)
EMPTY_ARGUMENTS = ArgumentInfo([ ], None, None)


def __newobj__(cls, *args):
    return cls.__new__(cls, *args)



class PyExpr(str):
    """
    Represents a string containing python code.
    """

    __slots__ = [
        'filename',
        'linenumber',
        'py',
        ]

    def __new__(cls, s, filename, linenumber, py=3):
        self = str.__new__(cls, s)
        self.filename = filename # type: ignore
        self.linenumber = linenumber # type: ignore
        self.py = py # type: ignore

        # Queue the string for precompilation.
        if self and (renpy.game.script.all_pyexpr is not None):
            renpy.game.script.all_pyexpr.append(self)

        return self

    def __getnewargs__(self):
        return (str(self), self.filename, self.linenumber, self.py)

    @staticmethod
    def checkpoint():
        """
        Checkpoints the pyexpr list. Returns an opaque object that can be used
        to revert the list.
        """

        if renpy.game.script.all_pyexpr is None:
            return None

        return len(renpy.game.script.all_pyexpr)

    @staticmethod
    def revert(opaque):

        if renpy.game.script.all_pyexpr is None:
            return

        if opaque is None:
            return

        renpy.game.script.all_pyexpr[opaque:] = [ ]


def probably_side_effect_free(expr):
    """
    Returns true if an expr probably does not have side effects, and should
    be predicted. Basically, this just whitelists a set of characters that
    doesn't allow for a function call.
    """

    return not ("(" in expr)


class PyCode(object):

    __slots__ = [
        'source',
        'location',
        'mode',
        'bytecode',
        'hash',
        'py',
        ]

    def __getstate__(self):
        return (1, self.source, self.location, self.mode, self.py)

    def __setstate__(self, state):
        if len(state) == 4:
            (_, self.source, self.location, self.mode) = state
            self.py = 2
        else:
            (_, self.source, self.location, self.mode, self.py) = state

        self.bytecode = None

        if renpy.game.script.record_pycode:
            renpy.game.script.all_pycode.append(self)

    def __init__(self, source, loc=('<none>', 1), mode='exec'):

        if isinstance(source, PyExpr):
            loc = (source.filename, source.linenumber, source)

        if PY2:
            self.py = 2
        else:
            self.py = 3

        # The source code.
        self.source = source

        # The time is necessary so we can disambiguate between Python
        # blocks on the same line in different script versions.
        self.location = loc + (int(time.time()),)
        self.mode = mode

        # This will be initialized later on, after we are serialized.
        self.bytecode = None

        if renpy.game.script.record_pycode:
            renpy.game.script.all_pycode.append(self)

        self.hash = self.get_hash()

    def get_hash(self):
        try:
            if self.hash is not None:
                return self.hash
        except Exception:
            pass

        code = self.source
        if isinstance(code, renpy.python.ast.AST): # @UndefinedVariable
            code = renpy.python.ast.dump(code) # @UndefinedVariable

        self.hash = bchr(renpy.bytecode_version) + hashlib.md5((repr(self.location) + code).encode("utf-8")).digest() # type:ignore
        return self.hash


def chain_block(block, next): # @ReservedAssignment
    """
    This is called to chain together all of the nodes in a block. Node
    n is chained with node n+1, while the last node is chained with
    next.
    """

    if not block:
        return

    for a, b in zip(block, block[1:]):
        a.chain(b)

    block[-1].chain(next)


DoesNotExtend = renpy.object.Sentinel("DoesNotExtend")


class Scry(object):
    """
    This is used to store information about the future, if we know it. Unlike
    predict, this tries to only get things we _know_ will happen.
    """

    _next = None # type: Node|None
    interacts = None # type: bool|None

    say = False # type: bool|None
    menu_with_caption = False # type: bool|None
    who = None # type: str|None

    # Text that will be added to the current say statment by a call to
    # extend.
    extend_text = None # type: str|None|renpy.object.Sentinel

    # By default, all attributes are None.
    def __getattr__(self, name):
        return None

    def next(self): # @ReservedAssignment
        if self._next is None:
            return None
        else:
            try:
                return self._next.scry()
            except Exception:
                return None


class Node(object):
    """
    A node in the abstract syntax tree of the program.

    @ivar name: The name of this node.
    @ivar filename: The filename where this node comes from.
    @ivar linenumber: The line number of the line on which this node is defined.
    @ivar next: The statement that will execute after this one.
    @ivar statement_start: If present, the first node that makes up the statement that includes this node.
    """

    __slots__ = [
        'name',
        'filename',
        'linenumber',
        'next',
        'statement_start',
        ]

    # True if this node is translatable, false otherwise. (This can be set on
    # the class or the instance.)
    translatable = False

    # True if the node is releveant to translation, and has to be processed by
    # take_translations.
    translation_relevant = False

    # How does the node participate in rollback?
    #
    # * "normal" in normal mode.
    # * "never" generally never.
    # * "force" force it to start.
    rollback = "normal"

    def __init__(self, loc):
        """
        Initializes this Node object.

        @param loc: A (filename, physical line number) tuple giving the
        logical line on which this Node node starts.
        """

        self.filename, self.linenumber = loc
        self.name = None
        self.next = None

    def diff_info(self):
        """
        Returns a tuple of diff info about ourself. This is used to
        compare Nodes to see if they should be considered the same node. The
        tuple returned must be hashable.
        """

        return (id(self),)

    def get_children(self, f):
        """
        Calls `f` with this node and its children.
        """

        f(self)

    # def get_init(self):
    #     """
    #     Returns a node that should be run at init time (that is, before
    #     the normal start of the script.), or None if this node doesn't
    #     care to suggest one.

    #     (The only class that needs to override this is Init.)
    #     """

    #     return None

    # get_init is only present on statements that define it.
    get_init = None

    def chain(self, next): # @ReservedAssignment
        """
        This is called with the Node node that should be followed after
        executing this node, and all nodes that this node
        executes. (For example, if this node is a block label, the
        next is the node that should be executed after all nodes in
        the block.)
        """

        self.next = next

    def replace_next(self, old, new):
        """
        Replaces instances of the `old` node with `new` when it is the next
        node.
        """

        if self.next is old:
            self.next = new

    def execute(self):
        """
        Causes this node to execute, and any action it entails to be
        performed. The node should call next_node with the node to
        be executed after this one.
        """

        raise Exception("Node subclass forgot to define execute.")

    # def early_execute(self):
    #     """
    #     Called when the module is loaded.
    #     """

    # early_execute is only present on statements that define it.
    early_execute = None

    def predict(self):
        """
        This is called to predictively load images from this node. It
        should cause renpy.display.predict.displayable and
        renpy.display.predict.screen to be called as necessary.
        """

        if self.next:
            return [ self.next ]
        else:
            return [ ]

    def scry(self):
        """
        Called to return an object with some general, user-definable information
        about the future.
        """

        rv = Scry()
        rv._next = self.next # type: ignore
        return rv

    def restructure(self, callback):
        """
        Called to restructure the AST.

        When this method is called, callback is called once for each child
        block of the node. The block, a list, can be updated by the callback
        using slice assignment to the list.
        """

        # Does nothing for nodes that do not contain child blocks.
        return

    def get_code(self, dialogue_filter=None):
        """
        Returns the canonical form of the code corresponding to this statement.
        This only needs to be defined if the statement is translatable.

        `filter`
            If present, a filter that should be applied to human-readable
            text in the statement.
        """

        raise Exception("Not Implemented")

    def analyze(self):
        """
        Called on all code after the init phase, to analyze it.
        """

        # Does nothing by default.
        return

    warp = False

    def can_warp(self):
        """
        Returns true if this should be run while warping, False otherwise.
        """

        return self.warp


def say_menu_with(expression, callback):
    """
    This handles the with clause of a say or menu statement.
    """

    if expression is not None:
        what = renpy.python.py_eval(expression)
    elif renpy.store.default_transition and renpy.game.preferences.transitions == 2: # type: ignore
        what = renpy.store.default_transition # type: ignore
    else:
        return

    if not what:
        return

    if renpy.game.preferences.transitions: # type: ignore
        callback(what)


def eval_who(who, fast=None):
    """
    Evaluates the `who` parameter to a say statement.
    """

    if who is None:
        return None

    if 'store.character' in renpy.python.store_dicts:
        rv = renpy.python.store_dicts['store.character'].get(who, None)
    else:
        rv = None

    if rv is None:
        rv = renpy.python.store_dicts['store'].get(who, None)

    if rv is not None:
        return rv

    try:
        return renpy.python.py_eval(who)
    except Exception:
        raise Exception("Sayer '%s' is not defined." % who)


class Say(Node):

    __slots__ = [
        'who',
        'who_fast',
        'what',
        'with_',
        'interact',
        'attributes',
        'arguments',
        'temporary_attributes',
        'rollback',
        'identifier',
        ]

    def diff_info(self):
        return (Say, self.who, self.what)

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.attributes = None
        self.interact = True
        self.arguments = None
        self.temporary_attributes = None
        self.rollback = "normal"
        return self

    def __init__(self, loc, who, what, with_, interact=True, attributes=None, arguments=None, temporary_attributes=None, identifier=None):

        super(Say, self).__init__(loc)

        if who is not None:
            self.who = who.strip()

            # True if who is a simple enough expression we can just look it up.
            if re.match(renpy.lexer.word_regexp + "$", self.who):
                self.who_fast = True
            else:
                self.who_fast = False
        else:
            self.who = None
            self.who_fast = False

        self.what = what
        self.with_ = with_
        self.interact = interact
        self.arguments = arguments

        # A tuple of attributes that are applied to the character that's
        # speaking, or None to disable this behavior.
        self.attributes = attributes

        # Ditto for temporary attributes.
        self.temporary_attributes = temporary_attributes

        # If given, write in the identifier.
        if identifier is not None:
            self.identifier = identifier

    def get_code(self, dialogue_filter=None):
        rv = [ ]

        if self.who:
            rv.append(self.who)

        if self.attributes is not None:
            rv.extend(self.attributes)

        if self.temporary_attributes:
            rv.append("@")
            rv.extend(self.temporary_attributes)

        what = self.what
        if dialogue_filter is not None:
            what = dialogue_filter(what)

        rv.append(renpy.translation.encode_say_string(what)) # @UndefinedVariable

        if not self.interact:
            rv.append("nointeract")

        if getattr(self, "identifier", None):
            rv.append("id")
            rv.append(getattr(self, "identifier", None))

        if self.arguments:
            rv.append(self.arguments.get_code())

        # This has to be at the end.
        if self.with_:
            rv.append("with")
            rv.append(self.with_)

        return " ".join(rv)

    def execute(self):

        next_node(self.next)

        try:

            renpy.game.context().say_attributes = self.attributes
            renpy.game.context().temporary_attributes = self.temporary_attributes

            who = eval_who(self.who, self.who_fast)

            if who is not None:
                stmt_name = getattr(who, "statement_name", "say")

                if callable(stmt_name):
                    stmt_name = stmt_name()

                statement_name(stmt_name)
            else:
                statement_name("say")

            if not (
                    (who is None) or
                    callable(who) or
                    isinstance(who, basestring)):

                raise Exception("Sayer %s is not a function or string." % self.who.encode("utf-8"))

            what = self.what
            if renpy.config.say_menu_text_filter:
                what = renpy.config.say_menu_text_filter(what) # E1102

            renpy.store._last_raw_what = what # type: ignore

            if self.arguments is not None:
                args, kwargs = self.arguments.evaluate()
            else:
                args = ()
                kwargs = {}

            kwargs.setdefault("interact", self.interact)

            if getattr(who, "record_say", True):
                renpy.store._last_say_who = self.who
                renpy.store._last_say_what = what
                renpy.store._last_say_args = args
                renpy.store._last_say_kwargs = kwargs

            say_menu_with(self.with_, renpy.game.interface.set_transition)
            renpy.exports.say(who, what, *args, **kwargs)

        finally:
            renpy.game.context().say_attributes = None
            renpy.game.context().temporary_attributes = None
            renpy.store._last_raw_what = "" # type: ignore

    def predict(self):

        old_attributes = renpy.game.context().say_attributes
        old_temporary_attributes = renpy.game.context().temporary_attributes

        try:

            renpy.game.context().say_attributes = self.attributes
            renpy.game.context().temporary_attributes = self.temporary_attributes

            who = eval_who(self.who, self.who_fast)

            def predict_with(trans):
                renpy.display.predict.displayable(trans(old_widget=None, new_widget=None))

            say_menu_with(self.with_, predict_with)

            what = self.what
            if renpy.config.say_menu_text_filter:
                what = renpy.config.say_menu_text_filter(what)

            renpy.exports.predict_say(who, what)

        finally:
            renpy.game.context().say_attributes = old_attributes
            renpy.game.context().temporary_attributes = old_temporary_attributes

        return [ self.next ]

    def scry(self):
        rv = Node.scry(self)

        who = eval_who(self.who, self.who_fast)
        rv.who = who
        rv.say = True

        if self.interact:
            renpy.exports.scry_say(who, self.what, rv)
        else:
            rv.interacts = False # type: ignore
            rv.extend_text = DoesNotExtend

        return rv


# Copy the descriptor.
setattr(Say, "with", Say.with_) # type: ignore


class Init(Node):

    __slots__ = [
        'block',
        'priority',
        ]

    def __init__(self, loc, block, priority):
        super(Init, self).__init__(loc)

        self.block = block
        self.priority = priority

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    def get_init(self):
        return self.priority, self.block[0]

    # We handle chaining specially. We want to chain together the nodes in
    # the block, but we want that chain to end in None, and we also want
    # this node to just continue on to the next node in normal execution.
    def chain(self, next): # @ReservedAssignment
        self.next = next

        chain_block(self.block, None)

    def execute(self):
        next_node(self.next)
        renpy.execution.not_infinite_loop(60)
        statement_name("init")

    def restructure(self, callback):
        callback(self.block)


class Label(Node):

    rollback = "force"

    translation_relevant = True
    __slots__ = [
        'parameters',
        'block',
        'hide',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.parameters = None
        self.hide = False
        return self

    def __init__(self, loc, name, block, parameters, hide=False):
        """
        Constructs a new Label node.

        @param name: The name of this label.
        @param block: A (potentially empty) list of nodes making up the
        block associated with this label.
        """

        super(Label, self).__init__(loc)

        self.name = name
        self.block = block
        self.parameters = parameters
        self.hide = hide

    def diff_info(self):
        return (Label, self.name)

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    def chain(self, next): # @ReservedAssignment

        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            self.next = next

    def execute(self):
        next_node(self.next)
        statement_name("label")

        renpy.game.context().mark_seen()

        values = apply_arguments(self.parameters, renpy.store._args, renpy.store._kwargs)

        renpy.exports.dynamic(**values)

        renpy.store._args = None
        renpy.store._kwargs = None

        renpy.easy.run_callbacks(renpy.config.label_callback, self.name, renpy.game.context().last_abnormal)
        renpy.easy.run_callbacks(renpy.config.label_callbacks, self.name, renpy.game.context().last_abnormal)

    def restructure(self, callback):
        callback(self.block)


class Python(Node):

    __slots__ = [
        'hide',
        'code',
        'store',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = "store"
        return self

    def __init__(self, loc, python_code, hide=False, store="store"):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """

        super(Python, self).__init__(loc)

        self.hide = hide

        if hide:
            self.code = PyCode(python_code, loc=loc, mode='hide')
        else:
            self.code = PyCode(python_code, loc=loc, mode='exec')

        self.store = store

    def diff_info(self):
        return (Python, self.code.source)

    def early_execute(self):
        renpy.python.create_store(self.store)

    def execute(self):
        next_node(self.next)
        statement_name("python")

        try:
            renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)
        finally:

            if not renpy.game.context().init_phase:
                for i in renpy.config.python_callbacks:
                    i()

    def scry(self):
        rv = Node.scry(self)
        rv.interacts = True
        return rv


class EarlyPython(Node):

    __slots__ = [
        'hide',
        'code',
        'store',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = "store"
        return self

    def __init__(self, loc, python_code, hide=False, store="store"):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """

        super(EarlyPython, self).__init__(loc)

        self.hide = hide

        if hide:
            self.code = PyCode(python_code, loc=loc, mode='hide')
        else:
            self.code = PyCode(python_code, loc=loc, mode='exec')

        self.store = store

    def diff_info(self):
        return (EarlyPython, self.code.source)

    def execute(self):
        next_node(self.next)
        renpy.execution.not_infinite_loop(60)
        statement_name("python early")

    def early_execute(self):
        renpy.python.create_store(self.store)

        if self.code.bytecode:
            renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)


class Image(Node):

    __slots__ = [
        'imgname',
        'code',
        'atl',
        ]

    def __init__(self, loc, name, expr=None, atl=None):
        """
        @param name: The name of the image being defined.

        @param expr: An expression yielding a Displayable that is
        assigned to the image.
        """

        super(Image, self).__init__(loc)

        self.imgname = name

        if expr:
            self.code = PyCode(expr, loc=loc, mode='eval')
            self.atl = None
        else:
            self.code = None
            self.atl = atl

    def diff_info(self):
        return (Image, tuple(self.imgname))

    def execute(self):

        # Note: We should always check that self.code is None before
        # accessing self.atl, as self.atl may not always exist.

        next_node(self.next)
        statement_name("image")

        if self.code is not None:
            img = renpy.python.py_eval_bytecode(self.code.bytecode)
        else:
            img = renpy.display.motion.ATLTransform(self.atl)

        renpy.exports.image(self.imgname, img)

    def analyze(self):
        if getattr(self, 'atl', None) is not None:
            # ATL images must participate with the game defined
            # constant names. So, we pass empty parameters to enable it.
            self.atl.analyze(EMPTY_PARAMETERS)


class Transform(Node):

    __slots__ = [
        # The name of the store this transform is stored in.
        'store',

        # The name of the transform.
        'varname',

        # The block of ATL associated with the transform.
        'atl',

        # The parameters associated with the transform, if any.
        'parameters',
        ]

    default_parameters = EMPTY_PARAMETERS

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = 'store'
        return self

    def __init__(self, loc, store, name, atl=None, parameters=default_parameters):

        super(Transform, self).__init__(loc)

        self.store = store
        self.varname = name
        self.atl = atl
        self.parameters = parameters

    def diff_info(self):
        return (Transform, self.store, self.varname)

    def early_execute(self):
        create_store(self.store)

    def execute(self):

        next_node(self.next)
        statement_name("transform")

        parameters = getattr(self, "parameters", None)

        if parameters is None:
            parameters = Transform.default_parameters

        trans = renpy.display.motion.ATLTransform(self.atl, parameters=parameters)
        renpy.dump.transforms.append((self.varname, self.filename, self.linenumber))
        renpy.exports.pure(self.varname)

        ns, _special = get_namespace(self.store)
        ns.set(self.varname, trans)

    def analyze(self):

        parameters = getattr(self, "parameters", None)

        if parameters is None:
            parameters = Transform.default_parameters

        self.atl.analyze(parameters)


def predict_imspec(imspec, scene=False, atl=None):
    """
    Call this to use the given callback to predict the image named
    in imspec.
    """

    if len(imspec) == 7:
        name, expression, tag, at_expr_list, layer, _zorder, _behind = imspec

    elif len(imspec) == 6:
        name, expression, tag, at_expr_list, layer, _zorder = imspec

    else:
        name, at_expr_list, layer = imspec
        tag = None
        expression = None

    if expression:
        try:
            img = renpy.python.py_eval(expression)
            img = renpy.easy.displayable(img)
        except Exception:
            return
    else:
        img = None

    at_list = [ ]
    for i in at_expr_list:
        try:
            at_list.append(renpy.python.py_eval(i))
        except Exception:
            pass

    if atl is not None:
        try:
            at_list.append(renpy.display.motion.ATLTransform(atl))
        except Exception:
            pass

    layer = renpy.exports.default_layer(layer, tag or name, bool(expression))

    if scene:
        renpy.game.context().images.predict_scene(layer)

    renpy.exports.predict_show(name, layer, what=img, tag=tag)


def show_imspec(imspec, atl=None):

    if len(imspec) == 7:
        name, expression, tag, at_list, layer, zorder, behind = imspec

    elif len(imspec) == 6:
        name, expression, tag, at_list, layer, zorder = imspec
        behind = [ ]

    else:
        name, at_list, layer = imspec
        expression = None
        tag = None
        zorder = None
        behind = [ ]

    if zorder is not None:
        zorder = renpy.python.py_eval(zorder)
    else:
        zorder = None

    if expression is not None:
        expression = renpy.python.py_eval(expression)
        expression = renpy.easy.displayable(expression)

    at_list = [ renpy.python.py_eval(i) for i in at_list ]

    layer = renpy.exports.default_layer(layer, tag or name, bool(expression) and (tag is None))

    renpy.config.show(name,
                      at_list=at_list,
                      layer=layer,
                      what=expression,
                      zorder=zorder,
                      tag=tag,
                      behind=behind,
                      atl=atl)


class Show(Node):

    __slots__ = [
        'imspec',
        'atl',
        ]

    warp = True

    def __init__(self, loc, imspec, atl=None):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer.
        """

        super(Show, self).__init__(loc)

        self.imspec = imspec
        self.atl = atl # type: Any

    def diff_info(self):
        return (Show, tuple(self.imspec[0]))

    def execute(self):
        next_node(self.next)
        statement_name("show")

        show_imspec(self.imspec, atl=getattr(self, "atl", None))

    def predict(self):
        predict_imspec(self.imspec, atl=getattr(self, "atl", None))
        return [ self.next ]

    def analyze(self):
        if getattr(self, 'atl', None) is not None:
            # ATL block defined for show, scene or show layer statements
            # must participate with the game defined constant names.
            # So, we pass empty parameters to enable it.
            self.atl.analyze(EMPTY_PARAMETERS)


class ShowLayer(Node):

    warp = True

    __slots__ = [
        'layer',
        'at_list',
        'atl',
        ]

    def __init__(self, loc, layer, at_list, atl):
        super(ShowLayer, self).__init__(loc)

        self.layer = layer
        self.at_list = at_list
        self.atl = atl

    def diff_info(self):
        return (ShowLayer, self.layer)

    def execute(self):
        next_node(self.next)
        statement_name("show layer")

        at_list = [ renpy.python.py_eval(i) for i in self.at_list ]

        if self.atl is not None:
            atl = renpy.display.motion.ATLTransform(self.atl)
            at_list.append(atl)

        renpy.exports.layer_at_list(at_list, layer=self.layer)

    def predict(self):
        return [ self.next ]

    def analyze(self):
        if self.atl is not None:
            self.atl.analyze(EMPTY_PARAMETERS)


class Camera(Node):

    warp = True

    __slots__ = [
        'layer',
        'at_list',
        'atl',
        ]

    def __init__(self, loc, layer, at_list, atl):
        super(Camera, self).__init__(loc)

        self.layer = layer
        self.at_list = at_list
        self.atl = atl

    def diff_info(self):
        return (ShowLayer, self.layer)

    def execute(self):
        next_node(self.next)
        statement_name("show layer")

        at_list = [ renpy.python.py_eval(i) for i in self.at_list ]

        if self.atl is not None:
            atl = renpy.display.motion.ATLTransform(self.atl)
            at_list.append(atl)

        renpy.exports.layer_at_list(at_list, layer=self.layer, camera=True)

    def predict(self):
        return [ self.next ]

    def analyze(self):
        if self.atl is not None:
            self.atl.analyze(EMPTY_PARAMETERS)


class Scene(Node):

    __slots__ = [
        'imspec',
        'layer',
        'atl',
        ]

    warp = True

    def __init__(self, loc, imgspec, layer, atl=None):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer, or
        None to not have this scene statement also display an image.
        """

        super(Scene, self).__init__(loc)

        self.imspec = imgspec
        self.layer = layer
        self.atl = atl # type: Any

    def diff_info(self):

        if self.imspec:
            data = tuple(self.imspec[0])
        else:
            data = None

        return (Scene, data)

    def execute(self):

        next_node(self.next)
        statement_name("scene")

        renpy.config.scene(self.layer)

        if self.imspec:
            show_imspec(self.imspec, atl=getattr(self, "atl", None))

    def predict(self):

        if self.imspec:
            predict_imspec(self.imspec, atl=getattr(self, "atl", None), scene=True)

        return [ self.next ]

    def analyze(self):
        if getattr(self, 'atl', None) is not None:
            self.atl.analyze(EMPTY_PARAMETERS)


class Hide(Node):

    __slots__ = [
        'imspec',
        ]

    warp = True

    def __init__(self, loc, imgspec):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a list of
        with expressions.
        """

        super(Hide, self).__init__(loc)

        self.imspec = imgspec

    def diff_info(self):
        return (Hide, tuple(self.imspec[0]))

    def predict(self):

        if len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec

        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
            _behind = None
        else:
            name, _at_list, layer = self.imspec
            tag = None
            _expression = None
            _zorder = None
            _behind = None

        if tag is None:
            tag = name[0]

        layer = renpy.exports.default_layer(layer, tag)

        renpy.game.context().images.predict_hide(layer, (tag,))

        return [ self.next ]

    def execute(self):

        next_node(self.next)
        statement_name("hide")

        if len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec
        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
        else:
            name, _at_list, layer = self.imspec
            _expression = None
            tag = None
            _zorder = 0

        layer = renpy.exports.default_layer(layer, tag or name)

        renpy.config.hide(tag or name, layer)


class With(Node):

    __slots__ = [
        'expr',
        'paired',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.paired = None
        return self

    def __init__(self, loc, expr, paired=None):
        """
        @param expr: An expression giving a transition or None.
        """

        super(With, self).__init__(loc)
        self.expr = expr
        self.paired = paired

    def diff_info(self):
        return (With, self.expr)

    def execute(self):

        next_node(self.next)
        statement_name("with")

        trans = renpy.python.py_eval(self.expr)

        if self.paired is not None:
            paired = renpy.python.py_eval(self.paired)
        else:
            paired = None

        renpy.exports.with_statement(trans, paired=paired)

    def predict(self):

        try:
            trans = renpy.python.py_eval(self.expr)

            if trans:
                renpy.display.predict.displayable(trans(old_widget=None, new_widget=None))

        except Exception:
            pass

        return [ self.next ]


class Call(Node):

    __slots__ = [
        'label',
        'arguments',
        'expression',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.arguments = None
        return self

    def __init__(self, loc, label, expression, arguments):

        super(Call, self).__init__(loc)
        self.label = label
        self.expression = expression
        self.arguments = arguments

    def diff_info(self):
        return (Call, self.label, self.expression)

    def execute(self):

        statement_name("call")

        label = self.label
        if self.expression:
            label = renpy.python.py_eval(label)

        rv = renpy.game.context().call(label, return_site=self.next.name)
        next_node(rv)
        renpy.game.context().abnormal = True

        if self.arguments:
            args, kwargs = self.arguments.evaluate()
            renpy.store._args = args
            renpy.store._kwargs = kwargs
        else:
            renpy.store._args = None
            renpy.store._kwargs = None

    def predict(self):

        label = self.label

        if self.expression:

            if not probably_side_effect_free(label):
                return [ ]

            try:
                label = renpy.python.py_eval(label)
            except Exception:
                return [ ]

            if not renpy.game.script.has_label(label):
                return [ ]

        return [ renpy.game.context().predict_call(label, self.next.name) ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv


class Return(Node):

    __slots__ = [ 'expression']

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.expression = None
        return self

    def __init__(self, loc, expression):
        super(Return, self).__init__(loc)
        self.expression = expression

    def diff_info(self):
        return (Return,)

    # We don't care what the next node is.
    def chain(self, next): # @ReservedAssignment
        self.next = None

    def execute(self):

        statement_name("return")

        if self.expression:
            renpy.store._return = renpy.python.py_eval(self.expression)
        else:
            renpy.store._return = None

        ctx = renpy.game.context()

        if renpy.game.context().init_phase:
            if len(ctx.return_stack) == 0:

                if renpy.config.developer:
                    raise Exception("Unexpected return during the init phase.")

                return

        next_node(renpy.game.context().lookup_return(pop=True))
        renpy.game.context().pop_dynamic()

    def predict(self):

        return [ renpy.game.context().predict_return() ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv


class Menu(Node):

    translation_relevant = True

    __slots__ = [
        'items',
        'set',
        'with_',
        'has_caption',
        'arguments',
        'item_arguments',
        'rollback',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.has_caption = False
        self.arguments = None
        self.item_arguments = None
        self.rollback = "force"
        return self

    def __init__(self, loc, items, set, with_, has_caption, arguments, item_arguments): # @ReservedAssignment
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with_ = with_
        self.has_caption = has_caption
        self.arguments = arguments
        self.item_arguments = item_arguments

    def diff_info(self):
        return (Menu,)

    def get_children(self, f):
        f(self)

        for _label, _condition, block in self.items:
            if block:
                for i in block:
                    i.get_children(f)

    # Blocks of statements in a choice continue after the menu.
    def chain(self, next): # @ReservedAssignment

        self.next = next

        for (_label, _condition, block) in self.items:
            if block:
                chain_block(block, next)

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        for _label, _condition, block in self.items:
            if block and (block[0] is old):
                block.insert(0, new)

    def execute(self):

        next_node(self.next)

        if self.has_caption or renpy.config.choice_empty_window:
            statement_name("menu-with-caption")
        else:
            statement_name("menu")

        if self.arguments is not None:
            args, kwargs = self.arguments.evaluate()
        else:
            args = kwargs = None

        choices = [ ]
        narration = [ ]
        item_arguments = [ ]

        for i, (label, condition, block) in enumerate(self.items):

            if renpy.config.say_menu_text_filter:
                label = renpy.config.say_menu_text_filter(label)

            has_item = False

            if block is None:
                if renpy.config.narrator_menu and label:
                    narration.append(label)
                else:
                    choices.append((label, condition, None))
                    has_item = True

            else:
                choices.append((label, condition, i))
                has_item = True

                next_node(block[0])

            if has_item:
                if self.item_arguments and (self.item_arguments[i] is not None):
                    item_arguments.append(self.item_arguments[i].evaluate())
                else:
                    item_arguments.append(((), {}))

        if narration:
            renpy.exports.say(None, "\n".join(narration), interact=False)

        say_menu_with(self.with_, renpy.game.interface.set_transition)

        choice = renpy.exports.menu(choices, self.set, args, kwargs, item_arguments)

        if choice is not None:
            next_node(self.items[choice][2][0])
        else:
            next_node(self.next)

    def predict(self):
        rv = [ ]

        def predict_with(trans):
            renpy.display.predict.displayable(trans(old_widget=None, new_widget=None))

        say_menu_with(self.with_, predict_with)

        renpy.store.predict_menu()

        for _label, _condition, block in self.items:
            if block:
                rv.append(block[0])

        return rv

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        rv.interacts = True
        if self.has_caption:
            rv.menu_with_caption = True
        return rv

    def restructure(self, callback):
        for _label, _condition, block in self.items:
            if block is not None:
                callback(block)


setattr(Menu, "with", Menu.with_) # type: ignore


# Goto is considered harmful. So we decided to name it "jump"
# instead.
class Jump(Node):

    __slots__ = [
        'target',
        'expression',
        ]

    def __init__(self, loc, target, expression):
        super(Jump, self).__init__(loc)

        self.target = target
        self.expression = expression

    def diff_info(self):
        return (Jump, self.target, self.expression)

    # We don't care what our next node is.
    def chain(self, next): # @ReservedAssignment
        self.next = None

    def execute(self):

        statement_name("jump")

        target = self.target
        if self.expression:
            target = renpy.python.py_eval(target)

        rv = renpy.game.script.lookup(target)
        renpy.game.context().abnormal = True

        next_node(rv)

    def predict(self):

        label = self.target

        if self.expression:

            if not probably_side_effect_free(label):
                return [ ]

            try:
                label = renpy.python.py_eval(label)
            except Exception:
                return [ ]

            if not renpy.game.script.has_label(label):
                return [ ]

        return [ renpy.game.script.lookup(label) ]

    def scry(self):
        rv = Node.scry(self)
        if self.expression:
            rv._next = None
        else:
            rv._next = renpy.game.script.lookup(self.target)

        return rv


# GNDN
class Pass(Node):

    __slots__ = [ ]

    def diff_info(self):
        return (Pass,)

    def execute(self):
        next_node(self.next)
        statement_name("pass")


class While(Node):

    __slots__ = [
        'condition',
        'block',
        ]

    def __init__(self, loc, condition, block):
        super(While, self).__init__(loc)

        self.condition = condition
        self.block = block

    def diff_info(self):
        return (While, self.condition)

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    def chain(self, next): # @ReservedAssignment
        self.next = next
        chain_block(self.block, self)

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        if self.block and (self.block[0] is old):
            self.block.insert(0, new)

    def execute(self):

        next_node(self.next)
        statement_name("while")

        if renpy.python.py_eval(self.condition):
            next_node(self.block[0])

    def predict(self):
        return [ self.block[0], self.next ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv

    def restructure(self, callback):
        callback(self.block)


class If(Node):

    __slots__ = [ 'entries' ]

    def __init__(self, loc, entries):
        """
        @param entries: A list of (condition, block) tuples.
        """

        super(If, self).__init__(loc)

        self.entries = entries

    def diff_info(self):
        return (If,)

    def get_children(self, f):
        f(self)

        for _condition, block in self.entries:
            for i in block:
                i.get_children(f)

    def chain(self, next): # @ReservedAssignment
        self.next = next

        for _condition, block in self.entries:
            chain_block(block, next)

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        for _condition, block in self.entries:
            if (block) and (block[0] is old):
                block.insert(0, new)

    def execute(self):

        next_node(self.next)
        statement_name("if")

        for condition, block in self.entries:
            if renpy.python.py_eval(condition):
                next_node(block[0])
                return

    def predict(self):

        return [ block[0] for _condition, block in self.entries ] + \
               [ self.next ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv

    def restructure(self, callback):
        for _condition, block in self.entries:
            callback(block)


class UserStatement(Node):

    __slots__ = [
        'line',
        'parsed',
        'block',
        'translatable',
        'code_block',
        'translation_relevant',
        'rollback',
        'subparses',
        'init_priority',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.block = [ ]
        self.code_block = None
        self.translatable = False
        self.translation_relevant = False
        self.rollback = "normal"
        self.subparses = [ ]
        self.init_priority = 0
        return self

    def __init__(self, loc, line, block, parsed):

        super(UserStatement, self).__init__(loc)
        self.code_block = None # type: Optional[list]
        self.parsed = parsed
        self.line = line
        self.block = block
        self.subparses = [ ]
        self.init_priority = 0

        self.name = self.call("label")
        self.rollback = renpy.statements.get("rollback", self.parsed) or "normal"

    def __repr__(self):
        return "<UserStatement {!r}>".format(self.line)

    def get_children(self, f):
        f(self)

        if self.code_block is not None:
            for i in self.code_block:
                i.get_children(f)

        for i in self.subparses:
            for j in i.block:
                j.get_children(f)

    def chain(self, next): # @ReservedAssignment
        self.next = next

        if self.code_block is not None:
            chain_block(self.code_block, next)

        for i in self.subparses:
            chain_block(i.block, next)

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        if (self.code_block) and (self.code_block[0] is old):
            self.code_block.insert(0, new)

        for i in self.subparses:
            if i.block[0] is old:
                i.block.insert(0, new)

    def restructure(self, callback):
        if self.code_block:
            callback(self.code_block)

        for i in self.subparses:
            callback(i.block)

    def diff_info(self):
        return (UserStatement, self.line)

    def call(self, method, *args, **kwargs):

        parsed = self.parsed

        if parsed is None:
            parsed = renpy.statements.parse(self, self.line, self.block)
            self.parsed = parsed

        return renpy.statements.call(method, parsed, *args, **kwargs)

    def execute_init(self):
        self.call("execute_init")

        if renpy.statements.get("init", self.parsed):
            self.init_priority = 1

        if renpy.statements.get("execute_default", self.parsed):
            default_statements.append(self)

    def get_init(self):
        return self.init_priority, self.execute_init

    def execute(self):
        next_node(self.get_next())
        statement_name(self.get_name())

        self.call("execute")

    def execute_default(self, start):
        self.call("execute_default")

    def predict(self):
        predictions = self.call("predict")

        if predictions is not None:
            for i in predictions:
                renpy.easy.predict(i)

        if self.parsed and renpy.statements.get("predict_all", self.parsed):
            return [ i.block[0] for i in self.subparses ] + [ self.next ]

        if self.next:
            next_label = self.next.name
        else:
            next_label = None

        next_list = self.call("predict_next", next_label)

        if next_list is not None:
            nexts = [ renpy.game.script.lookup_or_none(i) for i in next_list if i is not None ]
            return [ i for i in nexts if i is not None ]

        return [ self.next ]

    def get_name(self):
        parsed = self.parsed

        if parsed is None:
            parsed = renpy.statements.parse(self, self.line, self.block)
            self.parsed = parsed

        return renpy.statements.get_name(parsed)

    def get_next(self):

        if self.code_block and len(self.code_block):
            rv = self.call("next", self.code_block[0].name)
        else:
            rv = self.call("next")

        if rv is not None:
            return renpy.game.script.lookup(rv)
        else:
            return self.next

    def scry(self):
        rv = Node.scry(self)
        rv._next = self.get_next()
        self.call("scry", rv)
        return rv

    def get_code(self, dialogue_filter=None):
        return self.line

    def can_warp(self):

        if self.call("warp"):
            return True

        return False

    def reachable(self, is_reachable):
        """
        This is used by lint to find statements reachable from or through
        this statement.
        """

        rv = self.call(
            "reachable",
            is_reachable,
            self.name,
            self.next.name if self.next is not None else None,
            self.code_block[0].name if self.code_block else None,
            )

        if rv is None:

            rv = set()

            if self.call("label"):
                rv.add(self.name)
                is_reachable = True

            if is_reachable:

                if self.code_block:
                    rv.add(self.code_block[0].name)

                for i in self.subparses:
                    if i.block:
                        rv.add(i.block[0].name)

                if self.next:
                    rv.add(self.next.name)

        return rv

class PostUserStatement(Node):

    __slots__ = [
        'parent',
        ]

    def __init__(self, loc, parent):

        super(PostUserStatement, self).__init__(loc)
        self.parent = parent

        self.name = self.parent.call("post_label")

    def __repr__(self):
        return "<PostUserStatement {!r}>".format(self.parent.line)

    def diff_info(self):
        return (PostUserStatement, self.parent.line)

    def execute(self):
        next_node(self.next)
        statement_name("post " + self.parent.get_name())

        self.parent.call("post_execute")


def create_store(name):
    if name in renpy.config.special_namespaces:
        return

    # Take first two components of dot-joined name
    maybe_special = ".".join(name.split(".")[:2])
    if maybe_special in renpy.config.special_namespaces:
        if not renpy.config.special_namespaces[maybe_special].allow_child_namespaces:
            raise Exception('Creating stores within the {} namespace is not supported.'.format(maybe_special[6:]))

    renpy.python.create_store(name)


class StoreNamespace(object):
    pure = True

    def __init__(self, store):
        self.store = store

    def set(self, name, value):
        renpy.python.store_dicts[self.store][name] = value

    def set_default(self, name, value):
        renpy.python.store_dicts[self.store][name] = value

    def get(self, name):
        return renpy.python.store_dicts[self.store][name]


def get_namespace(store):
    """
    Returns the namespace object for `store`, and a flag that is true if the
    namespace is special, and false if it is a normal store.
    """

    if store in renpy.config.special_namespaces:
        return renpy.config.special_namespaces[store], True

    return StoreNamespace(store), False


# Config variables that are set twice - once when the rpy is first loaded,
# and then again at init time.
EARLY_CONFIG = {
    "save_directory",
    "allow_duplicate_labels",
    "keyword_after_python",
    "steam_appid",
    "name",
    "version",
    "save_token_keys",
    "check_conflicting_properties",
    "check_translate_none",
}

define_statements = [ ]


class Define(Node):

    __slots__ = [
        'varname',
        'code',
        'store',
        'operator',
        'index',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = 'store'
        self.operator = '='
        self.index = None
        return self

    def __init__(self, loc, store, name, index, operator, expr):
        super(Define, self).__init__(loc)

        self.store = store
        self.varname = name

        if index is not None:
            self.index = PyCode(index, loc=loc, mode='eval')
        else:
            self.index = None

        self.operator = operator
        self.code = PyCode(expr, loc=loc, mode='eval')

    def diff_info(self):
        return (Define, self.store, self.varname)

    def early_execute(self):
        create_store(self.store)

        if self.operator != "=":
            return

        if self.index is not None:
            return

        if self.store == "store.config" and self.varname in EARLY_CONFIG:
            value = renpy.python.py_eval_bytecode(self.code.bytecode)
            setattr(renpy.config, self.varname, value)

    def execute(self):

        next_node(self.next)
        statement_name("define")

        define_statements.append(self)

        if self.store == 'store':
            renpy.dump.definitions.append((self.varname, self.filename, self.linenumber))
        else:
            renpy.dump.definitions.append((self.store[6:] + "." + self.varname, self.filename, self.linenumber))

        if self.operator == "=" and self.index is None:
            ns, _special = get_namespace(self.store)
            if getattr(ns, "pure", True):
                renpy.exports.pure(self.store + "." + self.varname)

        self.set()

    def redefine(self, stores):

        if self.store not in stores:
            return

        self.set()

    def set(self):

        key = None
        new = None

        value = renpy.python.py_eval_bytecode(self.code.bytecode)
        ns, _special = get_namespace(self.store)

        if (self.index is None) and (self.operator == "="):
            ns.set(self.varname, value)
            return

        base = ns.get(self.varname)
        old = base

        if self.index:
            key = renpy.python.py_eval_bytecode(self.index.bytecode)

            if self.operator != "=":
                old = base[key]

        if self.operator == "=":
            new = value
        elif self.operator == "+=":
            new = old + value
        elif self.operator == "|=":
            new = old | value

        if self.index:
            base[key] = new
        else:
            ns.set(self.varname, new)


def redefine(stores):
    """
    Re-runs the given define statements.
    """

    for i in define_statements:
        i.redefine(stores)


# All the default statements, in the order they were registered.
default_statements = [ ]


class Default(Node):

    __slots__ = [
        'varname',
        'code',
        'store',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = 'store'
        return self

    def __init__(self, loc, store, name, expr):

        super(Default, self).__init__(loc)

        self.store = store
        self.varname = name
        self.code = PyCode(expr, loc=loc, mode='eval')

    def diff_info(self):
        return (Default, self.store, self.varname)

    def early_execute(self):
        create_store(self.store)

    def execute(self):

        next_node(self.next)
        statement_name("default")

        ns, special = get_namespace(self.store)

        if special:

            value = renpy.python.py_eval_bytecode(self.code.bytecode)
            ns.set_default(self.varname, value)
            return

        default_statements.append(self)

        if self.store == 'store':
            renpy.dump.definitions.append((self.varname, self.filename, self.linenumber))
        else:
            renpy.dump.definitions.append((self.store[6:] + "." + self.varname, self.filename, self.linenumber))

    def execute_default(self, start):
        d = renpy.python.store_dicts[self.store]

        defaults_set = d.get("_defaults_set", None)

        if defaults_set is None:
            d["_defaults_set"] = defaults_set = renpy.revertable.RevertableSet()
            d.ever_been_changed.add("_defaults_set")

        if self.varname in defaults_set:
            if start and renpy.config.developer:
                raise Exception("{}.{} is being given a default a second time.".format(self.store, self.varname))
            return

        # do the variable shadowing if not in this case, for compatibility reasons
        if start and (renpy.config.developer is True):
            fullname = '.'.join((self.store, self.varname))
            if fullname in renpy.python.store_dicts:
                raise Exception("{} is being given a default, but a store with that name already exists.".format(fullname))

        if start or (self.varname not in d.ever_been_changed):
            d[self.varname] = renpy.python.py_eval_bytecode(self.code.bytecode)

        d.ever_been_changed.add(self.varname)

        defaults_set.add(self.varname)

    def report_traceback(self, name, last):
        return [ (self.filename, self.linenumber, name, None) ]


class Screen(Node):

    __slots__ = [
        'screen',
        ]

    def __init__(self, loc, screen):
        """
        @param screen: The screen object being defined.
        In SL1, an instance of screenlang.ScreenLangScreen.
        In SL2, an instance of sl2.slast.SLScreen.
        """

        super(Screen, self).__init__(loc)

        self.screen = screen

    def diff_info(self):
        return (Screen, self.screen.name)

    def execute(self):
        next_node(self.next)
        statement_name("screen")

        self.screen.define((self.filename, self.linenumber))
        renpy.dump.screens.append((self.screen.name, self.filename, self.linenumber))

################################################################################
# Translations
################################################################################


class Translate(Node):
    """
    A translation block, produced either by explicit translation statements
    or implicit translation blocks.

    If language is None, when executed this transfers control to the translate
    statement in the current language, if any, and otherwise runs the block.
    If language is not None, causes an error to occur if control reaches this
    statement.

    When control normally leaves a translate statement, in any language, it
    goes to the end of the translate statement in the None language.
    """

    rollback = "never"

    translation_relevant = True

    __slots__ = [
        "identifier",
        "alternate",
        "language",
        "block",
        "after",
        ]

    def __init__(self, loc, identifier, language, block, alternate=None):
        super(Translate, self).__init__(loc)

        self.identifier = identifier
        self.alternate = alternate
        self.language = language
        self.block = block

    def diff_info(self):
        return (Translate, self.identifier, self.language)

    def chain(self, next): # @ReservedAssignment
        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            self.next = next

        self.after = next

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        if self.block and (self.block[0] is old):
            self.block.insert(0, new)

        if self.after is old:
            self.after = new

    def lookup(self):
        return renpy.game.script.translator.lookup_translate(self.identifier, getattr(self, "alternate", None))

    def execute(self):

        statement_name("translate")

        if self.language is not None:
            next_node(self.next)
            raise Exception("Translation nodes cannot be run directly.")

        if self.identifier not in renpy.game.persistent._seen_translates: # type: ignore
            renpy.game.persistent._seen_translates.add(self.identifier) # type: ignore
            renpy.game.seen_translates_count += 1
            renpy.game.new_translates_count += 1

        next_node(self.lookup())

        renpy.game.context().translate_identifier = self.identifier
        renpy.game.context().alternate_translate_identifier = getattr(self, "alternate", None)

    def predict(self):
        node = self.lookup()
        return [ node ]

    def scry(self):
        rv = Scry()
        rv._next = self.lookup()
        return rv

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    def restructure(self, callback):
        return callback(self.block)


class EndTranslate(Node):
    """
    A node added implicitly after each translate block. It's responsible for
    resetting the translation identifier.
    """

    rollback = "never"

    def diff_info(self):
        return (EndTranslate,)

    def execute(self):
        next_node(self.next)
        statement_name("end translate")

        renpy.game.context().translate_identifier = None
        renpy.game.context().alternate_translate_identifier = None


class TranslateString(Node):
    """
    A node used for translated strings.
    """

    translation_relevant = True

    __slots__ = [
        "language",
        "old",
        "new",
        "newloc",
        ]

    def __init__(self, loc, language, old, new, newloc):
        super(TranslateString, self).__init__(loc)
        self.language = language

        self.old = old
        self.new = new
        self.newloc = newloc

    def diff_info(self):
        return (TranslateString,)

    def execute(self):
        next_node(self.next)
        statement_name("translate string")

        newloc = getattr(self, "newloc", (self.filename, self.linenumber + 1))
        renpy.translation.add_string_translation(self.language, self.old, self.new, newloc)


class TranslatePython(Node):
    """
    Runs python code when changing the language.

    This is no longer generated, but is still run when encountered.
    """

    translation_relevant = True

    __slots__ = [
        'language',
        'code',
        ]

    def __init__(self, loc, language, python_code):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """

        super(TranslatePython, self).__init__(loc)

        self.language = language
        self.code = PyCode(python_code, loc=loc, mode='exec')

    def diff_info(self):
        return (TranslatePython, self.code.source)

    def execute(self):
        next_node(self.next)
        statement_name("translate_python")

    # def early_execute(self):
    #    renpy.python.create_store(self.store)
    #    renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)


class TranslateBlock(Node):
    """
    Runs a block of code when changing the language.
    """

    translation_relevant = True

    __slots__ = [
        'block',
        'language',
        ]

    def __init__(self, loc, language, block):
        super(TranslateBlock, self).__init__(loc)

        self.language = language
        self.block = block

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    # We handle chaining specially. We want to chain together the nodes in
    # the block, but we want that chain to end in None, and we also want
    # this node to just continue on to the next node in normal execution.
    def chain(self, next): # @ReservedAssignment
        self.next = next
        chain_block(self.block, None)

    def execute(self):
        next_node(self.next)
        statement_name("translate_block")

    def restructure(self, callback):
        callback(self.block)


class TranslateEarlyBlock(TranslateBlock):
    """
    This is similar to the TranslateBlock, except it runs before deferred
    styles do.
    """


class Style(Node):

    __slots__ = [
        'style_name',
        'parent',
        'properties',
        'clear',
        'take',
        'delattr',
        'variant',
    ]

    def __init__(self, loc, name):
        """
        `name`
            The name of the style to define.
        """

        super(Style, self).__init__(loc)

        self.style_name = name

        # The parent of this style.
        self.parent = None

        # Properties.
        self.properties = { }

        # Should we clear the style?
        self.clear = False

        # Should we take properties from another style?
        self.take = None

        # A list of attributes we should delete from this style.
        self.delattr = [ ]

        # If not none, an expression for the variant.
        self.variant = None

    def diff_info(self):
        return (Style, self.style_name)

    def apply(self):
        if self.variant is not None:
            variant = renpy.python.py_eval(self.variant)
            if not renpy.exports.variant(variant):
                return

        s = renpy.style.get_or_create_style(self.style_name)

        if self.clear:
            s.clear()

        if self.parent is not None:
            s.set_parent(self.parent)

        if self.take is not None:
            s.take(self.take)

        for i in self.delattr:
            s.delattr(i)

        if self.properties:
            properties = { }

            for name, expr in self.properties.items():

                value = renpy.python.py_eval(expr)

                if name == "properties":
                    properties.update(value)
                else:
                    properties[name] = value

            s.add_properties(properties)

    def execute(self):
        next_node(self.next)
        statement_name("style")

        if renpy.config.defer_styles and renpy.game.context().init_phase:
            renpy.translation.deferred_styles.append(self)
            return

        self.apply()


class Testcase(Node):

    __slots__ = [
        'label',
        'test',
        ]

    def __init__(self, loc, label, test):
        super(Testcase, self).__init__(loc)

        self.label = label
        self.test = test

    def diff_info(self):
        return (Testcase, self.label)

    def execute(self):
        next_node(self.next)
        statement_name("testcase")

        renpy.test.testexecution.testcases[self.label] = self.test


class RPY(Node):
    __slots__ = [
        "rest"
        ]

    def __init__(self, loc, rest):
        super(RPY, self).__init__(loc)

        self.rest = rest

    def diff_info(self):
        return (RPY, self.rest)

    def execute(self):
        next_node(self.next)
        statement_name("rpy")

        # rpy python 3 is run in Script.finish_load.

    def get_code(self):
        return "rpy " + " ".join(self.rest)
