
# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

import renpy

def chain_block(block, next):
    """
    This is called to chain together all of the nodes in a block. Node
    n is chained with node n+1, while the last node is chained with
    next.
    """

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
    
    # A map from filename to the largest serial number assigned to
    # a node from that file.
    serials = { }

    def __init__(self, loc):
        """
        Initializes this Node object.

        @param loc: A (filename, physical line number) tuple giving the
        logical line on which this Node node starts.
        """

        self.filename, self.linenumber, version = loc

        self.serials.setdefault(self.filename, 0)
        self.name = (self.filename, version, self.serials[self.filename])
        self.serials[self.filename] += 1

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

        assert False, "AST subclass forgot to define execute."

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


def say_menu_with(expression):
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
        renpy.game.interface.set_transition(what)
        
class Say(Node):

    def __init__(self, loc, who, what, with):

        super(Say, self).__init__(loc)
        
        self.who = who
        self.what = what
        self.with = with

    def execute(self):

        if self.who is not None:
            who = renpy.python.py_eval(self.who)
        else:
            who = None

        say_menu_with(self.with)
        renpy.exports.say(who, self.what)

        return self.next

class Init(Node):

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

    def __init__(self, loc, python_code, hide=False):
        """
        @param python_code: Properly-indented python code.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """
        
        super(Python, self).__init__(loc)

        self.hide = hide

        old_ei = renpy.game.exception_info

        renpy.game.exception_info = "While compiling python block starting at line %d of %s." % (self.linenumber, self.filename)
        self.bytecode = renpy.python.py_compile_exec_bytecode(python_code)
        renpy.game.exception_info = old_ei


    def execute(self):
        renpy.python.py_exec_bytecode(self.bytecode, self.hide)
        
        return self.next

class Image(Node):

    def __init__(self, loc, name, expr):
        """
        @param name: The name of the image being defined.

        @param expr: An expression yielding a Displayable that is
        assigned to the image.
        """

        super(Image, self).__init__(loc)
        
        self.name = name
        self.expr = expr

    def execute(self):
        import renpy.exports as exports

        if not renpy.game.init_phase:
            raise Exception("image statement should only be inside an init: block.")

        img = renpy.python.py_eval(self.expr)
        exports.images[self.name] = img

        return self.next

def imspec_common(imspec, hide=False):
    """
    This is code that's common to the three statements that can
    take imspecs (scene, show, and hide).

    It parses the imspec into a key, and an image, perhaps applying
    at clauses.

    @param hide: Reduces error checking, and changes the sticky position
    logic.
    """

    import renpy.display.image

    sls = renpy.game.context().scene_lists

    name, at_list = imspec
    key = name[0]

    # Handle sticky positions.
    if renpy.config.sticky_positions:
        if hide:
            if key in sls.sticky_positions:
                del sls.sticky_positions[key]
        else:
            if not at_list and key in sls.sticky_positions:
                at_list = sls.sticky_positions[key]

            sls.sticky_positions[key] = at_list

    # Get a reference to the base image.
    img = renpy.display.image.ImageReference(name)

    # Now, apply the at_list, from left to right.
    for i in at_list:
        img = renpy.python.py_eval(i)(img)

    # Update the set of images that have ever been seen.
    if not hide:
        renpy.game.persistent._seen_images[tuple(key)] = True

    return key, img

def predict_imspec(imspec, callback):
    """
    Call this to use the given callback to predict the image named
    in imspec.
    """

    if imspec[0] not in renpy.exports.images:
        return
    
    im = renpy.exports.images[imspec[0]]

    im.predict(callback)
            
        
class Show(Node):

    def __init__(self, loc, imspec):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a list of
        with expressions.
        """

        super(Show, self).__init__(loc)

        self.imspec = imspec

    def execute(self):

        key, img = imspec_common(self.imspec)
       
        sls = renpy.game.context().scene_lists
        sls.add('master', img, key)

        return self.next

    def predict(self, callback):
        predict_imspec(self.imspec, callback)
        return [ self.next ]
        

class Scene(Node):

    def __init__(self, loc, imgspec):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a list of
        with expressions, or None to not have this scene statement
        also display an image.
        """

        super(Scene, self).__init__(loc)

        self.imspec = imgspec

    def execute(self):

        import renpy.exports as exports

        sls = renpy.game.context().scene_lists
        
        sls.clear('master')
        sls.sticky_positions.clear()

        if self.imspec:
            key, img = imspec_common(self.imspec)
       
            sls.add('master', img, key)

        return self.next
        
    def predict(self, callback):

        if self.imspec:
            predict_imspec(self.imspec, callback)

        return [ self.next ]

class Hide(Node):

    def __init__(self, loc, imgspec):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a list of
        with expressions.
        """

        super(Hide, self).__init__(loc)

        self.imspec = imgspec

    def execute(self):

        import renpy.exports as exports

        sls = renpy.game.context().scene_lists
        
        key, img = imspec_common(self.imspec, hide=True)
       
        sls.remove('master', key)

        return self.next

class With(Node):
    def __init__(self, loc, expr):
        """
        @param expr: An expression giving a transition or None.
        """

        super(With, self).__init__(loc)
        self.expr = expr

    
    def execute(self):
        trans = renpy.python.py_eval(self.expr)

        renpy.exports.with(trans)

        return self.next
        
        
class Call(Node):

    def __init__(self, loc, label, expression):

        super(Call, self).__init__(loc)
        self.label = label
        self.expression = expression

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

    # No __init__ needed.

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

    def __init__(self, loc, items, set, with):
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with = with

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

        say_menu_with(self.with)
        choice = renpy.exports.menu(choices, self.set)

        if choice is None:
            return self.next
        else:
            return self.items[choice][2][0]
        

    def predict(self, callback):
        rv = [ ]

        for label, condition, block in self.items:
            if block:
                rv.append(block[0])

        return rv
                

# Goto is considered harmful. So we decided to name it "jump"
# instead. 
class Jump(Node):

    def  __init__(self, loc, target, expression):
        super(Jump, self).__init__(loc)

        self.target = target
        self.expression = expression

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

    def execute(self):
        return self.next

class While(Node):

    def __init__(self, loc, condition, block):
        super(While, self).__init__(loc)

        self.condition = condition
        self.block = block

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

    def __init__(self, loc, entries):
        """
        @param entries: A list of (condition, block) tuples.
        """

        super(If, self).__init__(loc)

        self.entries = entries

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
