# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display
from renpy.test.testmouse import click_mouse

class Node(object):
    """
    An AST node for a test script.
    """

    def __init__(self, loc):
        self.filename, self.linenumber = loc

    def start(self):
        """
        Called once when the node starts execution.

        This is expected to return a state, or None to advance to the next
        node.
        """

    def execute(self, state, t):
        """
        Called once each time the screen is drawn.

        `state`
            The last state that was returned from this node.

        `t`
            The time since start was called.
        """

        return state

    def ready(self):
        """
        Returns True if this node is ready to execute, or False otherwise.
        """

        return True

class Click(Node):

    def __init__(self, loc, pattern=None):
        Node.__init__(self, loc)
        self.pattern = pattern

    def start(self):
        return True

    def execute(self, state, t):
        if renpy.display.interface.trans_pause:
            return state

        x, y = renpy.display.focus.matching_focus_coordinates(self.pattern)

        if x is None:
            return state

        click_mouse(1, x, y)
        return None

    def ready(self):

        x, _y = renpy.display.focus.matching_focus_coordinates(self.pattern)

        if x is not None:
            return True
        else:
            return False


class Action(Node):

    def __init__(self, loc, expr):
        Node.__init__(self, loc)
        self.expr = expr

    def start(self):
        renpy.test.testexecution.action = renpy.python.py_eval(self.expr)
        return True

    def execute(self, state, t):
        if renpy.test.testexecution.action:
            return True
        else:
            return None

    def ready(self):
        action = renpy.python.py_eval(self.expr)
        return renpy.display.behavior.is_sensitive(action)


class Pause(Node):

    def __init__(self, loc, expr):
        Node.__init__(self, loc)
        self.expr = expr

    def start(self):
        return float(renpy.python.py_eval(self.expr))

    def execute(self, state, t):
        if t < state:
            return state
        else:
            return None


################################################################################
# Non-clause statements.

class Until(Node):
    """
    Executes `left` repeatedly until `right` is ready, then executes `right`
    once before quitting.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def start(self):
        return (None, None, 0)

    def execute(self, state, t):
        child, child_state, start = state

        if child_state is None:
            if self.right.ready():
                child = self.right
            else:
                child = self.left

            child_state = child.start()
            start = t

        if child_state is not None:
            child_state = child.execute(child_state, t - start)

        if (child_state is None) and (child is self.right):
            return None

        return child, child_state, start


################################################################################
# Control structures.

class Block(Node):

    def __init__(self, loc, block):
        Node.__init__(self, loc)
        self.block = block

    def start(self):
        return (0, None, None)

    def execute(self, state, t):
        i, start, s = state

        if i >= len(self.block):
            return None

        if s is None:
            s = self.block[i].start()
            start = t

        if s is not None:
            s = self.block[i].execute(s, t - start)

        if s is None:
            i += 1

        return i, start, s

