# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

import renpy.python as python
import renpy.game

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


class Say(Node):

    def __init__(self, loc, who, what):

        super(Say, self).__init__(loc)
        
        self.who = who
        self.what = what

    def execute(self):

        import renpy.exports as exports

        if self.who is not None:
            who = python.py_eval(self.who)
        else:
            who = None

        exports.say(who, self.what % renpy.game.store)

        return self.next

class Init(Node):

    def __init__(self, loc, block):
        super(Init, self).__init__(loc)

        self.block = block


    def get_children(self):
        return self.block

    def get_init(self):
        return self.block[0]

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

        self.python_code = python_code
        self.hide = hide
        

    def execute(self):
        python.py_exec(self.python_code, self.hide)

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

        img = python.py_eval(self.expr)
        exports.images[self.name] = img

        return self.next

def imspec_common(imspec, hide=False):
    """
    This is code that's common to the three statements that can
    take imspecs (scene, show, and hide).

    It parses the imspec into a key, an image, and a with_image, and
    returns all three to the user.

    @param hide: Reduces error checking, and makes the with_image None
    if the list of with expressions is empty.
    """

    import renpy.display.image
        
    name, at_list, with_list = imspec
    key = name[0]

    # Get a reference to the base image.
    img = renpy.display.image.ImageReference(name)

    # Now, apply the at_list, from left to right.
    for i in at_list:
        img = python.py_eval(i)(img)

    # Now, apply the with list to get the with_image.
    with_img = img

    for i in with_list:
        with_img = python.py_eval(i)(with_img)

    if hide and not with_list:
        with_img = None

    return key, img, with_img
            
        
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

        key, img, with_img = imspec_common(self.imspec)
       
        sls = renpy.game.context().scene_lists
        sls.add('master', img, key)
        sls.add('transient', with_img, key)

        return self.next

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
        sls.clear('transient')

        if self.imspec:
            key, img, with_img = imspec_common(self.imspec)
       
            sls.add('master', img, key)
            sls.add('transient', with_img, key)

        return self.next
        

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
        
        key, img, with_img = imspec_common(self.imspec, hide=True)
       
        sls.remove('master', key)

        if with_img:
            sls.add('transient', with_img, key)
        else:
            sls.remove('transient', key)
            
        return self.next
        
class Call(Node):

    def __init__(self, loc, label):

        super(Call, self).__init__(loc)
        self.label = label

    def execute(self):
        return renpy.game.context().call(self.label, return_site=self.next.name)

class Return(Node):

    # No __init__ needed.

    def execute(self):
        return renpy.game.context().lookup_return()

class Menu(Node):

    def __init__(self, loc, items, set):
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set

    # Blocks of statements in a choice continue after the menu.
    def chain(self, next):

        self.next = next

        for (label, condition, block) in self.items:
            if block:
                chain_block(block, next)

    def execute(self):

        import renpy.exports as exports

        choices = [ ]
            
        for i, (label, condition, block) in enumerate(self.items):
            if block is None:
                choices.append((label, condition, None))
            else:
                choices.append((label, condition, i))

        choice = exports.menu(choices, self.set)

        if choice is None:
            return self.next
        else:
            return self.items[choice][2][0]
        

# Goto is considered harmful. So we decided to name it "jump"
# instead. 
class Jump(Node):

    def  __init__(self, loc, target):
        super(Jump, self).__init__(loc)

        self.target = target

    def execute(self):
        return renpy.game.script.lookup(self.target)

# GNDN
class Pass(Node):

    def execute(self):
        return self.next

class While(Node):

    def __init__(self, loc, condition, block):
        super(While, self).__init__(loc)

        self.condition = condition
        self.block = block

    def chain(self, next):
        self.next = next
        chain_block(self.block, self)

    def execute(self):

        if python.py_eval(self.condition):
            return self.block[0]
        else:
            return self.next

class If(Node):

    def __init__(self, loc, entries):
        """
        @param entries: A list of (condition, block) tuples.
        """


        super(If, self).__init__(loc)

        self.entries = entries

    def chain(self, next):
        self.next = next

        for condition, block in self.entries:
            chain_block(block, next)


    def execute(self):

        for condition, block in self.entries:
            if python.py_eval(condition):
                return block[0]

        return self.next
        

        
        
