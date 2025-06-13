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

import math

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
    __slots__ = ("filename", "linenumber", "next")
    def __init__(self, loc: NodeLocation):
        self.filename, self.linenumber = loc
        self.next: Node | None = None

    def chain(self, next: "Node | None") -> None:
        """
        This is called with the Node node that should be followed after
        executing this node, and all nodes that this node
        executes. (For example, if this node is a block label, the
        next is the node that should be executed after all nodes in
        the block.)
        """

        self.next = next

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

        Returning None indicates that the node is done executing. You should
        then call `next_node()` with the next node to execute.

        `state`
            The last state that was returned from this node.

        `t`
            The time since start was called.
        """
        next_node(self.next)
        return None

    def ready(self) -> bool:
        """
        Returns True if this node is ready to execute, or False otherwise.
        """
        return True

    def get_repr_params(self) -> str:
        """
        Returns a string representation of the parameters of this node.
        This is used in the __repr__ method to provide additional information
        about the node.
        """
        return ""

    def __repr__(self):
        if params := self.get_repr_params():
            params = " " + params
        return "<{}{} ({}:{})>".format(type(self).__name__, params, self.filename, self.linenumber)


class Condition(Node):
    """
    A base class for conditions that can be used in test scripts.

    Conditions should NOT execute any actions or change the state of the game.
    They should only check if a certain condition is met.
    """
    def execute(self, state: State, t: float) -> State:
        raise TestcaseException("Conditions should not be executed directly. Use `ready()` instead.")

class TestcaseException(ValueError):pass

class SelectorException(TestcaseException):pass


class Selector(Condition):
    """
    Base class for selectors. Selectors find a focusable or displayable
    item on the screen.
    """

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
            raise ValueError("Specify screen and/or id.")

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


class TextSelector(Selector):
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
        super(TextSelector, self).__init__(loc)
        self.pattern = pattern

    def element_not_found_during_perform(self) -> None:
        if self.pattern:
            raise SelectorException("The given {!r} pattern was not resolved to a target".format(self.pattern))

    def get_element(self) -> Focus | None:
        return renpy.test.testfocus.find_focus(self.pattern)


class SelectorDrivenNode(Node):
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
        regardless of whether the selector is ready.
    """

    __slots__ = ("selector", "position", "always")

    def __init__(
        self,
        loc: NodeLocation,
        selector: Selector | None = None,
        position: Position | None = None,
        always: bool = False,
    ):
        super(SelectorDrivenNode, self).__init__(loc)
        self.selector = selector
        self.position = position
        self.always = always

    def execute(self, state: State, t: float) -> State:
        if renpy.display.interface.trans_pause and (t < _test.transition_timeout):
            return state

        if self.selector and not self.selector.ready():
            return state

        x, y = self.get_position()

        rv = self.perform(x, y, state, t)
        if rv is None:
            next_node(self.next)
            return None

        return rv

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

    def perform(self, x: int, y: int, state: State, t: float) -> State | None:
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


class Click(SelectorDrivenNode):
    # The number of the button to click.
    button: int = 1

    def perform(self, x, y, state, t):
        click_mouse(self.button, x, y)


class Move(SelectorDrivenNode):
    def perform(self, x, y, state, t):
        move_mouse(x, y)


class Scroll(Node):
    __slots__ = "pattern"
    def __init__(self, loc: NodeLocation, pattern: str | None = None):
        super(Scroll, self).__init__(loc)
        self.pattern = pattern

    def execute(self, state, t):
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

        next_node(self.next)
        return None

    def ready(self):
        f = renpy.test.testfocus.find_focus(self.pattern)
        return f is not None


class Drag(Node):
    __slots__ = ("points", "pattern", "button", "steps")
    def __init__(self, loc: NodeLocation, points: list[tuple[int, int]]):
        super(Drag, self).__init__(loc)
        self.points = points

        self.pattern: str | None = None
        self.button: int = 1
        self.steps: int = 10

    def execute(self, state, t):
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
            next_node(self.next)
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


class Type(SelectorDrivenNode):
    __slots__ = "text"
    # interval = .01 # unused

    def __init__(self, loc: NodeLocation, text: str, **kwargs):
        super().__init__(loc, **kwargs)
        self.text = text

    def start(self):
        return 0

    def perform(self, x, y, state, t):
        if state >= len(self.text):
            next_node(self.next)
            return None

        move_mouse(x, y)

        keysym = "K_" + self.text[state]
        renpy.test.testkey.down(self, keysym)
        renpy.test.testkey.up(self, keysym)

        return state + 1


class Keysym(SelectorDrivenNode):
    __slots__ = "keysym"

    def __init__(self, loc: NodeLocation, keysym: str, **kwargs):
        super().__init__(loc, **kwargs)
        self.keysym = keysym

    def perform(self, x, y, state, t):
        move_mouse(x, y)
        renpy.test.testkey.queue_keysym(self, self.keysym)


class Action(Node):
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
        if renpy.test.testexecution.action:
            return state
        else:
            next_node(self.next)
            return None

    def ready(self):
        action = renpy.python.py_eval(self.expr)
        return renpy.display.behavior.is_sensitive(action)


class Pause(Node):
    __slots__ = "expr"
    def __init__(self, loc: NodeLocation, expr):
        super(Pause, self).__init__(loc)
        self.expr = expr

    def start(self):
        return float(renpy.python.py_eval(self.expr))

    def execute(self, state, t):
        if t < state:
            return state
        else:
            next_node(self.next)
            return None

    def get_repr_params(self):
        return f"{self.expr}"


class Label(Condition):
    __slots__ = "name"
    def __init__(self, loc: NodeLocation, name: str):
        super(Label, self).__init__(loc)
        self.name = name

    def ready(self):
        return self.name in renpy.test.testexecution.labels

    def get_repr_params(self):
        return f"{self.name}"


class Eval(Condition):
    __slots__ = ("expr")
    def __init__(self, loc: NodeLocation, expr):
        super(Eval, self).__init__(loc)
        self.expr = expr

    def ready(self):
        return bool(renpy.python.py_eval(self.expr))


class Pass(Node):
    pass


################################################################################
# Boolean proxy clauses

class Not(Condition):
    __slots__ = "condition"
    def __init__(self, loc: NodeLocation, condition: Condition):
        super(Not, self).__init__(loc)
        self.condition = condition

    def ready(self):
        return not self.condition.ready()

class Binary(Condition):
    __slots__ = ("left", "right",
                 "left_ready", "right_ready",
                 "left_state", "right_state")

    def __init__(self, loc: NodeLocation, left: Condition, right: Condition):
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

        if self.state() is None:
            next_node(self.next)
            return None

        next_node(self)
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

        if self.state() is None:
            next_node(self.next)
            return None

        next_node(self)
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

    `left`
        The node to execute repeatedly until `right` is ready.
    `right`
        The condition that must be ready for the node to stop executing.
    `timeout`
        The maximum time in seconds to wait for `right` to be ready.
        If None, the node will never time out.
        If float("NaN"), uses the global test timeout setting.
    """
    __slots__ = ("left", "right", "timeout")
    def __init__(self, loc: NodeLocation, left: Node, right: Condition, timeout: float | None = float("NaN")
    ):
        Node.__init__(self, loc)
        self.left = left
        self.right = right
        self.timeout = timeout

    def start(self):
        if self.timeout and math.isnan(self.timeout):
            self.timeout = _test.timeout

        return (None, None, 0, False)

    def execute(self, state, t):
        if self.timeout is not None and t > self.timeout:
            msg = "Testcase timed out after {} seconds.".format(self.timeout)
            raise renpy.test.testexecution.TestcaseException(msg)

        child, child_state, start_time, has_started = state

        if self.right.ready():
            next_node(self.next)
            return None

        else:
            ## The right hand side is not ready, so we execute the left hand side.
            if child == self.left or self.left.ready():
                if not has_started:
                    child = self.left
                    child_state = self.left.start()
                    start_time = t
                    has_started = True

            child_state = self.left.execute(child_state, t - start_time)

            if child_state is None:
                next_node(self)
                return (None, None, 0, False)

        next_node(self)
        return child, child_state, start_time, has_started

    def ready(self):
        return self.left.ready() or self.right.ready()


class If(Node):
    """
    If `condition` is ready, runs the block. Otherwise, goes to the next
    statement.
    """
    __slots__ = ("entries",)
    def __init__(self, loc: NodeLocation, entries: list[tuple[Node, "Block"]]):
        Node.__init__(self, loc)

        self.entries = entries # List of (condition, block) tuples.

    def execute(self, state, t):
        for condition, block in self.entries:
            if renpy.python.py_eval(condition):
                next_node(block.block[0])
                return None

        next_node(self.next)
        return None


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
        if renpy.test.testexecution.action:
            return True
        else:
            next_node(self.next)
            return None

    def __call__(self):
        renpy.python.py_exec_bytecode(self.code.bytecode, self.hide)


class AssertError(AssertionError):pass


class Assert(Condition):
    __slots__ = "condition"
    def __init__(self, loc: NodeLocation, condition: Condition):
        Node.__init__(self, loc)
        self.condition = condition

    def ready(self):
        if not self.condition.ready():
            raise AssertError("On line {}:{}, assertion of {} failed.".format(self.filename,
                                                                              self.linenumber,
                                                                              self.condition))
        return True


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

    def execute(self, state, t):
        n = renpy.test.testexecution.call_node(self.target)
        print("Call test", self.target)
        next_node(n)
        return None

    def get_repr_params(self):
        return f"{self.target}"


################################################################################
# Control structures.


class Block(Node):
    __slots__ = "block"
    def __init__(self, loc: NodeLocation, block: list[Node]):
        Node.__init__(self, loc)
        self.block = block

    def chain(self, next):
        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            super().chain(next)

    def execute(self, state, t):
        if not self.block:
            next_node(self.next)
            return None

        next_node(self.block[0])
        return None


class Exit(Node):
    def execute(self, state, t):
        raise renpy.game.QuitException


################################################################################
# Utility functions
################################################################################

def chain_block(block: list[Node], next: Node | None) -> None:
    """
    This is called to chain together all of the nodes in a block. Node
    n is chained with node n+1, while the last node is chained with
    next.
    """

    if not block:
        return

    for a, b in zip(block, block[1:]):
        a.chain(b)

    block[-1].chain(next)


def next_node(node: Node | None):
    """
    Indicates the next node that should be executed.
    """

    renpy.test.testexecution.next_node = node
