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
def pause(duration, t, start, end):
    if t < duration:
        return start
    else:
        return end

register_atl_interpolator("pause", pause, 1)
    
# A map from the name of a property to the function that sets that
# property on a Transform object.
properties = { }

def register_atl_property(name, f):
    properties[name] = f


# This can become one of three things:
#
# - An interpolation (which optionally can also reference other
# blocks, as long as they're not time-dependent, and have the same
# arity as the interpolation).
# - A call to another block.
# - A command to change the image, perhaps with a transition.
#
# We won't decide which it is until runtime, as we need the
# values of the variables here.
class RawMultipurpose(renpy.object.object):

    def __init__(self):
        self.interpolator = None
        self.properties = [ ]
        self.expressions = [ ]
        
    def add_interpolator(self, name, duration):
        self.interpolator = name
        self.duration = 0
        
    def add_property(self, name, exprs):
        self.properties.append((name, exprs))

    def add_expression(self, expr, with_clause):
        self.expressions.append((expr, with_clause))
    
# This parses an ATL block.
def parse_atl(stmtl):
    
    l = stmtl.subblock_lexer()

    # Create an ATL block here.

    while True:

        if False:
            pass

        else:
            # If we can't assign it it a statement more specifically,
            # we try to parse it into a RawMultipurpose. That will
            # then be turned into another statement, as appropriate.
            
            # The RawMultipurpose we add things to.
            rm = renpy.atl.RawInterpolation()

            # The arity of that statement.
            arity = None

            # First, look for an interpolator. If we see one, use
            # it. Otherwise, use the default interpolator.
            clause = l.name()

            if clause in renpy.atl.interpolators:
                duration = l.require(l.simple_expression)
                func, arity = renpy.atl.interpolators[clause]
            else:
                clause, arity = "pause", 1
                duration = 0
                
            rm.add_interpolator(clause, duration)

            # Now, look for properties and simple_expressions.
            while True:

                # Try to parse a property. 
                cp = l.checkpoint()
                
                prop = l.require(l.name, 'property')

                if clause in renpy.atl.properties:
                    exprs = [ ]
                    
                    for i in range(arity):
                        exprs.append(l.require(l.simple_expression))

                    rm.add_property(prop, exprs)

                    continue

                # Otherwise, try to parse it as a simple expressoon,
                # with an optional with clause.

                l.rollback(cp)

                expr = l.simple_expression()

                if not expr:
                    break

                if l.keyword("with"):
                    with_expr = l.require(l.simple_expression)
                else:
                    with_expr = None

                rm.add_expression(expr, with_expr)

        if l.eol():
            l.advance()
            continue

        l.require(",", "comma or end of line")

        
                
                

                
                    
                    
                




                
                
                
    
    
    
    
