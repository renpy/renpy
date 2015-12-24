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


# The overridden positioning of the mouse.
mouse_pos = None

def get_mouse_pos(x, y):
    """
    Called to get the overridden mouse position.
    """

    if mouse_pos is None:
        return x, y

    return


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

    def per_interact(self, state, t):
        """
        Called at the start or restart of an interaction.

        `state`
            The last state that was returned from this node.

        `t`
            The time since start was called.
        """

        return True

    def periodic(self, state, t):
        """
        Called periodically over the course of each interaction.

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

    def __init__(self, target):
        self.target = target


    def per_interact(self, state, t):
        """
        Called once per interact,
        """

# The root node.
node = None

# The state of the root node.
status = None

# The time the root node started executing.
start_time = None

def periodic():
    """
    Called periodically by the test code to generate events, if desired.
    """

