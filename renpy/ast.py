# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import renpy
import re
import time

# Called to set the state of a Node, when necessary.
def setstate(node, state):
    for k, v in state[1].iteritems():
        setattr(node, k, v)

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
        'linenumber'
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
        ]

    # All PyCodes known to the system.
    extent = [ ]

    def __getstate__(self):
        return (1, self.source, self.location, self.mode)

    def __setstate__(self, state):
        (_, self.source, self.location, self.mode) = state
        self.bytecode = None
        
    def __init__(self, source, loc=('<none>', 1), mode='exec'):
        # The source code.
        self.source = source

        # The time is necessary so we can disambiguate between Python
        # blocks on the same line in different script versions.
        self.location = loc + ( int(time.time()), )
        self.mode = mode

        # This will be initialized later on, after we are serialized.
        self.bytecode = None

def chain_block(block, next):
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

    def next(self):
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
        
    def chain(self, next):
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
        performed. The node is then responsible for returning the node
        that should be executed after this one, or None to end the
        program or init block.
        """

        assert False, "Node subclass forgot to define execute."

    def predict(self, callback):
        """
        This is called to predictively load images from this node. The
        callback needs to be passed into the predict method of any
        images this ast node will probably load, and the method should
        return a list containing the nodes that this node will
        probably execute next.
        """

        if self.next:
            return [ self.next ]
        else:
            return [ ]

    def get_pycode(self):
        """
        Returns a list of PyCode objects associated with this Node,
        or None if no objects are associated with it.
        """

        return [ ]

    def scry(self):
        """
        Called to return an object with some general, user-definable information
        about the future.
        """

        rv = Scry()
        rv._next = self.next # W0201
        return rv

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
        ]

    def diff_info(self):
        return (Say, self.who, self.what)

    def __init__(self, loc, who, what, with_, interact=True):

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

    def execute(self):

        if self.who is not None:
            if self.who_fast:
                who = getattr(renpy.store, self.who, None)
                if who is None:
                    raise Exception("Sayer '%s' is not defined." % self.who.encode("utf-8"))
            else:
                who = renpy.python.py_eval(self.who)
        else:
            who = None

        what = self.what
        if renpy.config.say_menu_text_filter:
            what = renpy.config.say_menu_text_filter(what) # E1102
            
        say_menu_with(self.with_, renpy.game.interface.set_transition)
        renpy.exports.say(who, what, interact=getattr(self, 'interact', True))

        if getattr(who, "record_say", True):
            renpy.store._last_say_who = self.who
            renpy.store._last_say_what = what

        return self.next

    def predict(self, callback):

        if self.who is not None:
            if self.who_fast:
                who = getattr(renpy.store, self.who)
            else:
                who = renpy.python.py_eval(self.who)
        else:
            who = None

        def predict_with(trans):
            trans(old_widget=None, new_widget=None).predict(callback)

        say_menu_with(self.with_, predict_with)

        what = self.what
        if renpy.config.say_menu_text_filter:
            what = renpy.config.say_menu_text_filter(what)

        for i in renpy.exports.predict_say(who, what):
            if i is not None:
                i.predict(callback)

        return [ self.next ]

    def scry(self):
        rv = Node.scry(self)
        rv.interacts = True # W0201
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
    def chain(self, next):
        self.next = next

        chain_block(self.block, None)

    def execute(self):
        return self.next
    

class Label(Node):

    __slots__ = [
        'name',
        'parameters',
        'block',
        ]

    def __setstate__(self, state):
        self.parameters = None
        setstate(self, state)
    
    def __init__(self, loc, name, block, parameters):
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

    def diff_info(self):
        return (Label, self.name)

    def get_children(self):
        return self.block 

    def chain(self, next):

        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            self.next = next
            
    def execute(self):
        renpy.game.context().mark_seen()
        
        args = renpy.store._args
        kwargs = renpy.store._kwargs

        if self.parameters is None:
            if (args is not None) or (kwargs is not None):
                raise Exception("Arguments supplied, but label does not take parameters.")
            else:
                if renpy.config.label_callback:
                    renpy.config.label_callback(self.name, renpy.game.context().last_abnormal)

                return self.next
        else:
            if args is None:
                args = ()

            if kwargs is None:
                kwargs = { }
            
        values = { }        
        params = self.parameters

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
                    values[name] = renpy.python.py_eval(default)

                    
            renpy.exports.dynamic(name)
            setattr(renpy.store, name, values[name])
            del values[name]

        # Now, values has the left-over keyword arguments, and extrapos
        # has the left-over positional arguments.

        if params.extrapos:
            renpy.exports.dynamic(params.extrapos)
            setattr(renpy.store, params.extrapos, extrapos)
        else:
            if extrapos:
                raise Exception("Too many arguments in call (expected %d, got %d)." % (len(params.positional), len(args)))

        if params.extrakw:
            renpy.exports.dynamic(params.extrakw)
            setattr(renpy.store, params.extrakw, renpy.python.RevertableDict(values))
        else:
            if values:
                raise Exception("Unknown keyword arguments: %s" % ( ", ".join(values.keys())))

        renpy.store._args = None
        renpy.store._kwargs = None

        if renpy.config.label_callback:
            renpy.config.label_callback(self.name, renpy.game.context().last_abnormal)
        
        return self.next

class Python(Node):

    __slots__ = [
        'hide',
        'code',
        ]

    def __init__(self, loc, python_code, hide=False):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """
        
        super(Python, self).__init__(loc)

        self.hide = hide
        self.code = PyCode(python_code, loc=loc, mode='exec')

    def get_pycode(self):
        return [ self.code ]

    def diff_info(self):
        return (Python, self.code.source)

    def execute(self):
        renpy.python.py_exec_bytecode(self.code.bytecode, self.hide)
        return self.next

    def scry(self):
        rv = Node.scry(self)
        rv.interacts = True
        return rv

class EarlyPython(Node):

    __slots__ = [
        'hide',
        'code',
        ]

    def __init__(self, loc, python_code, hide=False):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """
        
        super(EarlyPython, self).__init__(loc)

        self.hide = hide
        self.code = PyCode(python_code, loc=loc, mode='exec')

    def get_pycode(self):
        return [ self.code ]

    def diff_info(self):
        return (EarlyPython, self.code.source)

    def execute(self):
        return self.next

    def early_execute(self):
        renpy.python.py_exec_bytecode(self.code.bytecode, self.hide)

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

    def get_pycode(self):
        if self.code:            
            return [ self.code ]
        else:
            return [ ]
        
    def execute(self):

        # Note: We should always check that self.code is None before
        # accessing self.atl, as self.atl may not always exist.

        if self.code is not None:
            img = renpy.python.py_eval_bytecode(self.code.bytecode)
        else:
            img = renpy.display.motion.ATLTransform(self.atl)

        renpy.exports.image(self.imgname, img)

        return self.next


    
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

        parameters = getattr(self, "parameters", None)

        if parameters is None:
            parameters = Transform.default_parameters

        trans = renpy.display.motion.ATLTransform(self.atl, parameters=parameters)
        renpy.exports.definitions[self.varname].append((self.filename, self.linenumber, "transform"))
        setattr(renpy.store, self.varname, trans)
                
        return self.next

    
def predict_imspec(imspec, callback, scene=False):
    """
    Call this to use the given callback to predict the image named
    in imspec.
    """

    if len(imspec) == 7:
        name, expression, tag, at_list, layer, zorder, behind = imspec

    elif len(imspec) == 6:
        name, expression, tag, at_list, layer, zorder = imspec

    elif len(imspec) == 3:
        name, at_list, layer = imspec
        
        
    if expression:
        try:
            img = renpy.python.py_eval(expression)
            img = renpy.easy.displayable(img)
        except:
            return

    else:
        img = renpy.exports.images.get(name, None)
        if img is None:
            return

    full_name = name
    if tag:
        full_name = (tag,) + full_name[1:]

    if scene:
        renpy.game.context().predict_info.images.predict_scene(layer)
        
    renpy.game.context().predict_info.images.predict_show(tag or name, layer)
        
    img.predict(callback)

    
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

        show_imspec(self.imspec, atl=getattr(self, "atl", None))

        return self.next

    def predict(self, callback):
        predict_imspec(self.imspec, callback)
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

        renpy.config.scene(self.layer)

        if self.imspec:
            show_imspec(self.imspec, atl=getattr(self, "atl", None))

        return self.next
        
    def predict(self, callback):
        
        if self.imspec:
            predict_imspec(self.imspec, callback, scene=True)

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

    def predict(self, callback):

        if len(self.imspec) == 3:
            name, at_list, layer = self.imspec
            expression = None
            tag = None
            zorder = 0
        elif len(self.imspec) == 6:
            name, expression, tag, at_list, layer, zorder = self.imspec
        elif len(self.imspec) == 7:
            name, expression, tag, at_list, layer, zorder, behind = self.imspec


        if tag is None:
            tag = name[0]
            
        renpy.game.context().predict_info.images.predict_hide(tag, layer)

        return [ ]
        
    def execute(self):

        if len(self.imspec) == 3:
            name, at_list, layer = self.imspec
            expression = None
            tag = None
            zorder = 0
        elif len(self.imspec) == 6:
            name, expression, tag, at_list, layer, zorder = self.imspec
        elif len(self.imspec) == 7:
            name, expression, tag, at_list, layer, zorder, behind = self.imspec
            
        renpy.config.hide(tag or name, layer)

        return self.next

    
class With(Node):

    __slots__ = [
        'expr',
        'paired',
        ]

    def __setstate__(self, state):
        self.paired = None
        setstate(self, state)
    
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

        trans = renpy.python.py_eval(self.expr)

        if self.paired is not None:
            paired = renpy.python.py_eval(self.paired)
        else:
            paired = None 

        renpy.exports.with_statement(trans, paired)

        return self.next

    def predict(self, callback):

        try:
            trans = renpy.python.py_eval(self.expr)

            if trans:
                trans(old_widget=None, new_widget=None).predict(callback)
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
        setstate(self, state)
    
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
                    
        
        return rv
        
        
    def predict(self, callback):
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
        setstate(self, state)
    
    def __init__(self, loc, expression):
        super(Return, self).__init__(loc)
        self.expression = expression
        
    def diff_info(self):
        return (Return, )

    # We don't care what the next node is.
    def chain(self, next):
        self.next = None
        return

    def execute(self):

        if self.expression:
            renpy.store._return = renpy.python.py_eval(self.expression)
        else:
            renpy.store._return = None

        renpy.game.context().pop_dynamic()
            
        return renpy.game.context().lookup_return(pop=True)

    def predict(self, callback):
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

    def __init__(self, loc, items, set, with_):
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with_ = with_

    def diff_info(self):
        return (Menu,)

    def get_children(self):
        rv = [ ]

        for label, condition, block in self.items:
            if block:
                rv.extend(block)

        return rv

    # Blocks of statements in a choice continue after the menu.
    def chain(self, next):

        self.next = next

        for (label, condition, block) in self.items:
            if block:
                chain_block(block, next)

    def execute(self):

        choices = [ ]
            
        for i, (label, condition, block) in enumerate(self.items):

            if renpy.config.say_menu_text_filter:
                label = renpy.config.say_menu_text_filter(label)

            if block is None:
                choices.append((label, condition, None))
            else:
                choices.append((label, condition, i))

        say_menu_with(self.with_, renpy.game.interface.set_transition)
        choice = renpy.exports.menu(choices, self.set)

        if choice is None:
            return self.next
        else:
            return self.items[choice][2][0]
        

    def predict(self, callback):
        rv = [ ]

        def predict_with(trans):
            trans(old_widget=None, new_widget=None).predict(callback)

        say_menu_with(self.with_, predict_with)

        for i in renpy.store.predict_menu():
            if i is not None:
                i.predict(callback)

        for label, condition, block in self.items:
            if block:
                rv.append(block[0])

        return rv

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        rv.interacts = True
        return rv
    
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
    def chain(self, next):
        self.next = None
        return

    def execute(self):

        target = self.target
        if self.expression:
            target = renpy.python.py_eval(target)

        rv = renpy.game.script.lookup(target)
        renpy.game.context().abnormal = True
        return rv

    def predict(self, callback):

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
        return self.next


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

    def chain(self, next):
        self.next = next
        chain_block(self.block, self)

    def execute(self):

        if renpy.python.py_eval(self.condition):
            return self.block[0]
        else:
            return self.next

    def predict(self, callback):
        return [ self.block[0], self.next ]
        
    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv

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

        for condition, block in self.entries:
            rv.extend(block)

        return rv

    def chain(self, next):
        self.next = next

        for condition, block in self.entries:
            chain_block(block, next)

    def execute(self):

        for condition, block in self.entries:
            if renpy.python.py_eval(condition):
                return block[0]

        return self.next

    def predict(self, callback):

        return [ block[0] for condition, block in self.entries ] + \
               [ self.next ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv


class UserStatement(Node):

    __slots__ = [ 'line', 'parsed' ]

    def __init__(self, loc, line):

        super(UserStatement, self).__init__(loc)
        self.line = line
        self.parsed = None

        # Do not store the parse quite yet.
        renpy.statements.parse(self, self.line)
        
    def diff_info(self):
        return (UserStatement, self.line)

    def execute(self):
        self.call("execute")
        return self.get_next()

    def predict(self, callback):
        predicted = self.call("predict") or [ ]

        for i in predicted:
            callback(i)
            
        return [ self.get_next() ]
    
    def call(self, method, *args, **kwargs):
        
        parsed = self.parsed        
        if parsed is None:
            parsed = renpy.statements.parse(self, self.line)
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

    def get_pycode(self):
        if self.code:            
            return [ self.code ]
        else:
            return [ ]
        
    def execute(self):

        value = renpy.python.py_eval_bytecode(self.code.bytecode)
        renpy.exports.definitions[self.varname].append((self.filename, self.linenumber, "define"))
        setattr(renpy.store, self.varname, value)    
        
        return self.next
