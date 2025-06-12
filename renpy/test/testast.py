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
from renpy.display.focus import Focus
from renpy.display.displayable import Displayable
from renpy.test.testmouse import click_mouse, move_mouse
from renpy.test.types import State, NodeLocation, Position


class TestSettings(renpy.object.Object):
    def __init__(self):
        # Should we use maximum framerate mode?
        self.maximum_framerate: bool = True

        # How long should we wait before declaring the test stuck?
        self.timeout: float = 5.0

        # Should we force the test to proceed despite suppress_underlay?
        self.force: bool = False

        # How long should we wait for a transition before we proceed?
        self.transition_timeout: float = 5.0

        # How many times should we try to find a good spot to place the mouse?
        self.focus_trials: int = 100

_test = TestSettings()


class Node(object):
    """
    An AST node for a test script.
    """
    __slots__ = ("filename", "linenumber")
    def __init__(self, loc: NodeLocation):
        self.filename, self.linenumber = loc

    def start(self) -> State:
        """
        Called once when the node starts execution.

        This is expected to return a state, or None to advance to the next
        node.
        """
        return True

    def execute(self, state: State, t: float) -> State:
        """
        Called once each time the screen is drawn.

        Returning None indicates that the node is done executing, and
        to advance to the next node.

        `state`
            The last state that was returned from this node.

        `t`
            The time since start was called.
        """
        return state

    def ready(self) -> bool:
        """
        Returns True if this node is ready to execute, or False otherwise.
        """
        return True

    def report(self) -> None:
        """
        Reports the location of this statement. This should only be called
        in the execute method of leaf nodes of the test tree.
        """
        renpy.test.testexecution.node_loc = (self.filename, self.linenumber)


class Clause(Node):
    __slots__ = ()

    def __repr__(self):
        return "<{} test clause>".format(type(self).__name__.lower())


class SelectorException(ValueError):pass


class Selector(Clause):
    """
    Base class for selectors. Selectors find a focusable or displayable
    item on the screen.
    """

    def execute(self, state, t):

        self.report()

        if renpy.display.interface.trans_pause and (t < _test.transition_timeout):
            return state

        return None

    def element_not_found_during_perform(self) -> None:
        """
        Called when the element is not found during perform.
        This can be overridden to handle cases where the element is not found.
        """
        raise SelectorException("Element was not found.")

    def get_element(self) -> Displayable | Focus | None:
        """
        Returns the element that this selector is looking for.
        If no element is found, returns None.
        """
        raise NotImplementedError("get_element() must be implemented in subclasses of Selector.")

    def ready(self) -> bool:
        return self.get_element() is not None


class DisplayableSelector(Selector):
    """
    A selector that finds a widget by its id or screen.
    """

    __slots__ = ("screen", "id", "layer")

    def __init__(
        self,
        loc: NodeLocation,
        screen: str | None = None,
        id: str | None = None,
        layer: str | None = None,
    ):
        super(DisplayableSelector, self).__init__(loc)
        self.screen = screen
        self.id = id
        self.layer = layer

        if self.screen is None and self.id is None:
            raise ValueError("A displayable clause must have a screen and/or an id specified.")

    def element_not_found_during_perform(self) -> None:
        if self.screen or self.id:
            raise SelectorException("The displayable with screen {!r} and id {!r} was not found".format(self.screen, self.id))

        raise SelectorException("No displayable was specified.")

    def get_element(self) -> Displayable | None:
        if self.screen and self.id is None:
            return renpy.exports.get_screen(self.screen, self.layer)
        return renpy.exports.get_displayable(self.screen, self.id, self.layer)

    def ready(self) -> bool:
        ## Needs to be checked here and not in __init__ since screens are not be defined yet.
        if self.screen is not None and not renpy.exports.has_screen(self.screen):
            raise ValueError("The screen {!r} does not exist.".format(self.screen))

        return super().ready()


class Pattern(Selector):
    """
    A selector that finds a widget by its text or alt text.
    Once found, the `perform()` method is called.

    `pattern`
        The pattern string used to find a focus.
        This could be a text string, alt text, or another
        identifier recognized by `renpy.test.testfocus.find_focus`.
    """

    __slots__ = ("pattern",)

    def __init__(self, loc: NodeLocation, pattern: str):
        super(Pattern, self).__init__(loc)
        self.pattern = pattern

    def element_not_found_during_perform(self) -> None:
        if self.pattern:
            raise SelectorException("The given {!r} pattern was not resolved to a target".format(self.pattern))

    def get_element(self) -> Focus | None:
        return renpy.test.testfocus.find_focus(self.pattern)


class SelectorDrivenClause(Clause):
    """
    Base class for nodes that perform actions that may take
    a selector as a target.

    `selector`
        An optional `Selector` instance that determines the target

    `position`
        An optional Python expression string that, when evaluated,
        should return a tuple `(x, y)` representing a position relative to the
        target element.
        If not specified or selector is None, the current mouse position will be used.

    `always`
        If True, the `ready()` method will always return True,
        regardless of whether the pattern can be resolved.
    """

    __slots__ = ("selector", "position", "always")

    def __init__(
        self,
        loc: NodeLocation,
        selector: Selector | None = None,
        position: Position | None = None,
        always: bool = False,
    ):
        super(SelectorDrivenClause, self).__init__(loc)
        self.selector = selector
        self.position = position
        self.always = always

    def execute(self, state: State, t: float) -> State:

        self.report()

        if renpy.display.interface.trans_pause and (t < _test.transition_timeout):
            return state

        x, y = self.get_position()

        return self.perform(x, y, state, t)

    def get_position(self) -> tuple[int, int]:
        """
        Returns the x and y coordinates for the action to be performed.
        """
        if self.position is not None:
            position = renpy.python.py_eval(self.position)
        else:
            position = (None, None)

        if self.selector is not None:
            f = self.selector.get_element()
        else:
            f = None

        if f is None:
            x, y = None, None
        else:
            x, y = renpy.test.testfocus.find_position(f, position)

        if None in (x, y):
            if not self.always and self.selector is not None:
                self.selector.element_not_found_during_perform()
            x, y = renpy.exports.get_mouse_pos()

        return x, y # type: ignore

    def perform(self, x: int, y: int, state: State, t: float) -> State:
        """
        Perform the action at the given coordinates.

        Returning None indicates that the node is done executing, and
        to advance to the next node.

        `x`
            The x-coordinate where the action should be performed.
        `y`
            The y-coordinate where the action should be performed.
        `state`
            The current state of the test execution.
        `t`
            The time since start was called.
        """
        raise NotImplementedError("perform() must be implemented in subclasses of SelectorDrivenNode.")

    def ready(self) -> bool:
        if self.always:
            return True

        if self.selector is not None:
            return self.selector.ready()

        return True


class Click(Pattern):
    # The number of the button to click.
    button: int = 1

    def perform(self, x, y, state, t):
        click_mouse(self.button, x, y)
        return None


class Move(SelectorDrivenClause):
    __slots__ = ()
    def perform(self, x, y, state, t):
        move_mouse(x, y)
        return None


class Scroll(Clause):
    __slots__ = "pattern"
    def __init__(self, loc: NodeLocation, pattern: str | None = None):
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
    def __init__(self, loc: NodeLocation, points: list[tuple[int, int]]):
        super(Drag, self).__init__(loc)
        self.points = points

        self.pattern: str | None = None
        self.button: int = 1
        self.steps: int = 10

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


class Type(SelectorDrivenClause):
    __slots__ = "text"
    # interval = .01 # unused

    def __init__(self, loc: NodeLocation, text: str, **kwargs):
        super().__init__(loc, **kwargs)
        self.text = text

    def start(self):
        return 0

    def perform(self, x, y, state, t):
        if state >= len(self.text):
            return None

        move_mouse(x, y)

        keysym = "K_" + self.text[state]
        renpy.test.testkey.down(self, keysym)
        renpy.test.testkey.up(self, keysym)

        return state + 1


class Keysym(SelectorDrivenClause):
    __slots__ = "keysym"

    def __init__(self, loc: NodeLocation, keysym: str, **kwargs):
        super().__init__(loc, **kwargs)
        self.keysym = keysym

    def perform(self, x, y, state, t):

        move_mouse(x, y)
        renpy.test.testkey.queue_keysym(self, self.keysym)

        return None


class Action(Clause):
    """
    This is for the `run` keyword
    """
    __slots__ = "expr"
    def __init__(self, loc: NodeLocation, expr):
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
    def __init__(self, loc: NodeLocation, expr):
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
    def __init__(self, loc: NodeLocation, name: str):
        super(Label, self).__init__(loc)
        self.name = name

    def execute(self, state, t):
        return None

    def ready(self):
        return self.name in renpy.test.testexecution.labels


class Eval(Clause):
    __slots__ = ("expr", "evaluated")
    def __init__(self, loc: NodeLocation, expr):
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
    def __init__(self, loc: NodeLocation, clause: Clause):
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

    def __init__(self, loc: NodeLocation, left: Clause, right: Clause):
        super(Binary, self).__init__(loc)
        self.left = left
        self.right = right
        self.left_ready = self.right_ready = None

    def state(self) -> bool | None:
        """
        Returns the state of this binary clause.
        """
        raise NotImplementedError("state() must be implemented in subclasses of Binary.")

    def start(self):
        self.left_state = self.left.start()
        self.right_state = self.right.start()
        return self.state()

class And(Binary):
    __slots__ = ()

    def state(self) -> bool | None:
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

    def state(self) -> bool | None:
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
    def __init__(self, loc: NodeLocation, left: Node, right: Node):
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
    def __init__(self, loc: NodeLocation, condition: Node, block: "Block"):
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
    def __init__(self, loc: NodeLocation, code: renpy.ast.PyCode, hide: bool =False):
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
    def __init__(self, loc: NodeLocation, clause: Clause):
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
    def __init__(self, loc: NodeLocation, target: str):
        Node.__init__(self, loc)

        self.target = target

    def start(self):
        node = renpy.test.testexecution.lookup(self.target, self)
        raise renpy.test.testexecution.TestJump(node)


class Call(Node):
    __slots__ = "target"
    def __init__(self, loc: NodeLocation, target: str):
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
    def __init__(self, loc: NodeLocation, block: list[Node]):
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
