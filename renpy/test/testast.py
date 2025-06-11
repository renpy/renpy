# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import renpy
from renpy.test.testmouse import click_mouse, move_mouse


class TestSettings(renpy.object.Object):
    def __init__(self):
        # Should we use maximum framerate mode?
        self.maximum_framerate = True

        # How long should we wait before declaring the test stuck?
        self.timeout = 5.0

        # Should we force the test to proceed despite suppress_underlay?
        self.force = False

        # How long should we wait for a transition before we proceed?
        self.transition_timeout = 5.0

        # How many times should we try to find a good spot to place the mouse?
        self.focus_trials = 100

_test = TestSettings()


class Node(object):
    """
    An AST node for a test script.
    """
    __slots__ = ("filename", "linenumber")
    def __init__(self, loc):
        self.filename, self.linenumber = loc

    def start(self):
        """
        Called once when the node starts execution.

        This is expected to return a state, or None to advance to the next
        node.
        """
        return True

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


class Clause(Node):
    __slots__ = ()

    def __repr__(self):
        return "<{} test clause>".format(type(self).__name__.lower())


class PatternException(ValueError):pass

class Pattern(Clause):
    __slots__ = ("pattern", "position", "always")

    def __init__(self, loc, pattern=None):
        super(Pattern, self).__init__(loc)
        self.pattern = pattern
        self.position = None
        self.always = False

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

        if None in (x, y):
            if self.pattern:
                raise PatternException("The given {!r} pattern was not resolved to a target".format(self.pattern))
            x, y = renpy.exports.get_mouse_pos()

        return self.perform(x, y, state, t)

    def ready(self):
        if self.always:
            return True

        f = renpy.test.testfocus.find_focus(self.pattern)

        return (f is not None)

    def perform(self, x, y, state, t):
        return None


class Click(Pattern):
    # The number of the button to click.
    button = 1

    def perform(self, x, y, state, t):
        click_mouse(self.button, x, y)
        return None


class Move(Pattern):
    __slots__ = ()
    def perform(self, x, y, state, t):
        move_mouse(x, y)
        return None


class Scroll(Clause):
    __slots__ = "pattern"
    def __init__(self, loc, pattern=None):
        super(Scroll, self).__init__(loc)
        self.pattern = pattern

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


class Drag(Clause):
    __slots__ = ("points", "pattern", "button", "steps")
    def __init__(self, loc, points):
        super(Drag, self).__init__(loc)
        self.points = points

        self.pattern = None
        self.button = 1
        self.steps = 10

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
            points = [renpy.test.testfocus.find_position(f, i) for i in points]

            if len(points) < 2:
                raise ValueError("A drag requires at least two points.")

            interpoints = []

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
    __slots__ = "keys"
    # interval = .01 # unused

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


class Action(Clause):
    """
    This is for the `run` keyword
    """
    __slots__ = "expr"
    def __init__(self, loc, expr):
        super(Action, self).__init__(loc)
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


class Pause(Clause):
    __slots__ = "expr"
    def __init__(self, loc, expr):
        super(Pause, self).__init__(loc)
        self.expr = expr

    def start(self):
        return float(renpy.python.py_eval(self.expr))

    def execute(self, state, t):
        self.report()

        if t < state:
            return state
        else:
            return None


class Label(Clause):
    __slots__ = "name"
    def __init__(self, loc, name):
        super(Label, self).__init__(loc)
        self.name = name

    def execute(self, state, t):
        return None

    def ready(self):
        return self.name in renpy.test.testexecution.labels


class Eval(Clause):
    __slots__ = ("expr", "evaluated")
    def __init__(self, loc, expr):
        super(Eval, self).__init__(loc)
        self.expr = expr
        self.evaluated = False

    def execute(self, state, t):
        if not self.evaluated: # check if this is necessary
            self.ready()
        return None

    def ready(self):
        rv = bool(renpy.python.py_eval(self.expr))
        self.evaluated = True
        return rv

class Pass(Clause):
    __slots__ = ()
    def execute(self, state, t):
        return None


################################################################################
# Boolean proxy clauses

class Not(Clause):
    __slots__ = "clause"
    def __init__(self, loc, clause):
        super(Not, self).__init__(loc)
        self.clause = clause

    def start(self):
        return self.clause.start()

    def execute(self, state, t):
        # return self.clause.execute(state, t)
        return None

    def ready(self):
        return not self.clause.ready()

class Binary(Clause):
    __slots__ = ("left", "right",
                 "left_ready", "right_ready",
                 "left_state", "right_state")

    def __init__(self, loc, left, right):
        super(Binary, self).__init__(loc)
        self.left = left
        self.right = right
        self.left_ready = self.right_ready = None

    def start(self):
        self.left_state = self.left.start()
        self.right_state = self.right.start()
        return self.state()

class And(Binary):
    __slots__ = ()

    def state(self):
        if (self.left_state is None) and (self.right_state is None):
            return None
        return True

    def execute(self, state, t):
        """
        Executes both if both are ready, otherwise the left one.
        """
        self.ready()

        if self.left_state is not None:
            self.left_state = self.left.execute(self.left_state, t)

        if self.left_ready and self.right_ready and (self.right_state is not None):
            self.right_state = self.right.execute(self.right_state, t)

        return self.state()

    def ready(self):
        """
        Memorizes the computed values.
        Effectively returns self.left.ready() and self.right.ready().
        """
        self.left_ready = self.left.ready()
        self.right_ready = self.right.ready()
        return self.left_ready and self.right_ready

class Or(Binary):
    __slots__ = ()

    def state(self):
        if (self.left_state is None) or (self.right_state is None):
            return None
        return True

    def execute(self, state, t):
        """
        Executes the ready one(s), if any, otherwise the right one.
        """
        self.ready()

        if self.left_ready and (self.left_state is not None):
            self.left_state = self.left.execute(self.left_state, t)

        if (self.right_ready or not self.left_ready) and (self.right_state is not None):
            self.right_state = self.right.execute(self.right_state, t)

        return self.state()

    def ready(self):
        """
        Memorizes the computed values.
        Effectively returns self.left.ready() or self.right.ready().
        """
        self.left_ready = self.left.ready()
        self.right_ready = self.right.ready()
        return self.left_ready or self.right_ready


################################################################################
# Non-clause statements.


class Until(Node):
    """
    Executes `left` repeatedly until `right` is ready (and unless it already is),
    then executes `right` once before quitting.
    """
    __slots__ = ("left", "right")
    def __init__(self, loc, left, right):
        Node.__init__(self, loc)
        self.left = left
        self.right = right

    def start(self):
        return (None, None, 0)

    def execute(self, state, t):
        child, child_state, start = state

        if self.right.ready() and (child is not self.right):
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
    __slots__ = ("condition", "block")
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
    __slots__ = ("code", "hide")
    def __init__(self, loc, code, hide=False):
        Node.__init__(self, loc)
        self.code = code
        self.hide = hide

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
        renpy.python.py_exec_bytecode(self.code.bytecode, self.hide)


class AssertError(AssertionError):pass

class Assert(Node):
    __slots__ = "clause"
    def __init__(self, loc, clause):
        Node.__init__(self, loc)
        self.clause = clause

    def execute(self, state, t):
        self.report()

        if not self.clause.ready():
            raise AssertError("On line {}:{}, assertion of {} failed.".format(self.filename,
                                                                              self.linenumber,
                                                                              self.clause))

        return None


class Jump(Node):
    __slots__ = "target"
    def __init__(self, loc, target):
        Node.__init__(self, loc)

        self.target = target

    def start(self):
        node = renpy.test.testexecution.lookup(self.target, self)
        raise renpy.test.testexecution.TestJump(node)


class Call(Node):
    __slots__ = "target"
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
    __slots__ = "block"
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

class Exit(Node):
    __slots__ = ()
    def execute(self, state, t):
        raise renpy.game.QuitException
