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
from renpy.test.testsettings import _test
from renpy.test.types import NodeState, NodeLocation, Position, RenpyTestException, RenpyTestTimeoutError, HookType


class SelectorException(RenpyTestException):
    pass


class Node(object):
    """
    An AST node for a test script.
    """

    __slots__ = ("filename", "linenumber", "next", "done")

    def __init__(self, loc: NodeLocation):
        self.filename, self.linenumber = loc
        self.next: Node | None = None
        self.done: bool = False

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        return (self.filename, self.linenumber) == (other.filename, other.linenumber)

    def __repr__(self):
        if params := self.get_repr_params():
            params = " " + params
        return "<{}{} ({}:{})>".format(type(self).__name__, params, self.filename, self.linenumber)

    def chain(self, next: "Node | None") -> None:
        """
        This is called with the Node node that should be followed after
        executing this node, and all nodes that this node
        executes. (For example, if this node is a block label, the
        next is the node that should be executed after all nodes in
        the block.)
        """

        self.next = next

    def get_repr_params(self) -> str:
        """
        Returns a string representation of the parameters of this node.
        This is used in the __repr__ method to provide additional information
        about the node.
        """
        return ""

    def restart(self) -> None:
        self.done = False

    #######################

    def ready(self) -> bool:
        """
        Returns True if this node is ready to execute, or False otherwise.
        """
        return True

    def start(self) -> NodeState:
        """
        Called once when the node starts execution.

        This is expected to return a state, or None to advance to the next
        node.
        """
        return 0

    def execute(self, state: NodeState, t: float) -> NodeState:
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

    def after_until(self) -> None:
        """
        Called after an Until node has finished executing.
        This is used to end any function that was started by this node.
        """
        pass

    def cleanup_after_error(self) -> None:
        """
        Called if an exception is raised during the execution of this node.
        This can be used to clean up any state that was set by this node.
        """
        pass


class Block(Node):
    __slots__ = ("block", "name")

    def __init__(self, loc: NodeLocation, block: list[Node], name: str = ""):
        Node.__init__(self, loc)
        self.block = block
        self.name = name
        self.restart()

    def chain(self, next):
        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            super().chain(next)

    def restart(self) -> None:
        if self.block:
            for node in self.block:
                node.restart()
            self.done = False
        else:
            self.done = True

    def execute(self, state, t):
        if not self.block:
            next_node(self.next)
            return None

        next_node(self.block[0])
        return None


class TestCase(Block):
    __slots__ = ("description", "skip", "only", "parent")

    def __init__(
        self,
        loc: NodeLocation,
        name: str,
        block: list[Node],
        description: str = "",
        skip: bool = False,
        only: bool = False,
        parent: "TestCase | None" = None,
    ):
        super().__init__(loc, block, name)
        self.name = name
        self.block = block
        self.description = description
        self.skip = skip
        self.only = only
        self.parent = parent

        if self.skip and self.only:
            raise ValueError(f"Test case '{self.name}' cannot have both 'skip' and 'only' set to True.")

    def __hash__(self):
        return hash(self.name)

    def get_repr_params(self) -> str:
        return f"name={self.name!r}"


class TestHook(Block):
    __slots__ = "depth"

    def __init__(
        self,
        loc: NodeLocation,
        name: str,
        block: list[Node],
        depth: int = 0,
    ):
        super().__init__(loc, block, name)
        self.depth = depth


class TestSuite(TestCase):
    """
    Most of the logic is handled in renpy.test.testexecution.
    """

    __slots__ = (
        "subtests",
        "subtest_index",
        "hooks",
        "after",
        "after_each_case",
        "after_each_suite",
        "before",
        "before_each_case",
        "before_each_suite",
    )

    def __init__(
        self,
        loc: NodeLocation,
        name: str,
        description: str = "",
        skip: bool = False,
        only: bool = False,
        parent: "TestCase | None" = None,
        subtests: list[TestCase] | None = None,
        after: TestHook | None = None,
        after_each_case: TestHook | None = None,
        after_each_suite: TestHook | None = None,
        before: TestHook | None = None,
        before_each_case: TestHook | None = None,
        before_each_suite: TestHook | None = None,
    ):
        super().__init__(loc, name, [], description, skip, only, parent)

        self.subtest_index = -1

        self.subtests = subtests if subtests is not None else []
        for subtest in self.subtests:
            subtest.parent = self

        self.hooks: list[TestHook] = []
        for hook in [after, after_each_case, after_each_suite, before, before_each_case, before_each_suite]:
            if hook is not None:
                self.hooks.append(hook)

        self.after = after
        self.after_each_case = after_each_case
        self.after_each_suite = after_each_suite
        self.before = before
        self.before_each_case = before_each_case
        self.before_each_suite = before_each_suite

    def chain(self, next: Node | None) -> None:
        for block in self.hooks:
            block.chain(None)

        for subtest in self.subtests:
            subtest.chain(None)

    def add(self, child: TestCase) -> None:
        self.subtests.append(child)

    @property
    def current_test(self) -> TestCase | None:
        if 0 <= self.subtest_index < len(self.subtests):
            return self.subtests[self.subtest_index]
        return None

    @property
    def num_tests(self) -> int:
        return len(self.subtests)

    @property
    def is_all_tests_completed(self) -> bool:
        return self.subtest_index >= len(self.subtests)

    def advance(self) -> Block | None:
        """
        Advances the test suite to the next block.

        NOTE: Must be run at the start of a test suite run to correctly set
        the testcase_index to 0.
        """
        self.subtest_index += 1

    def get_hook(self, hook_type: HookType) -> TestHook | None:
        """Returns the hook of the given type, or None if no such hook exists."""
        match hook_type:
            case HookType.AFTER:
                return self.after
            case HookType.AFTER_EACH_CASE:
                return self.after_each_case
            case HookType.AFTER_EACH_SUITE:
                return self.after_each_suite
            case HookType.BEFORE:
                return self.before
            case HookType.BEFORE_EACH_SUITE:
                return self.before_each_suite
            case HookType.BEFORE_EACH_CASE:
                return self.before_each_case
            case _:
                raise ValueError(f"Invalid hook tag: {self.hook_type}")


class Condition(Node):
    """
    A base class for conditions that can be used in test scripts.

    Conditions should NOT execute any actions or change the state of the game.
    They should only check if a certain condition is met.
    """

    def execute(self, state: NodeState, t: float) -> NodeState:
        raise RenpyTestException("Conditions should not be executed directly. Use `ready()` instead.")


################################################################################
# Selectors
class Selector(Condition):
    """
    Base class for selectors. Selectors find a focusable or displayable
    item on the screen.
    """

    __slots__ = ("element", "wait_for_focus")

    def __init__(self, loc, wait_for_focus):
        super().__init__(loc)

        self.wait_for_focus: bool = wait_for_focus
        self.element: Displayable | Focus | None = None

    def ready(self) -> bool:
        self.element = self.get_element()
        focused = self.is_focused() or not self.wait_for_focus
        return self.element is not None and focused

    def get_element(self) -> Displayable | Focus | None:
        """
        Returns the element that this selector is looking for.
        If no element is found, returns None.
        """
        raise NotImplementedError("get_element() must be implemented in subclasses of Selector.")

    def element_not_found_during_perform(self) -> None:
        """
        Called when the element is not found during perform.
        This can be overridden to handle cases where the element is not found.
        """
        raise SelectorException("Element was not found.")

    def is_focused(self) -> bool:
        """
        Checks if the element or its children are focused.
        """
        displayable = None
        if isinstance(self.element, Focus):
            displayable = self.element.widget
        elif isinstance(self.element, Displayable):
            displayable = self.element

        if displayable is None:
            return False

        child_stack: list[Displayable] = [displayable]
        while child_stack:
            child = child_stack.pop()

            if child is renpy.game.context().scene_lists.focused:
                return True

            if isinstance(child, renpy.display.layout.Container):
                child_stack.extend(child.children)

        return False


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
        wait_for_focus: bool = False,
    ):
        super(DisplayableSelector, self).__init__(loc, wait_for_focus)
        self.screen = screen
        self.id = id
        self.layer = layer

        if self.screen is None and self.id is None:
            raise ValueError("Specify screen and/or id.")

    def ready(self) -> bool:
        ## Needs to be checked here and not in __init__ since screens are not be defined yet.
        if self.screen is not None and not renpy.exports.has_screen(self.screen):
            raise ValueError(f"The screen {self.screen!r} does not exist.")

        return super().ready()

    def get_element(self) -> Displayable | None:
        if self.screen and self.id is None:
            rv = renpy.exports.get_screen(self.screen, self.layer)
        else:
            # rv = renpy.exports.get_displayable(self.screen, self.id, self.layer)
            rv = self.get_displayable()

        return rv

    def get_displayable(self) -> Displayable | None:
        """
        Returns the displayable that this selector is looking for.
        If no displayable is found, returns None.

        renpy.exports.get_displayable(screen, id, layer) is supposed to do this, but it sucks
        """
        ## NOTE: Move to renpy.exports.get_displayable() eventually?

        ctx: renpy.execution.Context = renpy.game.context()
        for layer, sles in ctx.scene_lists.layers.items():
            layer: str
            sles: list[renpy.display.scenelists.SceneListEntry]

            if self.layer and self.layer != layer:
                continue

            for sle in sles:
                if not isinstance(sle.displayable, renpy.display.screen.ScreenDisplayable):
                    continue

                if self.screen and sle.name != self.screen:
                    continue

                rv = sle.displayable.widgets.get(self.id, None)

                if rv is not None:
                    return rv

        return None

    def element_not_found_during_perform(self) -> None:
        if self.screen or self.id:
            raise SelectorException("The displayable with screen {self.screen!r} and id {self.id!r} was not found")

        raise SelectorException("No displayable was specified.")

    def __str__(self) -> str:
        parts = []
        if self.screen:
            parts.append(f"screen={self.screen!r}")
        if self.id:
            parts.append(f"id={self.id!r}")
        if self.layer:
            parts.append(f"layer={self.layer!r}")
        if self.wait_for_focus:
            parts.append("wait_for_focus=True")
        return f"<{type(self).__name__} {' '.join(parts)}>"


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

    def __init__(self, loc: NodeLocation, pattern: str, wait_for_focus: bool = False):
        super(TextSelector, self).__init__(loc, wait_for_focus)
        self.pattern = pattern

    def get_repr_params(self) -> str:
        return f"pattern={self.pattern!r}"

    def get_element(self) -> Focus | None:
        rv = renpy.test.testfocus.find_focus(self.pattern)
        return rv

    def element_not_found_during_perform(self) -> None:
        if self.pattern:
            raise SelectorException(f"The given pattern {self.pattern!r} was not resolved to a target")


################################################################################
# Selector-driven nodes
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

    def ready(self) -> bool:
        if self.always:
            return True

        if self.selector is not None:
            return self.selector.ready()

        return True

    def execute(self, state: NodeState, t: float) -> NodeState:
        if renpy.display.interface.trans_pause or renpy.display.interface.ongoing_transition:
            if t >= _test.transition_timeout:
                ## End the transition and wait for the next frame.
                ## We need to suppress_transition in the core loop
                old_less_updates = renpy.game.less_updates
                renpy.game.less_updates = True
                return ("skipped_transition", old_less_updates, state)
            return state

        if isinstance(state, tuple) and len(state) == 3 and state[0] == "skipped_transition":
            renpy.game.less_updates = state[1]
            state = state[-1]

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

        if self.selector is None:
            f = None
        else:
            f = self.selector.element
            if f is None and not self.always:
                self.selector.element_not_found_during_perform()

        x, y = renpy.test.testfocus.find_position(f, position)

        return x, y

    def perform(self, x: int, y: int, state: NodeState, t: float) -> NodeState | None:
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

    def ready(self):
        f = renpy.test.testfocus.find_focus(self.pattern)
        return f is not None

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


class Drag(Node):
    __slots__ = ("points", "pattern", "button", "steps")

    def __init__(self, loc: NodeLocation, points: list[tuple[int, int]]):
        super(Drag, self).__init__(loc)
        self.points = points

        self.pattern: str | None = None
        self.button: int = 1
        self.steps: int = 10

    def ready(self):
        if self.pattern is None:
            return True

        f = renpy.test.testfocus.find_focus(self.pattern)

        if f is not None:
            return True
        else:
            return False

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

            # NOTE: Might be worth replacing with collections.deque if the number of points is large
            interpoints: list[tuple[int, int]] = []

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

        key = self.text[state]
        renpy.test.testkey.down(self, key)
        renpy.test.testkey.up(self, key)

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

    def ready(self):
        action = renpy.python.py_eval(self.expr)
        return renpy.display.behavior.is_sensitive(action)

    def start(self):
        renpy.test.testexecution.action = renpy.python.py_eval(self.expr)
        return True

    def execute(self, state, t):
        if renpy.test.testexecution.action:
            return state
        else:
            next_node(self.next)
            return None


class Pause(Node):
    __slots__ = "expr"

    def __init__(self, loc: NodeLocation, expr: str):
        super(Pause, self).__init__(loc)
        self.expr = expr

    def get_repr_params(self):
        return f"{self.expr}"

    def start(self):
        return float(renpy.python.py_eval(self.expr)), 0

    def execute(self, state, t):
        delay, _ = state
        if t < delay:
            ## Avoids timeout by appending t to the state
            return delay, t
        else:
            next_node(self.next)
            return None


class Label(Condition):
    __slots__ = "name"

    def __init__(self, loc: NodeLocation, name: str):
        super(Label, self).__init__(loc)
        self.name = name

    def ready(self):
        return self.name in renpy.test.testexecution.reached_labels

    def get_repr_params(self):
        return f"{self.name}"


class Eval(Condition):
    __slots__ = "expr"

    def __init__(self, loc: NodeLocation, expr):
        super(Eval, self).__init__(loc)
        self.expr = expr

    def ready(self):
        return bool(renpy.python.py_eval(self.expr))


class RepeatCounter(Condition):
    __slots__ = ("initial_value", "value")

    def __init__(self, loc: NodeLocation, value: int):
        super(RepeatCounter, self).__init__(loc)
        self.initial_value = value
        self.restart()

    def restart(self) -> None:
        self.value = self.initial_value
        return super().restart()

    def ready(self):
        self.value -= 1
        return self.value == 0


class Pass(Node):
    pass


class Advance(Node):
    """
    Advances the said dialogue by one line.
    """

    last_event: str = ""
    last_kwargs: dict = {}
    began_newline: bool = False

    @staticmethod
    def character_callback(event, **kwargs) -> None:
        if event == "begin":
            Advance.began_newline = True
        Advance.last_event = event
        Advance.last_kwargs = kwargs

    def ready(self):
        if Advance.character_callback not in renpy.config.all_character_callbacks:
            renpy.config.all_character_callbacks.append(Advance.character_callback)

        return True

    def start(self):
        Advance.began_newline = False
        return Advance.last_event

    def execute(self, state, t):
        if Advance.began_newline:
            next_node(self.next)
            return None

        renpy.test.testkey.queue_keysym(self, "dismiss")
        return Advance.last_event


class Skip(Node):
    """
    Trigger the skip key
    """

    __slots__ = ("fast",)

    def __init__(self, loc: NodeLocation, fast: bool = False):
        super(Skip, self).__init__(loc)
        self.fast = fast

    def start(self):
        if not renpy.config.allow_skipping:
            return None

        if renpy.store.main_menu:
            return None

        return True

    def execute(self, state, t):
        was_skipping = renpy.config.skipping is not None

        if renpy.exports.context()._menu:  # type: ignore
            if self.fast:
                renpy.exports.jump("_return_fast_skipping")
            else:
                renpy.exports.jump("_return_skipping")
        else:
            if self.fast:
                renpy.config.skipping = "fast"
            else:
                renpy.config.skipping = "slow"

            if not was_skipping:
                renpy.exports.restart_interaction()

        next_node(self.next)
        return None

    def after_until(self) -> None:
        renpy.config.skipping = None


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
    __slots__ = ("left", "right", "left_ready", "right_ready", "left_state", "right_state")

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

    def ready(self):
        self.left_ready = self.left.ready()
        self.right_ready = self.right.ready()
        return self.left_ready and self.right_ready

    def state(self) -> bool | None:
        if (self.left_state is None) and (self.right_state is None):
            return None
        return True

    def execute(self, state, t):
        ## TODO: Remove?
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


class Or(Binary):
    __slots__ = ()

    def ready(self):
        self.left_ready = self.left.ready()
        self.right_ready = self.right.ready()
        return self.left_ready or self.right_ready

    def state(self) -> bool | None:
        if (self.left_state is None) or (self.right_state is None):
            return None
        return True

    def execute(self, state, t):
        ## TODO: Remove?
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

    def __init__(self, loc: NodeLocation, left: Node, right: Condition, timeout: float | None = float("NaN")):
        Node.__init__(self, loc)
        self.left = left
        self.right = right
        self.timeout = timeout

    def restart(self):
        self.left.restart()
        self.right.restart()
        super().restart()

    def ready(self):
        return self.left.ready() or self.right.ready()

    def start(self):
        if self.timeout and math.isnan(self.timeout):
            self.timeout = _test.timeout

        return (None, 0, False)

    def execute(self, state, t):
        if self.timeout is not None and t > self.timeout:
            msg = f"Until Statement timed out after {self.timeout} seconds."
            raise RenpyTestTimeoutError(msg)

        if self.right.ready():
            self.left.after_until()
            next_node(self.next)
            return None

        ## The right hand side is not ready, so we execute the left hand side.
        child_state, start_time, has_started = state

        if not has_started and self.left.ready():
            child_state = self.left.start()
            start_time = t
            has_started = True

        if has_started:
            child_state = self.left.execute(child_state, t - start_time)

        next_node(self)
        if child_state is None:
            return (None, 0, False)

        return child_state, start_time, has_started

    def cleanup_after_error(self) -> None:
        return self.left.after_until()


class Repeat(Until):
    """
    Executes `left` for `count` times.
    """

    def __init__(self, loc: NodeLocation, left: Node, count: int, timeout: float | None = float("NaN")):
        ## Multiplied by 2 to account for Until.execute() calling ready twice per iteration.
        right = RepeatCounter(loc, count * 2)
        super(Repeat, self).__init__(loc, left, right, timeout)

    def ready(self):
        return self.left.ready()


class If(Node):
    """
    If `condition` is ready, runs the block. Otherwise, goes to the next
    statement.
    """

    __slots__ = ("entries",)

    def __init__(self, loc: NodeLocation, entries: list[tuple[Condition, "Block"]]):
        Node.__init__(self, loc)

        self.entries = entries  # List of (condition, block) tuples.

    def chain(self, next):
        self.next = next

        for _condition, block in self.entries:
            block.chain(next)

    def execute(self, state, t):
        for condition, block in self.entries:
            if condition.ready():
                next_node(block.block[0])
                return None

        next_node(self.next)
        return None


class Python(Node):
    __slots__ = ("code", "hide")

    def __init__(self, loc: NodeLocation, code: renpy.ast.PyCode, hide: bool = False):
        Node.__init__(self, loc)
        self.code = code
        self.hide = hide

    def __call__(self):
        renpy.python.py_exec_bytecode(self.code.bytecode, self.hide)

    def start(self):
        renpy.test.testexecution.set_action(self)
        return True

    def execute(self, state, t):
        if renpy.test.testexecution.action:
            return state
        else:
            next_node(self.next)
            return None


class Assert(Node):
    """
    An assertion that checks if a condition is met.
    If the condition is not met, an AssertError is raised.

    `condition`
        A `Condition` instance that should be ready for the assertion to pass.
    `timeout`
        The maximum delay to wait for the condition to be ready.
    """

    __slots__ = ("condition", "timeout", "failed")

    def __init__(self, loc: NodeLocation, condition: Condition, timeout: float = 0.0):
        Node.__init__(self, loc)
        self.condition = condition
        self.timeout = timeout
        self.failed = False

    def execute(self, state, t):
        """
        Executes the assertion. If the condition is not ready, it waits up to
        `self.timeout` seconds.
        """
        if not self.condition.ready():
            if t < self.timeout:
                return state

            self.failed = True

        renpy.test.testreporter.reporter.log_assert(self)
        next_node(self.next)
        return None


################################################################################
# Control structures.


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

    renpy.test.testexecution.set_next_execution_node(node)
