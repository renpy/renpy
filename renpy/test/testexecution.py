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
from typing import Callable


import renpy
import renpy.pygame as pygame

from renpy.error import FrameSummary
from renpy.test.testast import Node, Block, TestSuite, TestCase, TestHook
from renpy.test.types import NodeState, NodeLocation, RenpyTestTimeoutError, HookType
import renpy.test.testreporter as testreporter
from renpy.test.testsettings import _test

initialized: bool = False
global_testsuite_name = "global"
isolated_testsuite_name = "<Top>"

action: Callable | None = None
reached_labels: set[str] = set()
suite_stack: list[TestSuite] = []

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

    global action

    if not is_in_test():
        return

    if renpy.display.interface.suppress_underlay and (not _test.force):
        return

    renpy.exports.maximum_framerate(10.0 if _test.maximum_framerate else None)

    # Make sure there are no test events in the event queue.
    for e in pygame.event.copy_event_queue():
        if getattr(e, "test", False):
            return

    if action:
        old_action = action
        action = None
        renpy.display.behavior.run(old_action)

    try:
        phase_controller.update()
    except renpy.game.QuitException as e:
        status = quit_handler()
        raise renpy.game.QuitException(status=status)

    reached_labels.clear()


def initialize(root_name: str) -> None:
    """
    Initializes the test execution system. This is called when the game starts, and
    sets up the testcases and the context stack.
    """

    global initialized
    global node_executor
    global phase_controller

    if initialized:
        return

    suite = create_or_get_root_suite(root_name)
    process_only_flag()
    update_suite_skip_flag(suite)
    suite.chain(None)

    testreporter.reporter.initialize_test_outcomes(suite)

    node_executor = NodeExecutor(None)
    phase_controller = TestPhaseController(suite)
    initialized = True


def is_in_test() -> bool:
    return initialized and phase_controller is not None and phase_controller.is_running


def pop_suite_stack() -> None:
    suite = suite_stack.pop()

    testreporter.reporter.test_suite_end(suite)

    if len(suite_stack) == 0:
        testreporter.reporter.test_run_end()
        renpy.test.testmouse.reset()


def push_suite_stack(suite: TestSuite) -> None:
    testreporter.reporter.test_suite_start(suite, depth=len(suite_stack))
    suite_stack.append(suite)


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


def report_testcase_skipped(node: TestCase) -> None:
    """
    Marks all children (if any) of the given testcase as skipped.
    """
    if isinstance(node, TestSuite):
        for child in node.subtests:
            report_testcase_skipped(child)

    testreporter.reporter.test_case_skipped(node)


def set_action(a: Callable) -> None:
    """
    Sets an action to run before continuing the test execution.
    This action will be run once, and then cleared.
    """

    global action
    action = a


def set_next_execution_node(next_node: Node | None) -> None:
    """
    Sets the next node to execute. This is used to change the flow of execution
    to a different node.
    """

    node_executor.set_next_node(next_node)


################################################################################
## Setup methods


def link_top_level_testcase_to_parent(node: TestCase) -> None:
    """
    Links a top-level testcase (with a name that contains a dot) to its parent TestSuite.
    """
    if "." not in node.name:
        return

    parent_name = node.name.rsplit(".", 1)[0]
    parent_node = get_testcase_by_name(parent_name)
    if not isinstance(parent_node, TestSuite):
        raise TypeError(f'Parent node "{parent_name}" is not a TestSuite.')
    parent_node.add(node)


def add_child_testcases(parent: TestCase) -> None:
    if not isinstance(parent, TestSuite):
        return

    for child in parent.subtests:
        register_testcase(child, parent)


def create_or_get_root_suite(root_name: str) -> TestSuite:
    if root_name == global_testsuite_name:
        setup_global_test_suite()

    root = get_testcase_by_name(root_name)

    if isinstance(root, TestSuite):
        return root

    return TestSuite(name=isolated_testsuite_name, loc=(root.filename, root.linenumber), subtests=[root])


def register_testcase(node: TestCase, parent: TestSuite | None = None) -> None:
    """
    Adds a testcase to the `testcases` dictionary. The name is a tuple of strings,
    and the node is the root node of the testcase.
    """

    ## NOTE: This is run every time the script is reloaded.

    if node.name in testcases:
        if testcases[node.name] != node:
            raise KeyError(
                f"The testcase {node.name!r} is defined twice, "
                f"at File {testcases[node.name].filename}:{testcases[node.name].linenumber} "
                f"and File {node.filename}:{node.linenumber}."
            )
        return

    testcases[node.name] = node

    add_child_testcases(node)
    if parent is None:
        link_top_level_testcase_to_parent(node)


def setup_global_test_suite() -> None:
    """
    Set up the global test suite, which contains all top-level testcases,
    and contains hooks for before and after each test.
    """
    if global_testsuite_name not in testcases:
        register_testcase(TestSuite(name=global_testsuite_name, loc=("", 0), subtests=[]))

    root = get_testcase_by_name(global_testsuite_name)

    if not isinstance(root, TestSuite):
        raise ValueError(f"Root node for {global_testsuite_name!r} must be a TestSuite, got {type(root)}")

    for node_name, node in testcases.items():
        if (node_name == global_testsuite_name) or ("." in node_name):
            continue
        root.subtests.append(node)


def get_testcase_by_name(name: str) -> TestCase:
    if name not in testcases:
        raise KeyError(f"Testcase {name} not found.")

    return testcases[name]


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

    processed = set()

    def unskip_relatives(tc: TestCase):
        if tc in processed:
            return

        processed.add(tc)

        # Unskip parents
        parent = tc.parent
        while parent is not None:
            if parent in processed:
                break
            processed.add(parent)
            parent.skip = False
            parent = parent.parent

        # Mark children so they are not skipped later
        if isinstance(tc, TestSuite):
            for child in tc.subtests:
                unskip_relatives(child)

    for tc in has_only:
        unskip_relatives(tc)

    for tc in testcases.values():
        if tc not in processed:
            tc.skip = True


def update_suite_skip_flag(node: TestSuite) -> None:
    """
    Updates the skip flag for a TestSuite and its children based on the ignore_skip_flag setting.
    """
    for child in node.subtests:
        if isinstance(child, TestSuite):
            update_suite_skip_flag(child)
        else:
            child.skip = not _test.ignore_skip_flag and child.skip

    all_children_skipped = all(child.skip for child in node.subtests)
    node.skip = not _test.ignore_skip_flag and (node.skip or all_children_skipped)


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

    end_callback: Callable | None = None
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

    def set_end_callback(self, callback: Callable) -> None:
        self.end_callback = callback

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
        self.node_state = self.node.execute(self.node_state, elapsed)
        self.move_to_next_node_if_possible()

        self.check_for_timeout(now)

    def move_to_next_node_if_possible(self) -> None:
        if self.node_state is not None:
            return

        if self.node is not None:
            self.node.done = True

        self.node = self.next_node
        self.node_has_started = False

        if self.node is None and self.end_callback is not None:
            self.end_callback()
            self.end_callback = None

    def check_for_timeout(self, now) -> None:
        self.update_last_state_change(now)

        timeout = _test.timeout
        if hasattr(self.node, "timeout") and self.node.timeout > 0:  # type: ignore
            timeout = self.node.timeout  # type: ignore

        if (now - self.last_state_change) > timeout:
            raise RenpyTestTimeoutError(f"Testcase timed out after {timeout} seconds.")

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

        except renpy.game.QuitException:
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
        frame_stack = self.get_frame_stack()
        testreporter.reporter.log_exception(exc, frame_stack)

        if node_executor.node is not None:
            node_executor.node.cleanup_after_error()
        node_executor.reinitialize(None)

        new_state = self.active_phase.error()
        self.transition_to_new_phase(new_state)

    def get_frame_stack(self) -> list[FrameSummary]:
        """
        Returns a list of FrameSummary objects representing the current context stack.
        This indicates where the exception occurred in the test execution.
        """
        frame_stack: list[FrameSummary] = []

        nodes: list[Node | None] = [s for s in suite_stack]
        labels: list[str] = [f"testsuite {suite.name}" for suite in suite_stack]

        block = self.active_phase.block
        if isinstance(block, TestHook):
            nodes.append(block)
            labels.append(f"hook {block.name}")
        elif isinstance(block, TestCase):
            nodes.append(block)
            labels.append(f"testcase {block.name}")

        nodes.append(node_executor.node)
        labels.insert(0, "None")

        for n, label in zip(nodes, labels):
            if n is None:
                frame_stack.append(FrameSummary(str(label), "<during last test>", 0))
            else:
                frame_stack.append(FrameSummary(str(label), n.filename, n.linenumber))

        return frame_stack

    def quit(self) -> None:
        while suite_stack:
            pop_suite_stack()


################################################################################
## STATES / PHASES
class BaseExecutionPhase:
    """A base class for all execution phases."""

    block: Block | None = None

    def enter(self) -> None:
        """Called when entering this phase."""
        pass

    def error(self) -> "BaseExecutionPhase | None":
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
    def error(self):
        if not isinstance(self.block, TestHook):
            raise RuntimeError("Block is not a TestHook.")

        testreporter.reporter.test_hook_end(self.block, testreporter.OutcomeStatus.FAILED, depth=len(suite_stack))
        return RemoveSubSuitePhase()


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
            node_executor.set_end_callback(
                renpy.curry.partial(testreporter.reporter.test_hook_end, self.block, depth=len(suite_stack))
            )
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


class StartPhase(BaseExecutionPhase):
    def __init__(self, root_suite: TestSuite):
        self.root_suite = root_suite

    def enter(self) -> None:
        testreporter.reporter.test_run_start()
        push_suite_stack(self.root_suite)

    def update(self) -> BaseExecutionPhase | None:
        return BeforeSuitePhase()


class EndPhase(BaseExecutionPhase):
    def enter(self) -> None:
        pop_suite_stack()
        testreporter.reporter.test_run_end()


class NextTestTransitionPhase(BaseExecutionPhase):
    """
    Checks if there are more tests to run in the current suite.
    If so, transitions to the appropriate state to run the next test.
    If not, transitions to the EndState or RunAfterState as appropriate.
    """

    def enter(self) -> None:
        suite_stack[-1].advance()

    def update(self) -> BaseExecutionPhase | None:
        if suite_stack[-1].is_all_tests_completed:
            return AfterSuitePhase()

        current_test = suite_stack[-1].current_test
        if current_test is None:
            raise RuntimeError("No current test to run.")

        if current_test.skip:
            report_testcase_skipped(current_test)
            return NextTestTransitionPhase()

        if isinstance(current_test, TestSuite):
            return BeforeEachSuitePhase()
        elif isinstance(current_test, TestCase):
            return BeforeEachCasePhase()
        return None


class BeforeEachSuitePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.BEFORE_EACH_SUITE
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
        return BeforeSuitePhase()


class BeforeSuitePhase(BaseExecutionPhase):
    def enter(self) -> None:
        self.block = suite_stack[-1].before
        if self.block is not None:
            testreporter.reporter.test_hook_start(self.block, depth=len(suite_stack))
            node_executor.set_next_node(self.block)
            node_executor.set_end_callback(
                renpy.curry.partial(testreporter.reporter.test_hook_end, self.block, depth=len(suite_stack))
            )

    def update(self) -> BaseExecutionPhase | None:
        return NextTestTransitionPhase()


class BeforeEachCasePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.BEFORE_EACH_CASE
        self.next_phase = TestCasePhase
        self.reverse = False


class TestCasePhase(BaseExecutionPhase):
    def enter(self) -> None:
        if suite_stack[-1].current_test is None:
            raise RuntimeError("No current test to run.")

        self.block = suite_stack[-1].current_test
        testreporter.reporter.test_case_start(self.block, depth=len(suite_stack))
        node_executor.set_next_node(self.block)
        node_executor.set_end_callback(
            renpy.curry.partial(testreporter.reporter.test_case_end, self.block, depth=len(suite_stack))
        )

    def error(self) -> BaseExecutionPhase | None:
        if not isinstance(self.block, TestCase):
            raise RuntimeError("Block is not a TestCase.")

        testreporter.reporter.test_case_end(self.block, testreporter.OutcomeStatus.FAILED, depth=len(suite_stack))
        return None

    def update(self) -> BaseExecutionPhase | None:
        return AfterEachCasePhase()


class AfterEachCasePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.AFTER_EACH_CASE
        self.next_phase = NextTestTransitionPhase
        self.reverse = True


class AfterSuitePhase(BaseExecutionPhase):
    def enter(self) -> None:
        self.block = suite_stack[-1].after
        if self.block is not None:
            testreporter.reporter.test_hook_start(self.block, depth=len(suite_stack))
            node_executor.set_next_node(self.block)
            node_executor.set_end_callback(
                renpy.curry.partial(testreporter.reporter.test_hook_end, self.block, depth=len(suite_stack))
            )

    def update(self) -> BaseExecutionPhase | None:
        if len(suite_stack) > 1:
            return RemoveSubSuitePhase()
        else:
            return EndPhase()


class RemoveSubSuitePhase(BaseExecutionPhase):
    def enter(self) -> None:
        pop_suite_stack()

    def update(self) -> BaseExecutionPhase | None:
        return AfterEachSuitePhase()


class AfterEachSuitePhase(HookLoopPhase):
    def __init__(self):
        self.hook_type = HookType.AFTER_EACH_SUITE
        self.next_phase = NextTestTransitionPhase
        self.reverse = True


def test_command() -> bool:
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ## NOTE: This command gets called after the game finishes and returns to the main menu
    if initialized:
        return True

    ap = renpy.arguments.ArgumentParser(description="Runs a testcase.")
    ap.add_argument("testcase", help="The name of a testcase to run.", nargs="?", default=global_testsuite_name)
    ap.add_argument(
        "--no-skip",
        action="store_true",
        dest="ignore_skip_flag",
        default=False,
        help="Do not skip testcases marked as skip.",
    )
    ap.add_argument(
        "--print-details",
        action="store_true",
        dest="print_details",
        default=False,
        help="Print detailed information for entire run.",
    )
    ap.add_argument(
        "--print-skipped",
        action="store_true",
        dest="print_skipped",
        default=False,
        help="Print information about skipped testcases. Requires --print-detailed.",
    )

    args = ap.parse_args()
    _test.ignore_skip_flag = args.ignore_skip_flag
    _test.print_skipped = args.print_skipped
    _test.print_details = args.print_details

    testreporter.reporter.add_reporter(testreporter.ConsoleReporter())
    initialize(args.testcase)

    return True


renpy.arguments.register_command("test", test_command, uses_display=True)
