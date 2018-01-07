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

# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

# NOTE:
# When updating this file, consider if lint.py or warp.py also need
# updating.

import renpy.display
import renpy.test

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

    def __init__(self, parameters, positional, extrapos, extrakw):

        # A list of parameter name, default value pairs.
        self.parameters = parameters

        # A list, giving the positional parameters to this function,
        # in order.
        self.positional = positional

        # A variable that takes the extra positional arguments, if
        # any. None if no such variable exists.
        self.extrapos = extrapos

        # A variable that takes the extra keyword arguments, if
        # any. None if no such variable exists.
        self.extrakw = extrakw

    def apply(self, args, kwargs, ignore_errors=False):
        """
        Applies `args` and `kwargs` to these parameters. Returns
        a dictionary that can be used to update an enclosing
        scope.

        `ignore_errors`
            If true, errors will be ignored, and this function will do the
            best job it can.
        """

        values = { }
        rv = { }

        if args is None:
            args = ()

        if kwargs is None:
            kwargs = { }

        for name, value in zip(self.positional, args):
            if name in values:
                if not ignore_errors:
                    raise Exception("Parameter %s has two values." % name)

            values[name] = value

        extrapos = tuple(args[len(self.positional):])

        for name, value in kwargs.iteritems():
            if name in values:
                if not ignore_errors:
                    raise Exception("Parameter %s has two values." % name)

            values[name] = value

        for name, default in self.parameters:

            if name not in values:
                if default is None:
                    if not ignore_errors:
                        raise Exception("Required parameter %s has no value." % name)
                else:
                    rv[name] = renpy.python.py_eval(default)

            else:
                rv[name] = values[name]
                del values[name]

        # Now, values has the left-over keyword arguments, and extrapos
        # has the left-over positional arguments.

        if self.extrapos:
            rv[self.extrapos] = extrapos
        elif extrapos and not ignore_errors:
            raise Exception("Too many arguments in call (expected %d, got %d)." % (len(self.positional), len(args)))

        if self.extrakw:
            rv[self.extrakw] = values
        elif values and not ignore_errors:
            raise Exception("Unknown keyword arguments: %s" % ( ", ".join(values.keys())))

        return rv


def apply_arguments(parameters, args, kwargs, ignore_errors=False):

    if parameters is None:
        if args or kwargs:
            raise Exception("Arguments supplied, but parameter list not present")
        else:
            return { }

    return parameters.apply(args, kwargs, ignore_errors)


class ArgumentInfo(object):

    def __init__(self, arguments, extrapos, extrakw):

        # A list of (keyword, expression) pairs. If an argument doesn't
        # have a keyword, it's thought of as positional.
        self.arguments = arguments

        # An expression giving extra positional arguments being
        # supplied to this function.
        self.extrapos = extrapos

        # An expression giving extra keyword arguments that need
        # to be supplied to this function.
        self.extrakw = extrakw

    def evaluate(self, scope=None):
        """
        Evaluates the arguments, returning a list of arguments and a
        dictionary of keyword arguments.
        """

        args = [ ]
        kwargs = renpy.python.RevertableDict()

        for k, v in self.arguments:
            if k is not None:
                kwargs[k] = renpy.python.py_eval(v, locals=scope)
            else:
                args.append(renpy.python.py_eval(v, locals=scope))

        if self.extrapos is not None:
            args.extend(renpy.python.py_eval(self.extrapos, locals=scope))

        if self.extrakw is not None:
            kwargs.update(renpy.python.py_eval(self.extrakw, locals=scope))

        return tuple(args), kwargs


def __newobj__(cls, *args):
    return cls.__new__(cls, *args)


# A list of pyexprs that need to be precompiled.
pyexpr_list = [ ]


class PyExpr(unicode):
    """
    Represents a string containing python code.
    """

    __slots__ = [
        'filename',
        'linenumber',
        ]

    def __new__(cls, s, filename, linenumber):
        self = unicode.__new__(cls, s)
        self.filename = filename
        self.linenumber = linenumber

        # Queue the string for precompilation.
        if self and (renpy.game.script.all_pyexpr is not None):
            renpy.game.script.all_pyexpr.append(self)

        return self

    def __getnewargs__(self):
        return (unicode(self), self.filename, self.linenumber)  # E1101


class PyCode(object):

    __slots__ = [
        'source',
        'location',
        'mode',
        'bytecode',
        'hash',
        ]

    def __getstate__(self):
        return (1, self.source, self.location, self.mode)

    def __setstate__(self, state):
        (_, self.source, self.location, self.mode) = state
        self.bytecode = None

        if renpy.game.script.record_pycode:
            renpy.game.script.all_pycode.append(self)

    def __init__(self, source, loc=('<none>', 1), mode='exec'):

        if isinstance(source, PyExpr):
            loc = (source.filename, source.linenumber, source)

        # The source code.
        self.source = source

        # The time is necessary so we can disambiguate between Python
        # blocks on the same line in different script versions.
        self.location = loc + ( int(time.time()), )
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
        except:
            pass

        code = self.source
        if isinstance(code, renpy.python.ast.AST):  # @UndefinedVariable
            code = renpy.python.ast.dump(code)  # @UndefinedVariable

        self.hash = chr(renpy.bytecode_version) + hashlib.md5(repr(self.location) + code.encode("utf-8")).digest()
        return self.hash


def chain_block(block, next):  # @ReservedAssignment
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


class Scry(object):
    """
    This is used to store information about the future, if we know it. Unlike
    predict, this tries to only get things we _know_ will happen.
    """

    # By default, all attributes are None.
    def __getattr__(self, name):
        return None

    def next(self):  # @ReservedAssignment
        if self._next is None:
            return None
        else:
            return self._next.scry()


class Node(object):
    """
    A node in the abstract syntax tree of the program.

    @ivar name: The name of this node.

    @ivar filename: The filename where this node comes from.
    @ivar linenumber: The line number of the line on which this node is defined.
    """

    __slots__ = [
        'name',
        'filename',
        'linenumber',
        'next',
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

        return ( id(self), )

    def get_children(self, f):
        """
        Calls `f` with this node and its children.
        """

        f(self)

    def get_init(self):
        """
        Returns a node that should be run at init time (that is, before
        the normal start of the script.), or None if this node doesn't
        care to suggest one.

        (The only class that needs to override this is Init.)
        """

        return None

    # get_init is only present on statements that define it.
    get_init = None

    def chain(self, next):  # @ReservedAssignment
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

    def early_execute(self):
        """
        Called when the module is loaded.
        """

    # early_execute is only present on statements that define it.
    early_execute = None

    def predict(self):
        """
        This is called to predictively load images from this node.  It
        should cause renpy.display.predict.image and
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
        rv._next = self.next  # W0201
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


def say_menu_with(expression, callback):
    """
    This handles the with clause of a say or menu statement.
    """

    if expression is not None:
        what = renpy.python.py_eval(expression)
    elif renpy.store.default_transition and renpy.game.preferences.transitions == 2:
        what = renpy.store.default_transition
    else:
        return

    if not what:
        return

    if renpy.game.preferences.transitions:
        # renpy.game.interface.set_transition(what)
        callback(what)


fast_who_pattern = re.compile(r'[a-zA-Z_][a-zA-Z_0-9]*$')


def eval_who(who, fast=None):
    """
    Evaluates the `who` parameter to a say statement.
    """

    if who is None:
        return None

    if fast is None:
        fast = bool(fast_who_pattern.match(who))

    if fast:

        if 'store.character' in renpy.python.store_dicts:
            rv = renpy.python.store_dicts['store.character'].get(who, None)
        else:
            rv = None

        if rv is None:
            rv = renpy.python.store_dicts['store'].get(who, None)

        if rv is None:
            raise Exception("Sayer '%s' is not defined." % who.encode("utf-8"))

        return rv

    return renpy.python.py_eval(who)


class Say(Node):

    __slots__ = [
        'who',
        'who_fast',
        'what',
        'with_',
        'interact',
        'attributes',
        'arguments',
        ]

    def diff_info(self):
        return (Say, self.who, self.what)

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.attributes = None
        self.interact = True
        self.arguments = None
        return self

    def __init__(self, loc, who, what, with_, interact=True, attributes=None, arguments=None):

        super(Say, self).__init__(loc)

        if who is not None:
            self.who = who.strip()

            # True if who is a simple enough expression we can just look it up.
            if re.match(renpy.parser.word_regexp + "$", self.who):
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

    def get_code(self, dialogue_filter=None):
        rv = [ ]

        if self.who:
            rv.append(self.who)

        if self.attributes is not None:
            rv.extend(self.attributes)

        what = self.what
        if dialogue_filter is not None:
            what = dialogue_filter(what)

        rv.append(renpy.translation.encode_say_string(what))

        if not self.interact:
            rv.append("nointeract")

        if self.with_:
            rv.append("with")
            rv.append(self.with_)

        return " ".join(rv)

    def execute(self):

        next_node(self.next)
        statement_name("say")

        try:

            renpy.game.context().say_attributes = self.attributes

            who = eval_who(self.who, self.who_fast)

            if not (
                    (who is None) or
                    callable(who) or
                    isinstance(who, basestring) ):

                raise Exception("Sayer %s is not a function or string." % self.who.encode("utf-8"))

            what = self.what
            if renpy.config.say_menu_text_filter:
                what = renpy.config.say_menu_text_filter(what)  # E1102

            renpy.store._last_raw_what = what

            if self.arguments is not None:
                args, kwargs = self.arguments.evaluate()
            else:
                args = tuple()
                kwargs = dict()

            if getattr(who, "record_say", True):
                renpy.store._last_say_who = self.who
                renpy.store._last_say_what = what
                renpy.store._last_say_args = args
                renpy.store._last_say_kwargs = kwargs

            say_menu_with(self.with_, renpy.game.interface.set_transition)
            renpy.exports.say(who, what, interact=self.interact, *args, **kwargs)

        finally:
            renpy.game.context().say_attributes = None

    def predict(self):

        old_attributes = renpy.game.context().say_attributes

        try:

            renpy.game.context().say_attributes = self.attributes

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

        return [ self.next ]

    def scry(self):
        rv = Node.scry(self)

        if self.who is not None:
            if self.who_fast:
                who = getattr(renpy.store, self.who)
            else:
                who = renpy.python.py_eval(self.who)
        else:
            who = None

        if self.interact:
            renpy.exports.scry_say(who, rv)
        else:
            rv.interacts = False

        return rv


# Copy the descriptor.
setattr(Say, "with", Say.with_)  # E1101


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
    def chain(self, next):  # @ReservedAssignment
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
        'name',
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

    def chain(self, next):  # @ReservedAssignment

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

        for k, v in values.iteritems():
            renpy.exports.dynamic(k)
            setattr(renpy.store, k, v)

        renpy.store._args = None
        renpy.store._kwargs = None

        if renpy.config.label_callback:
            renpy.config.label_callback(self.name, renpy.game.context().last_abnormal)

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
            self.atl.mark_constant()


class Transform(Node):

    __slots__ = [

        # The name of the transform.
        'varname',

        # The block of ATL associated with the transform.
        'atl',

        # The parameters associated with the transform, if any.
        'parameters',
        ]

    default_parameters = ParameterInfo([ ], [ ], None, None)

    def __init__(self, loc, name, atl=None, parameters=default_parameters):

        super(Transform, self).__init__(loc)

        self.varname = name
        self.atl = atl
        self.parameters = parameters

    def diff_info(self):
        return (Transform, self.varname)

    def execute(self):

        next_node(self.next)
        statement_name("transform")

        parameters = getattr(self, "parameters", None)

        if parameters is None:
            parameters = Transform.default_parameters

        trans = renpy.display.motion.ATLTransform(self.atl, parameters=parameters)
        renpy.dump.transforms.append((self.varname, self.filename, self.linenumber))
        renpy.exports.pure(self.varname)
        setattr(renpy.store, self.varname, trans)

    def analyze(self):
        self.atl.mark_constant()


def predict_imspec(imspec, scene=False, atl=None):
    """
    Call this to use the given callback to predict the image named
    in imspec.
    """

    if len(imspec) == 7:
        name, expression, tag, at_expr_list, layer, _zorder, _behind = imspec

    elif len(imspec) == 6:
        name, expression, tag, at_expr_list, layer, _zorder = imspec

    elif len(imspec) == 3:
        name, at_expr_list, layer = imspec
        tag = None
        expression = None

    if expression:
        try:
            img = renpy.python.py_eval(expression)
            img = renpy.easy.displayable(img)
        except:
            return
    else:
        img = None

    at_list = [ ]
    for i in at_expr_list:
        try:
            at_list.append(renpy.python.py_eval(i))
        except:
            pass

    if atl is not None:
        try:
            at_list.append(renpy.display.motion.ATLTransform(atl))
        except:
            pass

    layer = renpy.exports.default_layer(layer, tag or name, expression)

    if scene:
        renpy.game.context().images.predict_scene(layer)

    renpy.exports.predict_show(name, layer, what=img, tag=tag)


def show_imspec(imspec, atl=None):

    if len(imspec) == 7:
        name, expression, tag, at_list, layer, zorder, behind = imspec

    elif len(imspec) == 6:
        name, expression, tag, at_list, layer, zorder = imspec
        behind = [ ]

    elif len(imspec) == 3:
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

    layer = renpy.exports.default_layer(layer, tag or name, expression and (tag is None))

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

    def __init__(self, loc, imspec, atl=None):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer.
        """

        super(Show, self).__init__(loc)

        self.imspec = imspec
        self.atl = atl

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
            self.atl.mark_constant()


class ShowLayer(Node):

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
            self.atl.mark_constant()


class Scene(Node):

    __slots__ = [
        'imspec',
        'layer',
        'atl',
        ]

    def __init__(self, loc, imgspec, layer, atl=None):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer, or
        None to not have this scene statement also display an image.
        """

        super(Scene, self).__init__(loc)

        self.imspec = imgspec
        self.layer = layer
        self.atl = atl

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
            self.atl.mark_constant()


class Hide(Node):

    __slots__ = [
        'imspec',
        ]

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

        if len(self.imspec) == 3:
            name, _at_list, layer = self.imspec
            tag = None
            _expression = None
            _zorder = None
            _behind = None
        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
            _behind = None
        elif len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec

        if tag is None:
            tag = name[0]

        layer = renpy.exports.default_layer(layer, tag)

        renpy.game.context().images.predict_hide(tag, layer)

        return [ self.next ]

    def execute(self):

        next_node(self.next)
        statement_name("hide")

        if len(self.imspec) == 3:
            name, _at_list, layer = self.imspec
            _expression = None
            tag = None
            _zorder = 0
        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
        elif len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec

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

        renpy.exports.with_statement(trans, paired)

    def predict(self):

        try:
            trans = renpy.python.py_eval(self.expr)

            if trans:
                renpy.display.predict.displayable(trans(old_widget=None, new_widget=None))

        except:
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

    def predict(self):

        label = self.label

        if self.expression:
            label = renpy.python.py_eval(label)

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
        return (Return, )

    # We don't care what the next node is.
    def chain(self, next):  # @ReservedAssignment
        self.next = None
        return

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
        ]

    def __init__(self, loc, items, set, with_):  # @ReservedAssignment
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with_ = with_

    def diff_info(self):
        return (Menu,)

    def get_children(self, f):
        f(self)

        for _label, _condition, block in self.items:
            if block:
                for i in block:
                    i.get_children(f)

    # Blocks of statements in a choice continue after the menu.
    def chain(self, next):  # @ReservedAssignment

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
        statement_name("menu")

        choices = [ ]
        narration = [ ]

        for i, (label, condition, block) in enumerate(self.items):

            if renpy.config.say_menu_text_filter:
                label = renpy.config.say_menu_text_filter(label)

            if block is None:
                if renpy.config.narrator_menu and label:
                    narration.append(label)
                else:
                    choices.append((label, condition, None))
            else:
                choices.append((label, condition, i))
                next_node(block[0])

        if narration:
            renpy.exports.say(None, "\n".join(narration), interact=False)

        say_menu_with(self.with_, renpy.game.interface.set_transition)
        choice = renpy.exports.menu(choices, self.set)

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
        return rv

    def restructure(self, callback):
        for _label, _condition, block in self.items:
            if block is not None:
                callback(block)


setattr(Menu, "with", Menu.with_)  # E1101


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
    def chain(self, next):  # @ReservedAssignment
        self.next = None
        return

    def execute(self):

        statement_name("jump")

        target = self.target
        if self.expression:
            target = renpy.python.py_eval(target)

        rv = renpy.game.script.lookup(target)
        renpy.game.context().abnormal = True

        next_node(rv)

    def predict(self):

        if self.expression:
            return [ ]
        else:
            return [ renpy.game.script.lookup(self.target) ]

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

    def chain(self, next):  # @ReservedAssignment
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

    def chain(self, next):  # @ReservedAssignment
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
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.block = [ ]
        self.code_block = None
        self.translatable = False
        return self

    def __init__(self, loc, line, block):

        super(UserStatement, self).__init__(loc)
        self.line = line
        self.block = block
        self.code_block = None
        self.parsed = None

        self.name = self.call("label")

        # Do not store the parse.
        self.parsed = None

    def __repr__(self):
        return "<UserStatement {!r}>".format(self.line)

    def get_children(self, f):
        f(self)

        if not self.code_block:
            return

        for i in self.code_block:
            i.get_children(f)

    def chain(self, next):  # @ReservedAssignment
        self.next = next

        if self.code_block is not None:
            chain_block(self.code_block, next)

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        if (self.code_block) and (self.code_block[0] is old):
            self.code_block.insert(0, new)

    def restructure(self, callback):
        if self.code_block:
            callback(self.code_block)

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

    def get_init(self):
        return 0, self.execute_init

    def execute(self):
        next_node(self.get_next())
        statement_name(self.get_name())

        self.call("execute")

    def predict(self):
        predictions = self.call("predict")

        if predictions is not None:
            for i in predictions:
                renpy.easy.predict(i)

        return [ self.get_next() ]

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


def create_store(name):
    if name not in renpy.config.special_namespaces:
        renpy.python.create_store(name)


class StoreNamespace(object):

    def __init__(self, store):
        self.store = store

    def set(self, name, value):
        renpy.python.store_dicts[self.store][name] = value


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
EARLY_CONFIG = { "save_directory" }

define_statements = [ ]


class Define(Node):

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
        super(Define, self).__init__(loc)

        self.store = store
        self.varname = name
        self.code = PyCode(expr, loc=loc, mode='eval')

    def diff_info(self):
        return (Define, self.store, self.varname)

    def early_execute(self):
        create_store(self.store)

        if self.store == "store.config" and self.varname in EARLY_CONFIG:
            value = renpy.python.py_eval_bytecode(self.code.bytecode)
            setattr(renpy.config, self.varname, value)

    def execute(self):

        next_node(self.next)
        statement_name("define")

        define_statements.append(self)

        value = renpy.python.py_eval_bytecode(self.code.bytecode)

        if self.store == 'store':
            renpy.exports.pure(self.varname)
            renpy.dump.definitions.append((self.varname, self.filename, self.linenumber))
        else:
            renpy.dump.definitions.append((self.store[6:] + "." + self.varname, self.filename, self.linenumber))

        ns, _special = get_namespace(self.store)
        ns.set(self.varname, value)

    def redefine(self, stores):

        if self.store not in stores:
            return

        value = renpy.python.py_eval_bytecode(self.code.bytecode)
        ns, _special = get_namespace(self.store)
        ns.set(self.varname, value)


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

    def set_default(self, start):
        d = renpy.python.store_dicts[self.store]

        defaults_set = d.get("_defaults_set", None)

        if defaults_set is None:
            d["_defaults_set"] = defaults_set = renpy.python.RevertableSet()
            d.ever_been_changed.add("_defaults_set")

        if self.varname not in defaults_set:
            d[self.varname] = renpy.python.py_eval_bytecode(self.code.bytecode)
            d.ever_been_changed.add(self.varname)

            defaults_set.add(self.varname)

        else:

            if start and renpy.config.developer:
                raise Exception("{}.{} is being given a default a second time.".format(self.store, self.varname))

    def report_traceback(self, name, last):
        return [ (self.filename, self.linenumber, name, None) ]


class Screen(Node):

    __slots__ = [
        'screen',
        ]

    def __init__(self, loc, screen):
        """
        @param name: The name of the image being defined.

        @param expr: An expression yielding a Displayable that is
        assigned to the image.
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
        "language",
        "block",
        "after",
        ]

    def __init__(self, loc, identifier, language, block):
        super(Translate, self).__init__(loc)

        self.identifier = identifier
        self.language = language
        self.block = block

    def diff_info(self):
        return (Translate, self.identifier, self.language)

    def chain(self, next):  # @ReservedAssignment
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

    def execute(self):

        statement_name("translate")

        if self.language is not None:
            next_node(self.next)
            raise Exception("Translation nodes cannot be run directly.")

        if self.identifier not in renpy.game.persistent._seen_translates:  # @UndefinedVariable
            renpy.game.persistent._seen_translates.add(self.identifier)  # @UndefinedVariable
            renpy.game.seen_translates_count += 1
            renpy.game.new_translates_count += 1

        next_node(renpy.game.script.translator.lookup_translate(self.identifier))

        renpy.game.context().translate_identifier = self.identifier
        renpy.game.context().translate_block_language = self.language

    def predict(self):
        node = renpy.game.script.translator.lookup_translate(self.identifier)
        return [ node ]

    def scry(self):
        rv = Scry()
        rv._next = renpy.game.script.translator.lookup_translate(self.identifier)
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

    def __init__(self, loc):
        super(EndTranslate, self).__init__(loc)

    def diff_info(self):
        return (EndTranslate,)

    def execute(self):
        next_node(self.next)
        statement_name("end translate")

        renpy.game.context().translate_identifier = None
        renpy.game.context().translate_block_language = None


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
    def chain(self, next):  # @ReservedAssignment
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

        s = renpy.style.get_or_create_style(self.style_name)  # @UndefinedVariable

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
