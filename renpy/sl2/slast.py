# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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


# This file contains the abstract syntax tree for a screen language
# screen.

# A serial number that makes each SLNode unique.
serial = 0

# A constant used when a node does not have children.

class SLContext(object):
    """
    A context object that can be passed to the execute methods.
    """

    def __init__(self, parent=None):
        if parent is not None:

            # The scope that python methods are evaluated in.
            self.scope = parent.scope

            # A list of child displayables that will be added to an outer
            # displayable.
            self.children = parent.children

            # A list of keywords.
            self.keywords = parent.keywords

            # The style prefix that is given to children of this displayable.
            self.style_prefix = parent.style_prefix

        else:
            self.scope = { }
            self.children = [ ]
            self.keywords = { }
            self.style_prefix = None


class SLNode(object):
    """
    The base class for screen language nodes.
    """

    def __init__(self):
        global serial
        serial += 1

        self.serial = serial

    def execute(self, context):
        """
        Execute this node, updating context as appropriate.
        """

class SLBlock(object):
    """
    Represents a screen language block that can contain keyword arguments
    and child displayables.
    """

    def __init__(self):

        # A list of keyword argument, expr tuples.
        self.keyword = [ ]

        # A list of child SLNodes.
        self.children = [ ]

class SLDisplayable(SLBlock):
    """
    A screen language AST node that corresponds to a displayable being
    added to the tree.
    """

    def __init__(self, displayable, scope=False, child_or_fixed=False):
        """
        `displayable`
            A function that, when called with the positional and keyword
            arguments, causes the displayable to be displayed.

        `scope`
            If true, the scope is supplied as an argument to the displayable.

        `child_or_fixed`
            If true and the number of children of this displayable is not one,
            the children are added to a Fixed, and the Fixed is added to the
            displayable.
        """

        self.displayable = displayable
        self.scope = scope
        self.child_or_fixed = child_or_fixed

        # Positional argument expressions.
        self.positional = [ ]



