# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

import itertools
from typing import Any
import glob
import os

import renpy
from renpy.display.focus import Focus
from renpy.display.displayable import Displayable
from renpy.test.testmouse import click_mouse, move_mouse, scroll_mouse
from renpy.test.testsettings import _test
from renpy.test.types import (
    HookType,
    NodeLocation,
    NodeState,
    Position,
    RenpyTestException,
    RenpyTestScreenshotError,
    RenpyTestTimeoutError,
)


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

    def cleanup_after_error(self, state: NodeState) -> None:
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

            for a, b in zip(self.block, self.block[1:]):
                a.chain(b)

            self.block[-1].chain(next)
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


class BaseTestBlock(Block):
    """
    A base class for TestCase, TestSuite, and TestHook.
    """

    __slots__ = ("parent", "xfail_expr")

    def __init__(
        self,
        loc: NodeLocation,
        block: list[Node],
        name: str,
        parent: "TestSuite | None" = None,
        xfail_expr: str = "False",
    ):
        self.parent = parent
        self.xfail_expr = xfail_expr
        super().__init__(loc, block, name)

    def __hash__(self):
        return hash(self.full_path)
        # return hash(self.parameterized_id)

    def get_repr_params(self) -> str:
        return f"name={self.current_full_parameterized_path!r}"

    def get_parameterized_name(self, index: int | None = None) -> str:
        """
        Returns the name with the parameters for the given index shown.
        If index is None, uses the current parameters.
        """
        raise NotImplementedError

    @property
    def xfail(self) -> bool:
        return bool(scoped_eval(self.xfail_expr))

    @property
    def current_parameters(self) -> dict[str, Any]:
        """The current parameters for this test block, or an empty dict if there are none."""
        raise NotImplementedError

    @property
    def full_path(self) -> str:
        """The full hierarchical path using `.` to separate testsuites and `::` to separate testcases."""
        if self.parent:
            return f"{self.parent.full_path}::{self.name}"
        return self.name

    @property
    def current_parameterized_name(self) -> str:
        """The name with current parameters shown."""
        return self.get_parameterized_name(None)

    @property
    def current_full_parameterized_path(self) -> str:
        """The full hierarchical path with current parameters shown."""
        if self.parent:
            return f"{self.parent.current_full_parameterized_path}::{self.current_parameterized_name}"
        return self.current_parameterized_name


class TestHook(BaseTestBlock):
    __slots__ = ("depth", "call_count")

    def __init__(
        self,
        loc: NodeLocation,
        block: list[Node],
        name: str,
        parent: "TestSuite | None" = None,
        xfail_expr: str = "False",
        depth: int = 0,
    ):
        self.depth = depth
        self.call_count = 0
        super().__init__(loc, block, name, parent, xfail_expr)

    def increment_call_count(self) -> None:
        self.call_count += 1

    def __hash__(self):
        return hash(self.current_full_parameterized_path)

    def get_parameterized_name(self, index=None):
        if index is None:
            index = self.call_count
        return f"{self.name}({index})"


class TestCase(BaseTestBlock):
    __slots__ = ("description", "enabled", "only", "parameters", "parameter_index")

    def __init__(
        self,
        loc: NodeLocation,
        block: list[Node],
        name: str,
        parent: "TestSuite | None" = None,
        xfail_expr: str = "False",
        description: str = "",
        enabled: bool = True,
        only: bool = False,
        parameters: list[list[dict[str, Any]]] | None = None,
    ):
        self.description = description
        self.enabled = enabled
        self.only = only
        self.parameters = self.generate_parameter_combinations(parameters)
        self.parameter_index = 0
        super().__init__(loc, block, name, parent, xfail_expr)

        if not self.enabled and self.only:
            raise ValueError(f"Test case '{self.name}' must be enabled before setting 'only' to True.")

    def restart(self) -> None:
        self.parameter_index = 0
        return super().restart()

    def generate_parameter_combinations(self, parameters: list[list[dict[str, Any]]] | None) -> list[dict[str, Any]]:
        if parameters is None:
            return []

        if len(parameters) == 1:
            return parameters[0]

        # Cartesian product of parameter lists.
        rv = []
        product = itertools.product(*parameters)
        for param_tuple in product:
            merged_dict = {}
            for d in param_tuple:
                merged_dict.update(d)
            rv.append(merged_dict)

        return rv

    def advance_to_next_parameter_set(self):
        """
        Advances the test case to the next parameter set.

        Returns True if there are no more parameter sets to advance to.
        """
        self.parameter_index += 1

    def get_parameterized_name(self, index=None):
        if not self.parameters:
            return self.name

        if index is None:
            index = self.parameter_index

        # if index >= len(self.parameters):
        #     return f"{self.name}(<no more parameters>)"

        params = self.parameters[index]
        param_str = ", ".join(f"{k}={v!r}" for k, v in params.items())
        return f"{self.name}({param_str})"

    @property
    def current_parameters(self) -> dict[str, Any]:
        if not self.parameters:
            return {}
        return self.parameters[self.parameter_index]

    @property
    def has_all_parameters_been_processed(self) -> bool:
        return self.parameter_index >= len(self.parameters)

    def has_testcase(self) -> bool:
        """
        Returns True if there is at least one test case defined.
        """

        return True


class TestSuite(TestCase):
    """
    Most of the logic is handled in renpy.test.testexecution.
    """

    __slots__ = (
        "subtests",
        "subtest_index",
        "setup",
        "before_testsuite",
        "before_testcase",
        "after_testcase",
        "after_testsuite",
        "teardown",
    )

    def __init__(
        self,
        loc: NodeLocation,
        name: str,
        parent: "TestSuite | None" = None,
        xfail_expr: str = "False",
        description: str = "",
        enabled: bool = True,
        only: bool = False,
        parameters: list[list[dict[str, Any]]] | None = None,
        subtests: list[TestCase] | None = None,
        setup: TestHook | None = None,
        before_testsuite: TestHook | None = None,
        before_testcase: TestHook | None = None,
        after_testsuite: TestHook | None = None,
        after_testcase: TestHook | None = None,
        teardown: TestHook | None = None,
    ):
        self.subtest_index = 0

        self.subtests: list[TestCase] = []
        self.setup = setup
        self.before_testsuite = before_testsuite
        self.before_testcase = before_testcase
        self.after_testcase = after_testcase
        self.after_testsuite = after_testsuite
        self.teardown = teardown
        super().__init__(loc, [], name, parent, xfail_expr, description, enabled, only, parameters)

        if subtests is not None:
            for subtest in subtests:
                self.add(subtest)

        for hook in self.hooks:
            hook.parent = self

    def chain(self, next: Node | None) -> None:
        for block in self.hooks:
            block.chain(None)

        for subtest in self.subtests:
            subtest.chain(None)

    def add(self, child: TestCase) -> None:
        child.parent = self
        self.subtests.append(child)

    def restart(self) -> None:
        self.parameter_index = 0
        self.subtest_index = 0
        for subtest in self.subtests:
            subtest.restart()
        for hook in self.hooks:
            hook.restart()
        return super().restart()

    def advance_to_next_subtest(self) -> None:
        """
        Advances the test suite to the next block.
        """
        test = self.current_test
        if test is None:
            raise RenpyTestException("No current test to advance to.")

        if test.enabled:
            test.advance_to_next_parameter_set()
            if test.has_all_parameters_been_processed:
                test.parameter_index = 0
                self.subtest_index += 1
        else:
            self.subtest_index += 1

    def advance_to_next_parameter_set(self):
        """
        Advances the test case to the next parameter set.

        Returns True if there are no more parameter sets to advance to.
        """

        super().advance_to_next_parameter_set()
        self.subtest_index = 0

    def get_hook(self, hook_type: HookType) -> TestHook | None:
        """Returns the hook of the given type, or None if no such hook exists."""
        match hook_type:
            case HookType.SETUP:
                return self.setup
            case HookType.BEFORE_TESTSUITE:
                return self.before_testsuite
            case HookType.BEFORE_TESTCASE:
                return self.before_testcase
            case HookType.AFTER_TESTCASE:
                return self.after_testcase
            case HookType.AFTER_TESTSUITE:
                return self.after_testsuite
            case HookType.TEARDOWN:
                return self.teardown

    @property
    def hooks(self) -> list[TestHook]:
        rv: list[TestHook] = []
        for hook in [
            self.setup,
            self.before_testsuite,
            self.before_testcase,
            self.after_testcase,
            self.after_testsuite,
            self.teardown,
        ]:
            if hook is not None:
                rv.append(hook)
        return rv

    @property
    def current_test(self) -> TestCase | None:
        if 0 <= self.subtest_index < len(self.subtests):
            return self.subtests[self.subtest_index]
        return None

    @property
    def num_tests(self) -> int:
        return len(self.subtests)

    @property
    def has_completed_all_subtests(self) -> bool:
        return self.subtest_index >= len(self.subtests)

    @property
    def full_path(self) -> str:
        if self.parent:
            return f"{self.parent.full_path}.{self.name}"
        return self.name

    @property
    def current_full_parameterized_path(self) -> str:
        if self.parent:
            return f"{self.parent.current_full_parameterized_path}.{self.current_parameterized_name}"
        return self.current_parameterized_name

    def has_testcase(self) -> bool:
        """
        Returns True if there is at least one test case defined.
        """

        if self.subtests is None:
            return False

        return any(subtest.has_testcase() for subtest in self.subtests)


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
        if self.screen is not None:
            if not renpy.exports.has_screen(scoped_eval(self.screen)):
                raise ValueError(f"The screen {self.screen!r} does not exist.")

        return super().ready()

    def get_element(self) -> Displayable | None:
        if self.screen and self.id is None:
            layer = None if self.layer is None else scoped_eval(self.layer)
            screen = None if self.screen is None else scoped_eval(self.screen)
            rv = renpy.exports.get_screen(screen, layer)
        else:
            rv = self.get_displayable()

        return rv

    def get_displayable(self) -> Displayable | None:
        """
        Returns the displayable that this selector is looking for.
        If no displayable is found, returns None.

        renpy.exports.get_displayable(screen, id, layer) is supposed to do this, but it sucks
        """
        ## NOTE: Move to renpy.exports.get_displayable() eventually?

        layer = None if self.layer is None else scoped_eval(self.layer)
        screen = None if self.screen is None else scoped_eval(self.screen)
        id = None if self.id is None else scoped_eval(self.id)

        ctx: renpy.execution.Context = renpy.game.context()
        for context_layer, sles in ctx.scene_lists.layers.items():
            context_layer: str
            sles: list[renpy.display.scenelists.SceneListEntry]

            if layer and layer != context_layer:
                continue

            for sle in sles:
                if not isinstance(sle.displayable, renpy.display.screen.ScreenDisplayable):
                    continue

                if screen and sle.name != screen:
                    continue

                rv = sle.displayable.widgets.get(id, None)

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

    `raw`
        If True, the raw text is used for matching before translation and
        substitution. If False, the processed text is used.
    """

    __slots__ = ("pattern", "raw")

    def __init__(
        self,
        loc: NodeLocation,
        wait_for_focus: bool = False,
        pattern: str = "",
        raw: bool = False,
    ):
        super(TextSelector, self).__init__(loc, wait_for_focus)
        self.pattern = pattern
        self.raw = raw

    def get_repr_params(self) -> str:
        return f"pattern={self.pattern!r}, raw={self.raw}"

    def get_element(self) -> Focus | None:
        rv = renpy.test.testfocus.find_focus(self.pattern, self.raw)
        return rv

    def element_not_found_during_perform(self) -> None:
        if self.pattern:
            raise SelectorException(f"The given pattern {self.pattern!r} was not resolved to a target")


################################################################################
# Command statements
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
        position: str | None = None,
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
        position: Position | tuple[None, None] = (None, None)
        if self.position is not None:
            position = scoped_eval(self.position)
            if not (isinstance(position, tuple) and len(position) == 2):
                raise ValueError("Position expression must evaluate to a tuple of (x, y).")

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


class Scroll(SelectorDrivenNode):
    amount: int = 1

    def perform(self, x, y, state, t):
        if self.selector is not None:
            element = self.selector.element

            if isinstance(element, renpy.display.focus.Focus):
                element = element.widget

            if isinstance(element, renpy.display.behavior.Bar):
                adj = element.adjustment

                if adj.value == adj.range:
                    new = 0
                else:
                    new = adj.value + (adj.page * self.amount)

                new = max(0, min(new, adj.range))
                adj.change(new)
                return

        scroll_mouse(-self.amount, x, y)


class Drag(Node):
    __slots__ = ("start_point", "end_point", "button", "steps")

    def __init__(
        self,
        loc: NodeLocation,
        start_point: SelectorDrivenNode,
        end_point: SelectorDrivenNode,
        button: int = 1,
        steps: int = 10,
    ):
        super(Drag, self).__init__(loc)
        self.start_point = start_point
        self.end_point = end_point
        self.button = button
        self.steps = steps

    def ready(self):
        return self.start_point.ready() and self.end_point.ready()

    def start(self):
        start_pos = self.start_point.get_position()
        end_pos = self.end_point.get_position()

        return (start_pos, end_pos, 0)  # (x, y, step)

    def execute(self, state, t):
        if renpy.display.interface.trans_pause:
            return state

        (start_pos, end_pos, step) = state
        x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * step / self.steps)
        y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * step / self.steps)

        renpy.test.testmouse.move_mouse(x, y)

        if step == 0:
            renpy.test.testmouse.press_mouse(self.button)

        elif step >= self.steps:
            renpy.test.testmouse.release_mouse(self.button)
            next_node(self.next)
            return None

        return (start_pos, end_pos, step + 1)


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

    def __init__(self, loc: NodeLocation, expr: str):
        super(Action, self).__init__(loc)
        self.expr = expr

    def ready(self):
        action = scoped_eval(self.expr)
        return renpy.display.behavior.is_sensitive(action)

    def execute(self, state, t):
        action = scoped_eval(self.expr)
        renpy.display.behavior.run(action)
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
        return float(scoped_eval(self.expr)), 0

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
        return bool(scoped_eval(self.expr))


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
# Boolean operators


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
        Returns the state of this binary operator.
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
    """

    __slots__ = ("left", "right", "timeout")

    def __init__(self, loc: NodeLocation, left: Node, right: Condition, timeout: str = "None"):
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
        old_timeout = _test.timeout
        timeout = scoped_eval(self.timeout)
        if isinstance(timeout, (int, float)):
            _test.timeout = timeout
        elif timeout is not None:
            raise ValueError("Timeout must be a float or None.")

        child_state = None
        start_time = 0
        has_started = False

        return (old_timeout, child_state, start_time, has_started)

    def execute(self, state: tuple[float | None, Any, float, bool], t):
        old_timeout, child_state, start_time, has_started = state

        if t > _test.timeout:
            msg = f"Until Statement timed out after {_test.timeout} seconds."
            raise RenpyTestTimeoutError(msg)

        if self.right.ready():
            self.cleanup_after_error(state)
            next_node(self.next)
            return None

        ## The right hand side is not ready, so we execute the left hand side.
        if not has_started and self.left.ready():
            child_state = self.left.start()
            start_time = t
            has_started = True

        if has_started:
            child_state = self.left.execute(child_state, t - start_time)

        next_node(self)
        if child_state is None:
            start_time = 0
            has_started = False

        return old_timeout, child_state, start_time, has_started

    def cleanup_after_error(self, state) -> None:
        _test.timeout = state[0]
        self.left.after_until()


class Repeat(Until):
    """
    Executes `left` for `count` times.
    """

    def __init__(self, loc: NodeLocation, left: Node, count: int, timeout: str = "None"):
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
    __slots__ = ("source", "hide")

    def __init__(self, loc: NodeLocation, source: str, hide: bool = False):
        Node.__init__(self, loc)
        self.source = source
        self.hide = hide

    def execute(self, state, t):
        scoped_exec(self.source, self.hide)

        next_node(self.next)
        return None


class Assert(Node):
    """
    An assertion that checks if a condition is met.
    If the condition is not met, a RenpyTestAssertionError is raised.

    `condition`
        A `Condition` instance that should be ready for the assertion to pass.
    `timeout`
        The maximum delay to wait for the condition to be ready.
    `xfail_expr`
        If True, the test is expected to fail. If the condition is not met,
        the test will be marked as xfailed instead of failed.
    """

    __slots__ = ("condition", "timeout", "xfail_expr", "is_assertion_true")

    def __init__(self, loc: NodeLocation, condition: Condition, timeout: str = "None", xfail_expr: str = "False"):
        Node.__init__(self, loc)
        self.condition = condition
        self.timeout = timeout
        self.xfail_expr = xfail_expr
        self.is_assertion_true = False  # Whether the assertion was true or not

    def start(self):
        old_timeout = _test.timeout
        timeout = scoped_eval(self.timeout)
        if isinstance(timeout, (int, float)):
            _test.timeout = timeout
        elif timeout is None:
            _test.timeout = 0
        else:
            raise ValueError("Timeout must be a float or None.")

        return old_timeout

    def execute(self, state, t):
        """
        Executes the assertion. If the condition is not ready, it waits up to
        `self.timeout` seconds.
        """
        if (not self.condition.ready()) ^ self.xfail:
            if t < _test.timeout:
                return state

        self.is_assertion_true = self.condition.ready()
        renpy.test.testreporter.reporter.log_assert(self)
        self.cleanup_after_error(state)
        next_node(self.next)
        return None

    def cleanup_after_error(self, state) -> None:
        _test.timeout = state

    @property
    def xfail(self) -> bool:
        return bool(scoped_eval(self.xfail_expr))


class Screenshot(Node):
    __slots__ = ("filename_expr", "max_pixel_difference", "crop")

    def __init__(
        self,
        loc: NodeLocation,
        filename: str,
        max_pixel_difference: str | None = None,
        crop: str | None = None,
    ):
        self.max_pixel_difference = max_pixel_difference
        self.crop = crop
        self.filename_expr = filename  # Note: self.filename refers to the Node attribute.
        super().__init__(loc)

    def start(self):
        filename = scoped_eval(self.filename_expr)
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string.")

        filename = filename.replace("\\", "/")
        filename = filename.lstrip("/")
        filename = os.path.join(renpy.config.basedir, _test.screenshot_directory, filename)
        filename = os.path.normpath(filename)

        base_filename, ext = os.path.splitext(filename)
        if ext.lower() != ".png":
            ext = ".png"
            filename = base_filename + ext

        return filename

    def execute(self, state, t):
        filename = state

        img: renpy.pygame.Surface | None = None
        old_img: renpy.pygame.Surface | None = None
        diff: renpy.pygame.Surface | None = None

        try:
            img = renpy.display.draw.screenshot(renpy.game.interface.surftree)

            if self.crop:
                # img = renpy.display.scale.smoothscale(img, (renpy.config.screen_width, renpy.config.screen_height))
                img = img.subsurface(scoped_eval(self.crop))

            base_filename, ext = os.path.splitext(filename)
            ref_img_path = self.get_reference_image_path(filename)
            new_fname = f"{base_filename}.new{ext}"
            diff_fname = f"{base_filename}.diff{ext}"

            if _test.overwrite_screenshots and ref_img_path is not None:
                os.remove(ref_img_path)
                ref_img_path = None

            if ref_img_path is None:
                if _test.vc_revision:
                    fname = f"{base_filename}@{_test.vc_revision}{ext}"
                else:
                    fname = filename
                self.save_image(img, fname)

                next_node(self.next)
                return None

            old_img = renpy.pygame.image.load(ref_img_path)  # type: ignore

            if img.get_size() != old_img.get_size():
                raise RenpyTestScreenshotError(f"{filename} (size mismatch: {img.get_size()} != {old_img.get_size()})")

            if img.get_bitsize() != old_img.get_bitsize():
                raise RenpyTestScreenshotError(
                    f"{filename} (bit size mismatch: {img.get_bitsize()} != {old_img.get_bitsize()})"
                )

            diff = renpy.pygame.Surface(img.get_size(), 0, img)

            diff_count = renpy.pygame.transform._diff(diff, img, old_img, (0, 0, 0, 255), (255, 255, 255, 255))

            max_pixel_difference = 0
            if self.max_pixel_difference is not None:
                max_pixel_difference = scoped_eval(self.max_pixel_difference)
                if not isinstance(max_pixel_difference, (int, float)):
                    raise ValueError("max_pixel_difference must be an int or float.")
                if isinstance(max_pixel_difference, float) and 0 < max_pixel_difference < 1:
                    max_pixel_difference = int(max_pixel_difference * img.get_width() * img.get_height())

            if diff_count > max_pixel_difference:
                self.save_image(img, new_fname)
                self.save_image(diff, diff_fname)
                raise RenpyTestScreenshotError(
                    f"{filename} (pixel difference: {diff_count} > {max_pixel_difference})\n"
                    f"Current image saved to {new_fname}\n"
                    f"Difference image saved to {diff_fname}"
                )
            else:
                if os.path.exists(new_fname):
                    os.remove(new_fname)
                if os.path.exists(diff_fname):
                    os.remove(diff_fname)

            next_node(self.next)
            return None

        finally:
            # Clear up surfaces to avoid memory leaks.
            if diff is not None:
                del diff
            if old_img is not None:
                del old_img
            if img is not None:
                del img

    def get_reference_image_path(self, filename: str) -> str | None:
        if os.path.exists(filename):
            return filename

        base_filename, ext = os.path.splitext(filename)
        fnames = glob.glob(os.path.join(base_filename + "@*" + ext))
        if len(fnames) > 1:
            raise RuntimeError(f"Multiple reference images found for {filename}: {', '.join(fnames)}")
        elif len(fnames) == 1:
            return fnames[0]

        return None

    def save_image(self, img: renpy.pygame.Surface, filename: str) -> None:
        path = os.path.dirname(filename)
        if path:
            os.makedirs(path, exist_ok=True)

        renpy.display.scale.image_save_unscaled(img, filename)


################################################################################
# Control structures.


class Exit(Node):
    def execute(self, state, t):
        raise renpy.game.QuitException


################################################################################
# Utility functions
################################################################################


def next_node(node: Node | None):
    renpy.test.testexecution.set_next_execution_node(node)


def scoped_eval(expr: str) -> Any:
    return renpy.test.testexecution.scoped_eval(expr)


def scoped_exec(source: str, hide: bool = False) -> None:
    renpy.test.testexecution.scoped_exec(source, hide)
