# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

import renpy.display
import renpy.test
from renpy.test.testmouse import click_mouse, move_mouse

# This is an object that is used to configure test settings.
_test = renpy.object.Object()

# Should we use maximum framerate mode?
_test.maximum_framerate = True

# How long should we wait before declaring the test stuck?
_test.timeout = 5.0

# Should we force the test to proceed despite suppress_underlay?
_test.force = False

# How long should we wait for a transition before we proceed?
_test.transition_timeout = 5.0


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

    def report(self):
        """
        Reports the location of this statement. This should only be called
        in the execute method of leaf nodes of the test tree.
        """

        renpy.test.testexecution.node_loc = (self.filename, self.linenumber)


class Pattern(Node):

    position = None
    always = False

    def __init__(self, loc, pattern=None):
        Node.__init__(self, loc)
        self.pattern = pattern

    def start(self):
        return True

    def execute(self, state, t):

        self.report()

        if renpy.display.interface.trans_pause and (t < _test.transition_timeout):
            return state

        if self.position is not None:
            position = renpy.python.py_eval(self.position)
        else:
            position = (None, None)

        f = renpy.test.testfocus.find_focus(self.pattern)

        if f is None:
            x, y = None, None
        else:
            x, y = renpy.test.testfocus.find_position(f, position)

        if x is None:
            if self.pattern:
                return state
            else:
                x, y = renpy.exports.get_mouse_pos()

        return self.perform(x, y, state, t)

    def ready(self):

        if self.always:
            return True

        f = renpy.test.testfocus.find_focus(self.pattern)

        if f is not None:
            return True
        else:
            return False


class Click(Pattern):

    # The number of the button to click.
    button = 1

    def perform(self, x, y, state, t):
        click_mouse(self.button, x, y)
        return None


class Move(Pattern):

    def perform(self, x, y, state, t):
        move_mouse(x, y)
        return None


class Scroll(Node):

    def __init__(self, loc, pattern=None):
        Node.__init__(self, loc)
        self.pattern = pattern

    def start(self):
        return True

    def execute(self, state, t):

        self.report()

        f = renpy.test.testfocus.find_focus(self.pattern)

        if f is None:
            return True

        if not isinstance(f.widget, renpy.display.behavior.Bar):
            return True

        adj = f.widget.adjustment

        if adj.value == adj.range:
            new = 0
        else:
            new = adj.value + adj.page

            if new > adj.range:
                new = adj.range

        adj.change(new)

        return None

    def ready(self):

        f = renpy.test.testfocus.find_focus(self.pattern)

        if f is not None:
            return True
        else:
            return False


class Drag(Node):

    def __init__(self, loc, points):
        Node.__init__(self, loc)
        self.points = points

        self.pattern = None
        self.button = 1
        self.steps = 10

    def start(self):
        return True

    def execute(self, state, t):

        self.report()

        if renpy.display.interface.trans_pause:
            return state

        if self.pattern:

            f = renpy.test.testfocus.find_focus(self.pattern)
            if f is None:
                return state

        else:
            f = None

        if state is True:

            points = renpy.python.py_eval(self.points)
            points = [ renpy.test.testfocus.find_position(f, i) for i in points ]

            if len(points) < 2:
                raise Exception("A drag requires at least two points.")

            interpoints = [ ]

            xa, ya = points[0]

            interpoints.append((xa, ya))

            for xb, yb in points[1:]:
                for i in range(1, self.steps + 1):
                    done = 1.0 * i / self.steps

                    interpoints.append((
                        int(xa + done * (xb - xa)),
                        int(ya + done * (yb - ya)),
                        ))

                xa = xb
                ya = yb

            x, y = interpoints.pop(0)

            renpy.test.testmouse.move_mouse(x, y)
            renpy.test.testmouse.press_mouse(self.button)

        else:

            interpoints = state

            x, y = interpoints.pop(0)
            renpy.test.testmouse.move_mouse(x, y)

        if not interpoints:
            renpy.test.testmouse.release_mouse(self.button)
            return None

        else:
            return interpoints

    def ready(self):

        if self.pattern is None:
            return True

        f = renpy.test.testfocus.find_focus(self.pattern)

        if f is not None:
            return True
        else:
            return False


class Type(Pattern):

    interval = .01

    def __init__(self, loc, keys):
        Pattern.__init__(self, loc)
        self.keys = keys

    def start(self):
        return 0

    def perform(self, x, y, state, t):

        if state >= len(self.keys):
            return None

        move_mouse(x, y)

        keysym = self.keys[state]
        renpy.test.testkey.down(self, keysym)
        renpy.test.testkey.up(self, keysym)

        return state + 1


class Action(Node):

    def __init__(self, loc, expr):
        Node.__init__(self, loc)
        self.expr = expr

    def start(self):
        renpy.test.testexecution.action = renpy.python.py_eval(self.expr)
        return True

    def execute(self, state, t):

        self.report()

        if renpy.test.testexecution.action:
            return True
        else:
            return None

    def ready(self):

        self.report()

        action = renpy.python.py_eval(self.expr)
        return renpy.display.behavior.is_sensitive(action)


class Pause(Node):

    def __init__(self, loc, expr):
        Node.__init__(self, loc)
        self.expr = expr

    def start(self):
        return float(renpy.python.py_eval(self.expr))

    def execute(self, state, t):

        self.report()

        if t < state:
            return state
        else:
            return None


class Label(Node):

    def __init__(self, loc, name):
        Node.__init__(self, loc)
        self.name = name

    def start(self):
        return True

    def execute(self, state, t):
        if self.name in renpy.test.testexecution.labels:
            return None
        else:
            return state

    def ready(self):
        return self.name in renpy.test.testexecution.labels


################################################################################
# Non-clause statements.

class Until(Node):
    """
    Executes `left` repeatedly until `right` is ready, then executes `right`
    once before quitting.
    """

    def __init__(self, loc, left, right):
        Node.__init__(self, loc)
        self.left = left
        self.right = right

    def start(self):
        return (None, None, 0)

    def execute(self, state, t):
        child, child_state, start = state

        if self.right.ready() and not (child is self.right):
            child = self.right
            child_state = None

        elif child is None:
            child = self.left

        if child_state is None:
            child_state = child.start()
            start = t

        if child_state is not None:
            child_state = child.execute(child_state, t - start)

        if (child_state is None) and (child is self.right):
            return None

        return child, child_state, start

    def ready(self):
        return self.left.ready() or self.right.ready()


class If(Node):
    """
    If `condition` is ready, runs the block. Otherwise, goes to the next
    statement.
    """

    def __init__(self, loc, condition, block):
        Node.__init__(self, loc)

        self.condition = condition
        self.block = block

    def start(self):
        return (None, None, 0)

    def execute(self, state, t):
        node, child_state, start = state

        if node is None:
            if not self.condition.ready():
                return None

            node = self.block

        node, child_state, start = renpy.test.testexecution.execute_node(t, node, child_state, start)

        if node is None:
            return None

        return (node, child_state, start)


class Python(Node):

    def __init__(self, loc, code):
        Node.__init__(self, loc)
        self.code = code

    def start(self):
        renpy.test.testexecution.action = self
        return True

    def execute(self, state, t):

        self.report()

        if renpy.test.testexecution.action:
            return True
        else:
            return None

    def __call__(self):
        renpy.python.py_exec_bytecode(self.code.bytecode)


class Assert(Node):

    def __init__(self, loc, expr):
        Node.__init__(self, loc)
        self.expr = expr

    def start(self):
        renpy.test.testexecution.action = self
        return True

    def execute(self, state, t):

        self.report()

        if renpy.test.testexecution.action:
            return True
        else:
            return None

    def __call__(self):
        if not renpy.python.py_eval(self.expr):
            raise Exception("On line {}:{}, assertion {} failed.".format(self.filename, self.linenumber, self.expr))


class Jump(Node):

    def __init__(self, loc, target):
        Node.__init__(self, loc)

        self.target = target

    def start(self):
        node = renpy.test.testexecution.lookup(self.target, self)
        raise renpy.test.testexecution.TestJump(node)


class Call(Node):

    def __init__(self, loc, target):
        Node.__init__(self, loc)

        self.target = target

    def start(self):
        print("Call test", self.target)
        node = renpy.test.testexecution.lookup(self.target, self)
        return (node, None, 0)

    def execute(self, state, t):
        node, child_state, start = state

        node, child_state, start = renpy.test.testexecution.execute_node(t, node, child_state, start)

        if node is None:
            return None

        return (node, child_state, start)


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
