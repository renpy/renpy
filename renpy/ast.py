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

# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

# NOTE:
# When updating this file, consider if lint.py or warp.py also need
# updating.

import renpy.display

import re
import time
import md5

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


def __newobj__(cls, *args):
    return cls.__new__(cls, *args)

# This represents a string containing python code.
class PyExpr(unicode):

    __slots__ = [
        'filename',
        'linenumber',
        ]

    def __new__(cls, s, filename, linenumber):
        self = unicode.__new__(cls, s)
        self.filename = filename
        self.linenumber = linenumber
        return self

    def __getnewargs__(self):
        return (unicode(self), self.filename, self.linenumber) # E1101

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

        self.hash = None

    def get_hash(self):
        try:
            if self.hash is not None:
                return self.hash
        except:
            pass

        code = self.source
        if isinstance(code, renpy.python.ast.AST): #@UndefinedVariable
            code = renpy.python.ast.dump(code) #@UndefinedVariable

        self.hash = chr(renpy.bytecode_version) + md5.md5(repr(self.location) + code.encode("utf-8")).digest()
        return self.hash


def chain_block(block, next): #@ReservedAssignment
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

    def next(self): #@ReservedAssignment
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

    # Called to set the state of a Node, when necessary.
    def __setstate__(self, state):
        for k, v in state[1].iteritems():
            try:
                setattr(self, k, v)
            except AttributeError:
                pass


    def __init__(self, loc):
        """
        Initializes this Node object.

        @param loc: A (filename, physical line number) tuple giving the
        logical line on which this Node node starts.
        """

        self.filename, self.linenumber  = loc
        self.name = None
        self.next = None

    def diff_info(self):
        """
        Returns a tuple of diff info about ourself. This is used to
        compare Nodes to see if they should be considered the same node. The
        tuple returned must be hashable.
        """

        return ( id(self), )

    def get_children(self):
        """
        Returns a list of all of the nodes that are children of this
        node. (That is, all of the nodes in any block associated with
        this node.)
        """

        return [ ]

    def get_init(self):
        """
        Returns a node that should be run at init time (that is, before
        the normal start of the script.), or None if this node doesn't
        care to suggest one.

        (The only class that needs to override this is Init.)
        """

        return None

    def chain(self, next): #@ReservedAssignment
        """
        This is called with the Node node that should be followed after
        executing this node, and all nodes that this node
        executes. (For example, if this node is a block label, the
        next is the node that should be executed after all nodes in
        the block.)
        """

        self.next = next

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
        rv._next = self.next # W0201
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

class Say(Node):

    __slots__ = [
        'who',
        'who_fast',
        'what',
        'with_',
        'interact',
        'attributes',
        ]

    def diff_info(self):
        return (Say, self.who, self.what)

    def __setstate__(self, state):
        self.attributes = None
        self.interact = True
        Node.__setstate__(self, state)

    def __init__(self, loc, who, what, with_, interact=True, attributes=None):

        super(Say, self).__init__(loc)

        if who is not None:
            self.who = who.strip()

            if re.match(r'[a-zA-Z_]\w*$', self.who):
                self.who_fast = True
            else:
                self.who_fast = False
        else:
            self.who = None
            self.who_fast = False

        self.what = what
        self.with_ = with_
        self.interact = interact

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

        try:

            renpy.exports.say_attributes = self.attributes

            if self.who is not None:
                if self.who_fast:
                    who = getattr(renpy.store, self.who, None)
                    if who is None:
                        raise Exception("Sayer '%s' is not defined." % self.who.encode("utf-8"))
                else:
                    who = renpy.python.py_eval(self.who)
            else:
                who = None

            if not (
                (who is None) or
                callable(who) or
                isinstance(who, basestring) ):

                raise Exception("Sayer %s is not a function or string." % self.who.encode("utf-8"))

            what = self.what
            if renpy.config.say_menu_text_filter:
                what = renpy.config.say_menu_text_filter(what) # E1102

            renpy.store._last_raw_what = what

            if getattr(who, "record_say", True):
                renpy.store._last_say_who = self.who
                renpy.store._last_say_what = what

            say_menu_with(self.with_, renpy.game.interface.set_transition)
            renpy.exports.say(who, what, interact=self.interact)

        finally:
            renpy.exports.say_attributes = None


    def predict(self):

        old_attributes = renpy.exports.say_attributes

        try:

            renpy.exports.say_attributes = self.attributes

            if self.who is not None:
                if self.who_fast:
                    who = getattr(renpy.store, self.who)
                else:
                    who = renpy.python.py_eval(self.who)
            else:
                who = None

            def predict_with(trans):
                renpy.display.predict.displayable(trans(old_widget=None, new_widget=None))

            say_menu_with(self.with_, predict_with)

            what = self.what
            if renpy.config.say_menu_text_filter:
                what = renpy.config.say_menu_text_filter(what)

            renpy.exports.predict_say(who, what)

        finally:
            renpy.exports.say_attributes = old_attributes

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
setattr(Say, "with", Say.with_) # E1101

class Init(Node):

    __slots__ = [
        'block',
        'priority',
        ]

    def __init__(self, loc, block, priority):
        super(Init, self).__init__(loc)

        self.block = block
        self.priority = priority


    def get_children(self):
        return self.block

    def get_init(self):
        return self.priority, self.block[0]

    # We handle chaining specially. We want to chain together the nodes in
    # the block, but we want that chain to end in None, and we also want
    # this node to just continue on to the next node in normal execution.
    def chain(self, next): #@ReservedAssignment
        self.next = next

        chain_block(self.block, None)

    def execute(self):
        next_node(self.next)

    def restructure(self, callback):
        callback(self.block)

def apply_arguments(params, args, kwargs):
    """
    Applies arguments to parameters to update scope.

    `scope`
        A dict.

    `params`
        The parameters object.

    `args`, `kwargs`
        Positional and keyword arguments.
    """

    values = { }
    rv = { }

    if args is None:
        args = ()

    if kwargs is None:
        kwargs = { }

    if params is None:
        if args or kwargs:
            raise Exception("Arguments supplied, but parameter list not present")
        else:
            return rv

    for name, value in zip(params.positional, args):
        if name in values:
            raise Exception("Parameter %s has two values." % name)

        values[name] = value

    extrapos = tuple(args[len(params.positional):])

    for name, value in kwargs.iteritems():
        if name in values:
            raise Exception("Parameter %s has two values." % name)

        values[name] = value

    for name, default in params.parameters:

        if name not in values:
            if default is None:
                raise Exception("Required parameter %s has no value." % name)
            else:
                rv[name] = renpy.python.py_eval(default)

        else:
            rv[name] = values[name]
            del values[name]

    # Now, values has the left-over keyword arguments, and extrapos
    # has the left-over positional arguments.

    if params.extrapos:
        rv[params.extrapos] = extrapos
    elif extrapos:
        raise Exception("Too many arguments in call (expected %d, got %d)." % (len(params.positional), len(args)))

    if params.extrakw:
        rv[params.extrakw] = values
    else:
        if values:
            raise Exception("Unknown keyword arguments: %s" % ( ", ".join(values.keys())))

    return rv

class Label(Node):

    __slots__ = [
        'name',
        'parameters',
        'block',
        'hide',
        ]

    def __setstate__(self, state):
        self.parameters = None
        self.hide = False
        Node.__setstate__(self, state)

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

    def get_children(self):
        return self.block

    def chain(self, next): #@ReservedAssignment

        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            self.next = next

    def execute(self):
        next_node(self.next)

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

    def __setstate__(self, state):
        self.store = "store"
        super(Python, self).__setstate__(state)

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

    def __setstate__(self, state):
        self.store = "store"
        super(EarlyPython, self).__setstate__(state)

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

        if self.code is not None:
            img = renpy.python.py_eval_bytecode(self.code.bytecode)
        else:
            img = renpy.display.motion.ATLTransform(self.atl)

        renpy.exports.image(self.imgname, img)



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

        parameters = getattr(self, "parameters", None)

        if parameters is None:
            parameters = Transform.default_parameters

        trans = renpy.display.motion.ATLTransform(self.atl, parameters=parameters)
        renpy.dump.transforms.append((self.varname, self.filename, self.linenumber))
        setattr(renpy.store, self.varname, trans)


def predict_imspec(imspec, scene=False, atl=None):
    """
    Call this to use the given callback to predict the image named
    in imspec.
    """

    if len(imspec) == 7:
        name, expression, tag, _at_list, layer, _zorder, _behind = imspec

    elif len(imspec) == 6:
        name, expression, tag, _at_list, layer, _zorder = imspec

    elif len(imspec) == 3:
        name, _at_list, layer = imspec


    if expression:
        try:
            img = renpy.python.py_eval(expression)
            img = renpy.easy.displayable(img)
        except:
            return

    else:
        img = renpy.display.image.images.get(name, None)
        if img is None:
            return

    full_name = name
    if tag:
        full_name = (tag,) + full_name[1:]

    if scene:
        renpy.game.context().images.predict_scene(layer)

    renpy.game.context().images.predict_show(tag or name, layer)

    if atl is not None:
        try:
            img = renpy.display.motion.ATLTransform(atl, child=img)
        except:
            import traceback
            traceback.print_exc()

    renpy.display.predict.displayable(img)



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
        zorder = 0

    if expression is not None:
        expression = renpy.python.py_eval(expression)
        expression = renpy.easy.displayable(expression)

    at_list = [ renpy.python.py_eval(i) for i in at_list ]

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

        show_imspec(self.imspec, atl=getattr(self, "atl", None))

    def predict(self):
        predict_imspec(self.imspec, atl=getattr(self, "atl", None))
        return [ self.next ]


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

        renpy.config.scene(self.layer)

        if self.imspec:
            show_imspec(self.imspec, atl=getattr(self, "atl", None))

    def predict(self):

        if self.imspec:
            predict_imspec(self.imspec, atl=getattr(self, "atl", None), scene=True)

        return [ self.next ]


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

        renpy.game.context().images.predict_hide(tag, layer)

        return [ self.next ]

    def execute(self):

        next_node(self.next)

        if len(self.imspec) == 3:
            name, _at_list, layer = self.imspec
            _expression = None
            tag = None
            _zorder = 0
        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
        elif len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec

        renpy.config.hide(tag or name, layer)


class With(Node):

    __slots__ = [
        'expr',
        'paired',
        ]

    def __setstate__(self, state):
        self.paired = None
        Node.__setstate__(self, state)

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

    def __setstate__(self, state):
        self.arguments = None
        Node.__setstate__(self, state)

    def __init__(self, loc, label, expression, arguments):

        super(Call, self).__init__(loc)
        self.label = label
        self.expression = expression
        self.arguments = arguments

    def diff_info(self):
        return (Call, self.label, self.expression)

    def execute(self):

        label = self.label
        if self.expression:
            label = renpy.python.py_eval(label)

        rv = renpy.game.context().call(label, return_site=self.next.name)
        next_node(rv)
        renpy.game.context().abnormal = True

        if self.arguments:

            args = [ ]
            kwargs = renpy.python.RevertableDict()

            for name, expr in self.arguments.arguments:

                value = renpy.python.py_eval(expr)

                if name is None:
                    args.append(value)
                else:
                    if name in kwargs:
                        raise Exception("The argument named %s appears twice." % name)

                    kwargs[name] = value

            if self.arguments.extrapos:
                args.extend(renpy.python.py_eval(self.arguments.extrapos))

            if self.arguments.extrakw:
                for name, value in renpy.python.py_eval(self.arguments.extrakw).iteritems():
                    if name in kwargs:
                        raise Exception("The argument named %s appears twice." % name)

                    kwargs[name] = value


            renpy.store._args = tuple(args)
            renpy.store._kwargs = kwargs

    def predict(self):
        if self.expression:
            return [ ]
        else:
            return [ renpy.game.script.lookup(self.label) ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv


class Return(Node):

    __slots__ = [ 'expression']

    def __setstate__(self, state):
        self.expression = None
        Node.__setstate__(self, state)

    def __init__(self, loc, expression):
        super(Return, self).__init__(loc)
        self.expression = expression

    def diff_info(self):
        return (Return, )

    # We don't care what the next node is.
    def chain(self, next): #@ReservedAssignment
        self.next = None
        return

    def execute(self):

        if self.expression:
            renpy.store._return = renpy.python.py_eval(self.expression)
        else:
            renpy.store._return = None

        renpy.game.context().pop_dynamic()

        next_node(renpy.game.context().lookup_return(pop=True))

    def predict(self):
        site = renpy.game.context().lookup_return(pop=False)
        if site:
            return [ site ]
        else:
            return [ ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv


class Menu(Node):

    __slots__ = [
        'items',
        'set',
        'with_',
        ]

    def __init__(self, loc, items, set, with_): #@ReservedAssignment
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with_ = with_

    def diff_info(self):
        return (Menu,)

    def get_children(self):
        rv = [ ]

        for _label, _condition, block in self.items:
            if block:
                rv.extend(block)

        return rv

    # Blocks of statements in a choice continue after the menu.
    def chain(self, next): #@ReservedAssignment

        self.next = next

        for (_label, _condition, block) in self.items:
            if block:
                chain_block(block, next)

    def execute(self):

        next_node(self.next)

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

setattr(Menu, "with", Menu.with_) # E1101


# Goto is considered harmful. So we decided to name it "jump"
# instead.
class Jump(Node):

    __slots__ = [
        'target',
        'expression',
        ]

    def  __init__(self, loc, target, expression):
        super(Jump, self).__init__(loc)

        self.target = target
        self.expression = expression

    def diff_info(self):
        return (Jump, self.target, self.expression)

    # We don't care what our next node is.
    def chain(self, next): #@ReservedAssignment
        self.next = None
        return

    def execute(self):

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

    def get_children(self):
        return self.block

    def chain(self, next): #@ReservedAssignment
        self.next = next
        chain_block(self.block, self)

    def execute(self):

        next_node(self.next)

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

    def get_children(self):
        rv = [ ]

        for _condition, block in self.entries:
            rv.extend(block)

        return rv

    def chain(self, next): #@ReservedAssignment
        self.next = next

        for _condition, block in self.entries:
            chain_block(block, next)

    def execute(self):

        next_node(self.next)

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
        'translatable' ]

    def __setstate__(self, state):
        self.block = [ ]
        self.translatable = False
        Node.__setstate__(self, state)

    def __init__(self, loc, line, block):

        super(UserStatement, self).__init__(loc)
        self.line = line
        self.block = block
        self.parsed = None

        # Do not store the parse quite yet.
        _parse_info = renpy.statements.parse(self, self.line, self.block)

    def diff_info(self):
        return (UserStatement, self.line)

    def execute(self):
        next_node(self.get_next())

        self.call("execute")

    def predict(self):
        self.call("predict")
        return [ self.get_next() ]

    def call(self, method, *args, **kwargs):

        parsed = self.parsed
        if parsed is None:
            parsed = renpy.statements.parse(self, self.line, self.block)
            self.parsed = parsed

        renpy.statements.call(method, parsed, *args, **kwargs)

    def get_next(self):
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


class Define(Node):

    __slots__ = [
        'varname',
        'code',
        ]

    def __init__(self, loc, name, expr):
        """
        @param name: The name of the image being defined.

        @param expr: An expression yielding a Displayable that is
        assigned to the image.
        """

        super(Define, self).__init__(loc)

        self.varname = name
        self.code = PyCode(expr, loc=loc, mode='eval')

    def diff_info(self):
        return (Define, tuple(self.varname))

    def execute(self):

        next_node(self.next)

        value = renpy.python.py_eval_bytecode(self.code.bytecode)
        renpy.dump.definitions.append((self.varname, self.filename, self.linenumber))
        setattr(renpy.store, self.varname, value)


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
        self.screen.define()
        renpy.dump.screens.append((self.screen.name, self.filename, self.linenumber))


################################################################################
# Translations
################################################################################

class Translate(Node):
    """
    A translation block, produced either by explicit translation statements
    or implicit translation blocs.

    If language is None, when executed this transfers control to the translate
    statement in the current language, if any, and otherwise runs the block.
    If language is not None, causes an error to occur if control reaches this
    statement.

    When control normally leaves a translate statement, in any language, it
    goes to the end of the translate statement in the None language.
    """

    __slots__ = [
        "identifier",
        "language",
        "block",
        ]

    def __init__(self, loc, identifier, language, block):
        super(Translate, self).__init__(loc)

        self.identifier = identifier
        self.language = language
        self.block = block

    def diff_info(self):
        return (Translate, self.identifier, self.language)

    def chain(self, next): #@ReservedAssignment
        self.next = next
        chain_block(self.block, next)

    def execute(self):

        if self.language is not None:
            next_node(self.next)
            raise Exception("Translation nodes cannot be run directly.")

        next_node(renpy.game.script.translator.lookup_translate(self.identifier))
        renpy.game.context().translate_identifier = self.identifier

    def predict(self):
        node = renpy.game.script.translator.lookup_translate(self.identifier)
        return [ node ]

    def scry(self):
        rv = Scry()
        rv._next = renpy.game.script.translator.lookup_translate(self.identifier)
        return rv

    def get_children(self):
        return self.block

    def restructure(self, callback):
        return callback(self.block)


class EndTranslate(Node):
    """
    A node added implicitly after each translate block. It's responsible for
    resetting the translation identifier.
    """

    def __init__(self, loc):
        super(EndTranslate, self).__init__(loc)

    def diff_info(self):
        return (EndTranslate,)

    def execute(self):
        next_node(self.next)
        renpy.game.context().translate_identifier = None


class TranslateString(Node):
    """
    A node used for translated strings.
    """

    __slots__ = [
        "language",
        "old",
        "new"
        ]

    def __init__(self, loc, language, old, new):
        super(TranslateString, self).__init__(loc)
        self.language = language
        self.old = old
        self.new = new

    def diff_info(self):
        return (TranslateString,)

    def execute(self):
        next_node(self.next)
        renpy.translation.add_string_translation(self.language, self.old, self.new)

class TranslatePython(Node):

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

    # def early_execute(self):
    #    renpy.python.create_store(self.store)
    #    renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)
