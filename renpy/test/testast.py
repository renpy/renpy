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

class TestNode(object):
    """
    An AST node for a test script.
    """

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

class Click(object):

    def __init__(self, pattern=None):
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


class Block(object):
    def __init__(self, block):
        self.block = block

    def start(self):
        return (0, None, None)

    def execute(self,  state, t):
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
