# Copyright 2004-2009 PyTom <pytom@bishoujo.us>
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

import renpy

# A map from the name of an interpolator, to a tuple containing the
# interpolator function, and the number of non-time arguments it takes.
interpolators = { }

def register_atl_interpolator(name, f, arity):
    interpolators[name] = (f, arity)

# An example interpolator. (This is used internally when no interpolator
# is otherwise specified.)
def pause(duration, start, end, t):
    if t < duration:
        return start
    else:
        return end

register_atl_interpolator("pause", pause, 1)
    
# A map from the name of a property to the function that sets that
# property on a Transform object.
properties_registry = { }

def register_atl_property(name, getter, setter):
    properties_registry[name] = (getter, setter)

    
# This is intended to be subclassed by ATLTransform. It takes care of
# managing ATL execution, which allows ATLTransform itself to not care
# much about the contents of this file.
class TransformBase(renpy.object.Object):

    def __init__(self, atl):

        # The raw code that makes up this ATL statement.
        self.atl = atl

        # The code after it has been compiled into a block.
        self.block = None

        # The properties of the block, if it contains only an
        # Interpolation.
        self.properties = None

        # The arity of the block, if it contains only an
        # Interpolation.
        self.arity = None

        # The state of the statement we are executing.
        self.state = None

        # Are we done?
        self.done = False
        
    # Compiles self.atl into self.block, and then update the rest of
    # the variables.
    def compile(self):
        self.block = self.atl.compile()

        if len(self.block.statements) == 1 \
                and isinstance(self.block.statements[0], Interpolation):

            interp = self.block.statements[0]

            if interp.duration == 0 and interp.properties:
            
                self.properties = interp.properties[:]
                self.arity = len(self.properties[0][1])

    def execute(self, st, event):
        if self.done:
            return

        if not self.block:
            self.compile()
        
        action, arg = self.block.execute(self, st, self.state, event)

        if action == "continue":
            self.state = arg
            return
        else:
            self.done = True


# The base class for raw ATL statements.
class RawStatement(renpy.object.Object):
    pass

# The base class for compiled ATL Statements.
class Statement(renpy.object.Object):


    # trans is the transform we're working on.
    # st is the time since this statement started executing.
    # state is the state stored by this statement, or None if
    # we've just started executing this statement.
    # event is an event we're triggering.
    #
    # "continue", state - Causes this statement to execute again,
    # with the given state passed in the second time around.
    #
    # "next", timeleft - Causes the next statement to execute, with
    # timeleft being the amount of time left after this statement
    # finished.
    #
    # "repeat", (count, timeleft) - Causes the repeat behavior to occur.
    #
    # As the Repeat statement can only appear in a block, only Block
    # needs to deal with the repeat behavior.
    def execute(self, trans, st, state, event):
        raise Exception("Not implemented.")
        
# This represents a Raw ATL block.
class RawBlock(RawStatement):

    def __init__(self):

        # A list of RawStatements in this block.
        self.statements = [ ]

    def compile(self):
        return Block(self.statements)

    
# A compiled ATL block. 
class Block(Statement):
    def __init__(self, statements):
        statements = [ i.compile() for i in statements ]

        # A list of statements in the block.
        self.statements = statements

    def execute(self, trans, st, state, event):

        # Unpack the state.
        if state is not None:
            index, start, repeats, child_state = state
        else:
            index, start, repeats, child_state = 0, 0, 0, None
        
        for i in range(0, 64):

            # If we've hit the last statement, it's the end of
            # this block.
            if index >= len(self.statements):
                return "next", st - start
            
            try:
                # Find the statement and try to run it.
                stmt = self.statements[index]
                action, arg = stmt.execute(trans, st - start, child_state, event)

                # On continue, persist our state.
                if action == "continue":
                    return "continue", (index, start, repeats, arg)

                # On next, advance to the next statement in the block.
                elif action == "next":
                    index += 1
                    start = st - arg
                    child_state = None

                # On repeat, either terminate the block, or go to
                # the first statement.
                elif action== "repeat":
                    count, arg = arg

                    repeats += 1

                    if repeats >= count:
                        return "next", arg
                    else:
                        index = 0
                        start = st - arg
                        child_state = None

            except:
                # If an exception occurs when dealing with a statment,
                # advance to the next statement.
                
                if renpy.config.debug:
                    raise

                index += 1
                start = st
                child_state = None

        else:

            if renpy.config.developer or renpy.config.debug:
                raise Exception("ATL Block probably in infinite loop.")

            return "continue", (index, st, repeats, child_state)


# This can become one of four things:
#
# - A pause.
# - An interpolation (which optionally can also reference other
# blocks, as long as they're not time-dependent, and have the same
# arity as the interpolation).
# - A call to another block.
# - A command to change the image, perhaps with a transition.
#
# We won't decide which it is until runtime, as we need the
# values of the variables here.
class RawMultipurpose(RawStatement):

    def __init__(self):
        self.interpolator = None
        self.duration = 0

        self.properties = [ ]
        self.expressions = [ ]
        
    def add_interpolator(self, name, duration):
        self.interpolator = name
        self.duration = 0
        
    def add_property(self, name, exprs):
        self.properties.append((name, exprs))

    def add_expression(self, expr, with_clause):
        self.expressions.append((expr, with_clause))

    def compile(self):

        # Figure out what kind of statement we have. If there's no
        # interpolator, and no properties, than we have either a
        # call, or a child statement.
        if self.interpolator is None and not self.properties and len(self.expressions) == 1:

            expr, withexpr = self.expressions[0]

            child = renpy.python.py_eval(expr)
            if withexpr:
                transition = renpy.python.py_eval(withexpr)
            else:
                transition = None

            if isinstance(child, (int, float)):
                return Interpolation(pause, child, [ ])
                
            if isinstance(child, TransformBase):
                child.compile()
                return child.block

            else:
                return Child(child, transition)

        # Otherwise, we probably have an interpolation statement.
        interpolator = self.interpolator or "pause"

        if interpolator not in interpolators:
            raise Exception("ATL Interpolator %s is unknown at runtime." % interpolator)

        ifunc, arity = interpolators[interpolator]

        properties = [ ]

        for i, exprs in self.properties:
            pfunc = properties_registry.get(i, None)
            if pfunc is None:
                raise Exception("ATL Property %s is unknown at runtime." % i)

            if len(exprs) != arity:
                raise Exception("ATL Property %s has incorrect number of expressions at runtime." % i)

            values = [ renpy.python.py_eval(i) for i in exprs ]

            properties.append((i, values))

        for expr, with_ in self.expressions:
            try:
                value = renpy.python.py_eval(expr)
            except:
                raise Exception("Could not evaluate expression %r when compiling ATL." % expr)

            if not isinstance(value, TransformBase):
                raise Exception("Expression %r is not an ATL transform, and so cannot be included in an ATL interpolation." % expr)

            value.compile()

            if value.properties is None:
                raise Exception("ATL transform %r is too complicated to be included in interpolation." % expr)

            if value.arity != arity:
                raise Exception("ATL transform %r contains properties with the wrong number of arguments." % expr)

            properties.extend(value.properties)

        return Interpolation(ifunc, self.duration, properties)
            
            
            
# This changes the child of this statement, optionally with a transition.
class Child(Statement):

    def __init__(self, child, transition):
        self.child = child
        self.transition = transition

    def execute(self, trans, st, state, event):
        old_child = trans.raw_child

        if old_child is not None and self.transition is not None:
            trans.child = self.transition(old_widget=old_child,
                                          new_widget=self.child)
        else:
            trans.child = self.child

        trans.raw_child = self.child

        return "next", st
    
        
        
# This causes interpolation to occur.
class Interpolation(Statement):

    def __init__(self, function, duration, properties):
        self.function = function
        self.duration = duration
        self.properties = properties

    def execute(self, trans, st, state, event):

        if self.duration:
            complete = min(1.0, st / self.duration)
        else:
            complete = 1.0

        if state is None:

            state = { }
            
            for k in self.properties:
                getter = properties_registry[k][0]
                state[k] = getter(trans)

        for k, v in self.properties.iteritems():
            setter = properties_registry[k][1]
            value = self.function(complete, state[k], *v)
            setter(trans, value)

        if st > self.duration:
            return "next", st - self.duration
        else:
            return "continue", state
        
        
                
        
# This parses an ATL block.
def parse_atl(l):

    l.advance()
    
    # The ATL block we're parsing.
    block = RawBlock()
    
    while not l.eob:

        if False:
            pass

        else:
            # If we can't assign it it a statement more specifically,
            # we try to parse it into a RawMultipurpose. That will
            # then be turned into another statement, as appropriate.
            
            # The RawMultipurpose we add things to.
            rm = renpy.atl.RawMultipurpose()

            # The arity of that statement.
            arity = None

            # First, look for an interpolator. If we see one, use
            # it. Otherwise, use the default interpolator.
            clause = l.name()

            if clause in renpy.atl.interpolators:
                duration = l.require(l.simple_expression)
                func, arity = interpolators[clause]
            else:
                clause, arity = None, 1
                duration = 0
                
            rm.add_interpolator(clause, duration)

            # Now, look for properties and simple_expressions.
            while True:

                # Try to parse a property. 
                cp = l.checkpoint()
                
                prop = l.name()
                
                if prop in properties_registry:
                    exprs = [ ]
                    
                    for i in range(arity):
                        exprs.append(l.require(l.simple_expression))

                    rm.add_property(prop, exprs)

                    continue

                # Otherwise, try to parse it as a simple expressoon,
                # with an optional with clause.

                l.revert(cp)

                expr = l.simple_expression()

                if not expr:
                    break

                if l.keyword("with"):
                    with_expr = l.require(l.simple_expression)
                else:
                    with_expr = None

                rm.add_expression(expr, with_expr)

            block.statements.append(rm)

                
        if l.eol():
            l.advance()
            continue

        l.require(",", "comma or end of line")
