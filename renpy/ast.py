# Copyright 2004-2006 PyTom <pytom@bishoujo.us>
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
        'with',
        'interact',
        ]

    def diff_info(self):
        return (Say, self.who, self.what)

    def __init__(self, loc, who, what, with, interact=True):

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
        self.with = with
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

        say_menu_with(self.with, renpy.game.interface.set_transition)
        renpy.exports.say(who, self.what, interact=getattr(self, 'interact', True))

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

        say_menu_with(self.with, predict_with)

        for i in renpy.exports.predict_say(who, self.what):
            if i is not None:
                i.predict(callback)

        return [ self.next ]
        

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
        'block',
        ]

    def __init__(self, loc, name, block):
        """
        Constructs a new Label node.

        @param name: The name of this label.
        @param block: A (potentially empty) list of nodes making up the
        block associated with this label.
        """

        super(Label, self).__init__(loc)

        self.name = name
        self.block = block

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

        old_ei = renpy.game.exception_info

        # renpy.game.exception_info = "While compiling python block starting at line %d of %s." % (self.linenumber, self.filename)
        # renpy.python.py_compile_exec_bytecode(python_code, filename=filename, lineno=lineno)
        self.code = PyCode(python_code, loc=loc, mode='exec')
        # renpy.game.exception_info = old_ei

    def get_pycode(self):
        return [ self.code ]

    def diff_info(self):
        return (Python, self.code.source)

    def execute(self):
        renpy.python.py_exec_bytecode(self.code.bytecode, self.hide)
        return self.next

class Image(Node):

    __slots__ = [
        'imgname',
        'code',
        ]

    def __init__(self, loc, name, expr):
        """
        @param name: The name of the image being defined.

        @param expr: An expression yielding a Displayable that is
        assigned to the image.
        """

        super(Image, self).__init__(loc)
        
        self.imgname = name
        self.code = PyCode(expr, loc=loc, mode='eval')

    def diff_info(self): 
        return (Image, tuple(self.imgname))

    def get_pycode(self):
        return [ self.code ]

    def execute(self):
        
        img = renpy.python.py_eval_bytecode(self.code.bytecode)
        renpy.exports.image(self.imgname, img)

        return self.next

def predict_imspec(imspec, callback):
    """
    Call this to use the given callback to predict the image named
    in imspec.
    """

    if len(imspec) == 3:
        name, at_list, layer = imspec
    else:
        name, expression, tag, at_list, layer, zorder = imspec

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

    img.predict(callback)
            
def show_imspec(imspec):

    if len(imspec) == 3:
        name, at_list, layer = imspec
        expression = None
        tag = None
        zorder = 0
    else:
        name, expression, tag, at_list, layer, zorder = imspec

        if zorder:
            zorder = renpy.python.py_eval(zorder)
        else:
            zorder = 0

        if expression:
            expression = renpy.python.py_eval(expression)
            expression = renpy.easy.displayable(expression)

    at_list = [ renpy.python.py_eval(i) for i in at_list ]

    renpy.exports.show(name, at_list=at_list, layer=layer,
                       what=expression, zorder=zorder, tag=tag)

class Show(Node):

    __slots__ = [
        'imspec',
        ]

    def __init__(self, loc, imspec):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer.
        """

        super(Show, self).__init__(loc)

        self.imspec = imspec

    def diff_info(self): 
        return (Show, tuple(self.imspec[0]))

    def execute(self):

        show_imspec(self.imspec)

        return self.next

    def predict(self, callback):
        predict_imspec(self.imspec, callback)
        return [ self.next ]
        

class Scene(Node):

    __slots__ = [
        'imspec',
        'layer',
        ]

    def __init__(self, loc, imgspec, layer):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer, or
        None to not have this scene statement also display an image.
        """

        super(Scene, self).__init__(loc)

        self.imspec = imgspec
        self.layer = layer

    def diff_info(self): 

        if self.imspec:
            data = tuple(self.imspec[0])
        else:
            data = None

        return (Scene, data)

    def execute(self):

        renpy.exports.scene(self.layer)

        if self.imspec:

            show_imspec(self.imspec)

        return self.next
        
    def predict(self, callback):

        if self.imspec:
            predict_imspec(self.imspec, callback)

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

    def execute(self):

        if len(self.imspec) == 3:
            name, at_list, layer = self.imspec
            expression = None
            tag = None
            zorder = 0
        else:
            name, expression, tag, at_list, layer, zorder = self.imspec

        renpy.exports.hide(tag or name, layer)

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

        renpy.exports.with(trans, paired)

        return self.next

    def predict(self, callback):

        trans = renpy.python.py_eval(self.expr)

        if trans:
            trans(old_widget=None, new_widget=None).predict(callback)
            
        return [ self.next ]
        
        
        
class Call(Node):

    __slots__ = [
        'label',
        'expression',
        ]

    def __init__(self, loc, label, expression):

        super(Call, self).__init__(loc)
        self.label = label
        self.expression = expression


    def diff_info(self):
        return (Call, self.label, self.expression)

    def execute(self):

        label = self.label
        if self.expression:
            label = renpy.python.py_eval(label)

        return renpy.game.context().call(label, return_site=self.next.name)

    def predict(self, callback):
        if self.expression:
            return [ ]
        else:
            return [ renpy.game.script.lookup(self.label) ]

class Return(Node):

    __slots__ = [ ]

    # No __init__ needed.

    def diff_info(self):
        return (Return, )

    # We don't care what the next node is.
    def chain(self, next):
        return

    def execute(self):
        return renpy.game.context().lookup_return(pop=True)

    def predict(self, callback):
        site = renpy.game.context().lookup_return(pop=False)
        if site:
            return [ site ]
        else:
            return [ ]

class Menu(Node):

    __slots__ = [
        'items',
        'set',
        'with',
        ]


    def __init__(self, loc, items, set, with):
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with = with

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
            if block is None:
                choices.append((label, condition, None))
            else:
                choices.append((label, condition, i))

        say_menu_with(self.with, renpy.game.interface.set_transition)
        choice = renpy.exports.menu(choices, self.set)

        if choice is None:
            return self.next
        else:
            return self.items[choice][2][0]
        

    def predict(self, callback):
        rv = [ ]

        def predict_with(trans):
            trans(old_widget=None, new_widget=None).predict(callback)

        say_menu_with(self.with, predict_with)

        for i in renpy.store.predict_menu():
            if i is not None:
                i.predict(callback)

        for label, condition, block in self.items:
            if block:
                rv.append(block[0])

        return rv
                

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
        return

    def execute(self):

        target = self.target
        if self.expression:
            target = renpy.python.py_eval(target)

        return renpy.game.script.lookup(target)

    def predict(self, callback):

        if self.expression:
            return [ ]
        else:
            return [ renpy.game.script.lookup(self.target) ]

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
