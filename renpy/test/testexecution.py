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

import argparse
from textwrap import dedent
from typing import Callable, Any

import renpy
import renpy.pygame as pygame

from renpy.error import FrameSummary
from renpy.test.testast import Node, BaseTestBlock, TestSuite, TestCase, TestHook, Exit
from renpy.test.types import NodeState, NodeLocation, RenpyTestTimeoutError, HookType
import renpy.test.testreporter as testreporter
from renpy.test.testsettings import _test

initialized: bool = False
global_testsuite_name = "global"

reached_labels: set[str] = set()
suite_stack: list[TestSuite] = []
scope_stack: list[dict[str, Any]] = [{}]

testcases: dict[str, TestCase] = {}
node_executor: "NodeExecutor"
phase_controller: "TestPhaseController"

################################################################################
## Public Methods


def exception_handler(exc: Exception) -> bool:
    """
    Handles exceptions that occur during the execution of testcases.
    This is called by Ren'Py when an exception is raised.
    """
    if not is_in_test():
        return False

    phase_controller.handle_exception(exc)
    return True


def execute() -> None:
    """
    Called periodically by the core interact loop when a new frame is drawn.
    This allows test code to generate events, if desired.
    """

    if not is_in_test():
        return

    if renpy.display.interface.suppress_underlay and (not _test.force):
        return

    if _test.maximum_framerate:
        renpy.exports.maximum_framerate(10.0)
    else:
        renpy.exports.maximum_framerate(None)

    # Make sure there are no test events in the event queue.
    for e in pygame.event.copy_event_queue():  # type: ignore
        if getattr(e, "test", False):
            return

    try:
        phase_controller.update()
    except renpy.game.QuitException as e:
        status = quit_handler()
        raise renpy.game.QuitException(status=status)

    reached_labels.clear()


def initialize(specified_test: str) -> None:
    """
    Initializes the test execution system. This is called when the game starts, and
    sets up the testcases and the context stack.
    """

    global initialized
    global node_executor
    global phase_controller

    if initialized:
        return

    root = setup_global_test_suite()

    test_node = get_testcase_by_id(specified_test)
    select_testcase(test_node)
    process_only_flag()
    update_suite_enabled_flag(root)
    root.chain(None)

    testreporter.reporter.initialize_test_outcomes(root)

    node_executor = NodeExecutor(None)
    phase_controller = TestPhaseController(root)
    initialized = True

def has_default_testcase() -> bool:
    """
    Returns True if at least one testcase exists.
    """

    root = setup_global_test_suite()
    return root.has_testcase()


def on_reload() -> None:
    if add_reached_label not in renpy.config.label_callbacks:
        renpy.config.label_callbacks.append(add_reached_label)

    testreporter.reporter.on_reload()


def is_in_test() -> bool:
    return initialized and phase_controller is not None and phase_controller.is_running


def pop_suite_stack() -> None:
    suite = suite_stack.pop()
    scope_stack.pop()

    testreporter.reporter.test_suite_end(suite)


def push_suite_stack(suite: TestSuite) -> None:
    testreporter.reporter.test_suite_start(suite, depth=len(suite_stack))
    suite_stack.append(suite)
    push_scope_stack(suite.current_parameters)


def push_scope_stack(new_scope: dict[str, Any]) -> None:
    updated_scope = scope_stack[-1].copy()
    updated_scope.update(new_scope)
    scope_stack.append(updated_scope)


def quit_handler() -> int:
    """
    Handles the quit command and QuitException thrown by the test.
    Returns a status code that indicates whether the test passed or failed.
    """

    if not is_in_test():
        return 0

    phase_controller.quit()

    if testreporter.reporter.has_failed:
        return 1
    return 0


def set_next_execution_node(next_node: Node | None) -> None:
    """
    Sets the next node to execute. This is used to change the flow of execution
    to a different node.
    """

    node_executor.set_next_node(next_node)


def add_reached_label(label: str, abnormal: bool) -> None:
    reached_labels.add(label)


def get_current_scope() -> dict:
    """
    Returns the current scope for py_eval.
    """
    return scope_stack[-1]


def scoped_eval(expr: str, store: str = "store") -> Any:
    """
    Evaluates a Python expression in the current test scope.
    """

    scope = renpy.test.testexecution.get_current_scope()
    globals = renpy.python.store_dicts[store]
    return renpy.python.py_eval(expr, globals=globals, locals=scope)


def scoped_exec(source: str, hide: bool = False, store: str = "store") -> None:
    """
    Executes Python bytecode in the current test scope.

    If `hide` is True, the executed code will not be visible in the store.
    """

    scope = renpy.test.testexecution.get_current_scope()
    old_keys = set(scope.keys())
    globals = renpy.python.store_dicts[store]

    # code = renpy.ast.PyCode(source, mode="hide" if hide else "exec")
    renpy.python.py_exec_bytecode(dedent(source), hide, globals=globals, locals=scope)

    if hide:
        return

    new_keys = set(scope.keys()) - old_keys
    for key in new_keys:
        globals[key] = scope[key]
        del scope[key]


################################################################################
## Setup methods


def link_top_level_testcase_to_parent(node: TestCase) -> None:
    """
    Links a top-level testcase (with a name that contains a dot) to its parent TestSuite.
    """
    if "." not in node.full_path:
        return

    parent_name = node.full_path.rsplit(".", 1)[0]
    parent_node = get_testcase_by_id(parent_name)
    if not isinstance(parent_node, TestSuite):
        raise TypeError(f'Parent node "{parent_name}" is not a TestSuite.')
    parent_node.add(node)


def add_child_testcases(parent: TestCase) -> None:
    if not isinstance(parent, TestSuite):
        return

    for child in parent.subtests:
        register_testcase(child, parent)


def register_testcase(node: TestCase, parent: TestSuite | None = None) -> None:
    """
    Adds a testcase to the `testcases` dictionary. The name is a tuple of strings,
    and the node is the root node of the testcase.
    """

    ## NOTE: This is run every time the script is reloaded.

    if node.full_path in testcases:
        if testcases[node.full_path] != node:
            raise KeyError(
                f"The testcase {node.full_path!r} is defined twice, "
                f"at File {testcases[node.full_path].filename}:{testcases[node.full_path].linenumber} "
                f"and File {node.filename}:{node.linenumber}."
            )
        return

    testcases[node.full_path] = node

    add_child_testcases(node)
    if parent is None:
        link_top_level_testcase_to_parent(node)


global_test_suite: TestSuite | None = None
"Caches the global test suite, once it's been set up."


def setup_global_test_suite() -> TestSuite:
    """
    Set up the global test suite, which contains all top-level testcases,
    and contains hooks for before and after each test.
    """

    global global_test_suite
    if global_test_suite is not None:
        return global_test_suite

    root_children = []
    for node_name, node in testcases.items():
        if (node_name == global_testsuite_name) or (node.parent is not None):
            continue
        root_children.append(node)

    try:
        root = get_testcase_by_id(global_testsuite_name)
        if not isinstance(root, TestSuite):
            raise ValueError(f"Root node for {global_testsuite_name!r} must be a TestSuite, got {type(root)}")

        for child in root_children:
            root.add(child)
    except KeyError:
        root = TestSuite(name=global_testsuite_name, loc=("", 0), subtests=root_children)
        register_testcase(root)

    global_test_suite = root

    return root


def get_testcase_by_id(id: str) -> TestCase:
    if id not in testcases:
        if suggestion := renpy.error.compute_closest_value(id, list(testcases.keys())):
            raise KeyError(f"TestCase {id} not found. Did you mean: {suggestion}?")
        raise KeyError(f"TestCase {id} not found.")

    return testcases[id]


def process_only_flag() -> None:
    """
    If any testcase has the `only` flag set, all other testcases that do not have
    the `only` flag will be marked as skipped.

    Parent tests will ignore the skip flag if they have a child with the `only` flag set.
    Child tests are unaffected.
    """
    has_only = [tc for tc in testcases.values() if tc.only]

    if not has_only:
        return

    testreporter.reporter.log_message(f"Running {len(has_only)} test(s) marked with 'only' flag.")
    for tc in has_only:
        testreporter.reporter.log_message(f"- {tc.full_path}")

    processed = set()

    def enable_relatives(tc: TestCase):
        if tc in processed:
            return

        processed.add(tc)

        # Enable parents
        parent = tc.parent
        while parent is not None:
            if parent in processed:
                break
            processed.add(parent)
            parent = parent.parent

        # Mark children so they are not skipped later
        if isinstance(tc, TestSuite):
            for child in tc.subtests:
                enable_relatives(child)

    for tc in has_only:
        enable_relatives(tc)

    for tc in testcases.values():
        tc.enabled = tc in processed


def select_testcase(node: TestCase) -> None:
    id = node.full_path

    if id == global_testsuite_name:
        return

    for tc in testcases.values():
        if tc.full_path == id:
            tc.only = True
        else:
            tc.only = False


def update_suite_enabled_flag(node: TestSuite) -> None:
    """
    Updates the enabled flag for a TestSuite and its children based on the enable_all setting.
    """
    for child in node.subtests:
        if isinstance(child, TestSuite):
            update_suite_enabled_flag(child)
        else:
            child.enabled = _test.enable_all or child.enabled

    is_child_enabled = any(child.enabled for child in node.subtests)
    node.enabled = _test.enable_all or (node.enabled and is_child_enabled)


################################################################################
## NODE EXECUTOR


class NodeExecutor:
    """
    This class is responsible for executing a single node in the test execution.
    It manages the state of the node, handles starting and executing it, and
    transitions to the next node when the current one is done.
    """

    node: Node | None = None
    "Current node being executed."

    node_state: NodeState | None = None
    "The state of the current node being executed."

    node_has_started: bool = False
    "Whether the current node has run the start() method."

    next_node: Node | None = None
    "The next node to execute after the current one."

    old_state: NodeState | None = None
    "The previous state of the current node."

    old_loc: NodeLocation | None = None
    "The previous location in the game script of the current node."

    last_state_change: float = 0.0
    "The last time the state changed."

    end_callbacks: list[Callable] | None = None
    "A callback to run when no more nodes are left to execute."

    def __init__(self, node: Node | None = None):
        self.reinitialize(node)

    def reinitialize(self, node: Node | None) -> None:
        self.node = node
        self.node_state = None
        self.node_has_started = False
        self.next_node = None
        self.old_state = None
        self.old_loc = None
        self.last_state_change = renpy.display.core.get_time()

    def set_next_node(self, next: Node | None) -> None:
        self.next_node = next

    def set_end_callback(self, callback: Callable | list[Callable]) -> None:
        if not isinstance(callback, list):
            callback = [callback]
        self.end_callbacks = callback

    def execute(self) -> None:
        """
        Performs one execution cycle of a node.
        """
        if self.node is None:
            self.move_to_next_node_if_possible()
            return

        now = renpy.display.core.get_time()

        if not self.node_has_started:
            if not self.node.ready():
                self.check_for_timeout(now)
                return

            self.node_state = self.node.start()
            self.start = now
            self.node_has_started = True

        elapsed = now - self.start
        try:
            self.node_state = self.node.execute(self.node_state, elapsed)
        except renpy.game.QuitException:
            if isinstance(node_executor.node, Exit):
                # Handle Exit nodes gracefully, and run any callbacks.
                self.node_state = None
                self.next_node = None
                self.move_to_next_node_if_possible()
                raise
        except renpy.game.CONTROL_EXCEPTIONS:
            self.node_state = None
            self.next_node = self.node.next
            self.move_to_next_node_if_possible()
            raise

        self.move_to_next_node_if_possible()

        self.check_for_timeout(now)

    def move_to_next_node_if_possible(self) -> None:
        if self.node_state is not None:
            return

        if self.node is not None:
            self.node.done = True

        self.node = self.next_node
        self.node_has_started = False

        if self.node is None and self.end_callbacks is not None:
            for callback in self.end_callbacks:
                callback()
            self.end_callbacks = None

    def check_for_timeout(self, now) -> None:
        self.update_last_state_change(now)

        if (now - self.last_state_change) > _test.timeout:
            raise RenpyTestTimeoutError(f"TestCase timed out after {_test.timeout} seconds.")

    def cleanup_after_error(self) -> None:
        if self.node is not None:
            self.node.cleanup_after_error(self.node_state)

    def update_last_state_change(self, now):
        loc = renpy.exports.get_filename_line()

        if (self.old_state != self.node_state) or (self.old_loc != loc):
            self.last_state_change = now

        self.old_state = self.node_state
        self.old_loc = loc

    @property
    def done(self) -> bool:
        return self.node is None


################################################################################
## STATE MACHINE
class TestPhaseController:
    """
    This class is a finite state machine that manages the test execution.
    It transitions between different phases, such as
    running hooks, running testcases, and handling exceptions.
    """

    def __init__(self, root_suite: TestSuite):
        self.active_phase: BaseExecutionPhase = StartPhase(root_suite)
        testreporter.reporter.test_run_start()
        self.active_phase.enter()
        self.next_phase: BaseExecutionPhase | None = None

    @property
    def is_running(self) -> bool:
        return not isinstance(self.active_phase, EndPhase)

    def update(self):
        try:
            node_executor.execute()

            while node_executor.done and node_executor.next_node is None:
                next_phase = self.active_phase.update()
                self.transition_to_new_phase(next_phase)

        except renpy.game.CONTROL_EXCEPTIONS:
            raise

        except Exception as exc:
            self.handle_exception(exc)

    def transition_to_new_phase(self, new_state: "BaseExecutionPhase | None") -> None:
        if new_state is None:
            return

        del self.active_phase
        self.active_phase = new_state
        new_state.enter()

    def handle_exception(self, exc: Exception) -> None:
        if self.active_phase.block is None or not self.active_phase.block.xfail:
            xfailed = False
            status = testreporter.OutcomeStatus.FAILED
        else:
            xfailed = True
            status = testreporter.OutcomeStatus.XFAILED

        frame_stack = self.get_frame_stack()
        testreporter.reporter.log_exception(exc, frame_stack, xfailed)

        if node_executor.node is not None:
            node_executor.cleanup_after_error()
        node_executor.reinitialize(None)

        new_state = self.active_phase.error(status)
        self.transition_to_new_phase(new_state)

    def get_frame_stack(self) -> list[FrameSummary]:
        """
        Returns a list of FrameSummary objects representing the current context stack.
        This indicates where the exception occurred in the test execution.
        """
        frame_stack: list[FrameSummary] = []

        nodes: list[Node | None] = [s for s in suite_stack]
        labels: list[str] = [f"testsuite {suite.current_parameterized_name}" for suite in suite_stack]

        block = self.active_phase.block
        if isinstance(block, TestHook):
            nodes.append(block)
            labels.append(f"hook {block.current_parameterized_name}")
        elif isinstance(block, TestCase):
            nodes.append(block)
            labels.append(f"testcase {block.current_parameterized_name}")

        nodes.append(node_executor.node)
        labels.insert(0, "None")

        for n, label in zip(nodes, labels):
            if n is None:
                frame_stack.append(FrameSummary(str(label), "<during last test>", 0))
            else:
                frame_stack.append(FrameSummary(str(label), n.filename, n.linenumber))

        return frame_stack

    def quit(self) -> None:
        """
        Quits the test execution, transitioning to the EndPhase.
        """
        if isinstance(self.active_phase, EndPhase):
            return

        node_executor.reinitialize(None)
        new_state = EndPhase()
        self.transition_to_new_phase(new_state)


################################################################################
## STATE / PHASE BASES
class BaseExecutionPhase:
    """A base class for all execution phases."""

    block: BaseTestBlock | None = None

    def enter(self) -> None:
        """Called when entering this phase."""
        pass

    def error(self, status: testreporter.OutcomeStatus) -> "BaseExecutionPhase | None":
        """
        Returns the phase to transition to when an error occurs.
        By default, transitions to the EndPhase.
        """
        raise RuntimeError("Exception occurred outside of a testcase or hook.")

    def update(self) -> "BaseExecutionPhase | None":
        """
        Returns a new phase, or None to stay in the current phase.

        Runs only if node_executor has finished executing the provided nodes.
        """
        pass


class HookPhase(BaseExecutionPhase):
    def error(self, status):
        if not isinstance(self.block, TestHook):
            raise RuntimeError("Block is not a TestHook.")

        testreporter.reporter.test_hook_end(self.block, status, depth=len(suite_stack))
        self.block.increment_call_count()
        return SuiteTeardownPhase()


class HookLoopPhase(HookPhase):
    """A phase that loops through the suite stack, running hooks at each level."""

    suite_depth: int
    hook_type: HookType
    next_phase: type[BaseExecutionPhase]
    reverse: bool

    def __init__(self, reverse: bool = False):
        self.reverse = reverse

    def enter(self) -> None:
        if self.reverse:
            self.suite_depth = len(suite_stack) - 1
        else:
            self.suite_depth = 0

    def update(self) -> BaseExecutionPhase | None:
        condition = (lambda: self.suite_depth >= 0) if self.reverse else (lambda: self.suite_depth < len(suite_stack))
        step = -1 if self.reverse else 1

        while condition():
            self.block = suite_stack[self.suite_depth].get_hook(self.hook_type)

            if self.block is None or not self.should_hook_run(self.block):
                self.suite_depth += step
                continue

            testreporter.reporter.test_hook_start(self.block, depth=len(suite_stack))
            node_executor.set_next_node(self.block)
            node_executor.set_end_callback([
                renpy.curry.partial(testreporter.reporter.test_hook_end, self.block, depth=len(suite_stack)),
                self.block.increment_call_count,
            ])
            self.suite_depth += step
            return None

        return self.next_phase()

    def should_hook_run(self, hook: TestHook | None) -> bool:
        """Returns True if the given hook should run at the given depth in the suite stack."""
        if hook is None:
            return False

        if hook.depth < 0:
            return True

        return hook.depth + self.suite_depth >= len(suite_stack) - 1


################################################################################
## STATES / PHASES
class StartPhase(BaseExecutionPhase):
    def __init__(self, root_suite: TestSuite):
        self.root_suite = root_suite

    def enter(self) -> None:
        push_suite_stack(self.root_suite)

    def update(self) -> BaseExecutionPhase | None:
        return SuiteSetupPhase()


class EndPhase(BaseExecutionPhase):
    def enter(self) -> None:
        while suite_stack:
            pop_suite_stack()
        testreporter.reporter.test_run_end()
        renpy.test.testmouse.reset()


class NextTestTransitionPhase(BaseExecutionPhase):
    """
    Checks if there are more tests to run in the current suite.
    If so, transitions to the appropriate state to run the next test.
    If not, transitions to the EndState or RunAfterState as appropriate.
    """

    def update(self) -> BaseExecutionPhase | None:
        if suite_stack[-1].has_completed_all_subtests:
            return SuiteTeardownPhase()

        current_test = suite_stack[-1].current_test
        if current_test is None:
            raise RuntimeError("No current test to run.")

        if not current_test.enabled:
            testreporter.reporter.test_case_skipped(current_test)
            current_test.advance_to_next_parameter_set()
            if current_test.has_all_parameters_been_processed:
                suite_stack[-1].advance_to_next_subtest()
                current_test.restart()
            return None  # NextTestTransitionPhase()

        if isinstance(current_test, TestSuite):
            return BeforeTestSuitePhase()
        elif isinstance(current_test, TestCase):
            return BeforeTestCasePhase()

        raise TypeError("Current test is neither a TestSuite nor a TestCase.")


class BeforeTestSuitePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.BEFORE_TESTSUITE
        self.next_phase = AddSubSuitePhase
        self.reverse = False


class AddSubSuitePhase(BaseExecutionPhase):
    def enter(self) -> None:
        if suite_stack[-1].current_test is None:
            raise RuntimeError("No current test to run.")
        elif not isinstance(suite_stack[-1].current_test, TestSuite):
            raise TypeError("Current test is not a TestSuite.")

        push_suite_stack(suite_stack[-1].current_test)

    def update(self) -> BaseExecutionPhase | None:
        return SuiteSetupPhase()


class SuiteSetupPhase(HookPhase):
    def enter(self) -> None:
        self.block = suite_stack[-1].get_hook(HookType.SETUP)
        if self.block is not None:
            testreporter.reporter.test_hook_start(self.block, depth=len(suite_stack))
            node_executor.set_next_node(self.block)
            node_executor.set_end_callback([
                renpy.curry.partial(testreporter.reporter.test_hook_end, self.block, depth=len(suite_stack)),
                self.block.increment_call_count,
            ])

    def update(self) -> BaseExecutionPhase | None:
        return NextTestTransitionPhase()


class BeforeTestCasePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.BEFORE_TESTCASE
        self.next_phase = TestCasePhase
        self.reverse = False


class TestCasePhase(BaseExecutionPhase):
    def enter(self) -> None:
        if suite_stack[-1].current_test is None:
            raise RuntimeError("No current test to run.")

        self.block = suite_stack[-1].current_test
        push_scope_stack(self.block.current_parameters)

        testreporter.reporter.test_case_start(self.block, depth=len(suite_stack))
        node_executor.set_next_node(self.block)
        node_executor.set_end_callback(
            renpy.curry.partial(testreporter.reporter.test_case_end, self.block, depth=len(suite_stack))
        )

    def error(self, status) -> BaseExecutionPhase | None:
        if not isinstance(self.block, TestCase):
            raise RuntimeError("Block is not a TestCase.")

        testreporter.reporter.test_case_end(self.block, status, depth=len(suite_stack))
        return self.update()

    def update(self) -> BaseExecutionPhase | None:
        scope_stack.pop()
        return AfterTestCasePhase()


class AfterTestCasePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.AFTER_TESTCASE
        self.next_phase = TestCaseParameterCyclePhase
        self.reverse = True


class TestCaseParameterCyclePhase(BaseExecutionPhase):
    def update(self) -> BaseExecutionPhase | None:
        current_test = suite_stack[-1].current_test
        if not isinstance(current_test, TestCase):
            raise RuntimeError(f"Expecting TestCase, got {type(current_test)}.")

        current_test.advance_to_next_parameter_set()

        if current_test.has_all_parameters_been_processed:
            suite_stack[-1].advance_to_next_subtest()
            current_test.restart()
            return NextTestTransitionPhase()
        return BeforeTestCasePhase()


class SuiteTeardownPhase(HookPhase):
    def enter(self) -> None:
        self.block = suite_stack[-1].get_hook(HookType.TEARDOWN)
        if self.block is not None:
            testreporter.reporter.test_hook_start(self.block, depth=len(suite_stack))
            node_executor.set_next_node(self.block)
            node_executor.set_end_callback([
                renpy.curry.partial(testreporter.reporter.test_hook_end, self.block, depth=len(suite_stack)),
                self.block.increment_call_count,
            ])

    def update(self) -> BaseExecutionPhase | None:
        if len(suite_stack) > 1:
            return RemoveSubSuitePhase()
        else:
            return GlobalParameterCyclePhase()

    def error(self, status):
        super().error(status)
        return self.update()


class RemoveSubSuitePhase(BaseExecutionPhase):
    def enter(self) -> None:
        pop_suite_stack()

    def update(self) -> BaseExecutionPhase | None:
        return AfterTestSuitePhase()


class AfterTestSuitePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.AFTER_TESTSUITE
        self.next_phase = TestSuiteParameterCyclePhase
        self.reverse = True


class TestSuiteParameterCyclePhase(BaseExecutionPhase):
    def update(self) -> BaseExecutionPhase | None:
        current_test = suite_stack[-1].current_test
        if not isinstance(current_test, TestSuite):
            raise RuntimeError(f"Expecting TestSuite, got {type(current_test)}.")

        current_test.advance_to_next_parameter_set()

        if current_test.has_all_parameters_been_processed:
            suite_stack[-1].advance_to_next_subtest()
            current_test.restart()
            return NextTestTransitionPhase()
        return BeforeTestSuitePhase()


class GlobalParameterCyclePhase(BaseExecutionPhase):
    def update(self) -> BaseExecutionPhase | None:
        root = suite_stack[-1]
        pop_suite_stack()

        root.advance_to_next_parameter_set()
        if root.has_all_parameters_been_processed:
            return EndPhase()

        return StartPhase(root)


def test_command() -> bool:
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ## NOTE: This command gets called after the game finishes and returns to the main menu
    if initialized:
        return True

    ap = renpy.arguments.ArgumentParser(description="Run a Ren'Py test case or suite.")

    ap.add_argument(
        "testcase",
        help=f"Name of the test case or suite to run (default: {global_testsuite_name}).",
        nargs="?",
        type=str,
        default=global_testsuite_name,
    )

    group = ap.add_argument_group(title="Test Execution")
    group.add_argument(
        "--enable-all",
        dest="_test.enable_all",
        action="store_true",
        default=False,
        help="Run all test cases and test suites, even if they are disabled. "
        "Does not work if a specific test case or suite is specified.",
    )
    group.add_argument(
        "--overwrite-screenshots",
        dest="_test.overwrite_screenshots",
        action="store_true",
        default=False,
        help="Replace existing screenshots when a screenshot is taken during tests.",
    )

    group = ap.add_argument_group(title="Console Reporting")
    group.add_argument(
        "--hide-header",
        dest="_test.report.hide_header",
        action="store_true",
        default=False,
        help="Disable header at start of run",
    )
    group.add_argument(
        "--hide-execution",
        dest="_test.report.hide_execution",
        action="store",
        choices=["no", "hooks", "testcases", "all"],
        default="hooks",
        help="Hide test execution output. 'hooks' hides hooks, 'testcases' hides test cases and hooks, and 'all' hides everything including test suites.",
    )
    group.add_argument(
        "--hide-summary",
        dest="_test.report.hide_summary",
        action="store_true",
        default=False,
        help="Disable summary",
    )
    group.add_argument(
        "--report-detailed",
        dest="_test.report.report_detailed",
        action="store_true",
        default=False,
        help="Show detailed information about each test during the run.",
    )
    group.add_argument(
        "--report-skipped",
        dest="_test.report.report_skipped",
        action="store_true",
        default=False,
        help="Show information about skipped tests (use with --report-detailed).",
    )

    args = ap.parse_args()

    for key, value in vars(args).items():
        key_parts = key.split(".")

        if key_parts[0] != "_test":
            continue
        obj = _test

        for part in key_parts[1:-1]:
            obj = getattr(obj, part)

        if hasattr(obj, key_parts[-1]):
            setattr(obj, key_parts[-1], value)
        else:
            raise AttributeError(f"Unknown test setting: {key}")

    testreporter.reporter.add_reporter(testreporter.ConsoleReporter())
    initialize(args.testcase)

    # Disable vsync, to speed up testing.
    renpy.config.gl_vsync = False

    return True


renpy.arguments.register_command("test", test_command, uses_display=True)
