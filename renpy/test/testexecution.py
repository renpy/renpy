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
import renpy.pygame as pygame

from renpy.error import FrameSummary
from renpy.test.testast import Node, TestSuite, TestCase
from renpy.test.types import State, NodeLocation, RenpyTestTimeoutError, RenpyTestAssertionError
import renpy.test.testreporter as testreporter
from renpy.test.testsettings import _test

global_testsuite_name = "all"
"The name of the global testsuite that contains all testcases."

isolated_testsuite_name = "<Top>"
"The name of the dummy testsuite that is created when a testcase is run in isolation."

initialized: bool = False
"Whether the test execution system has been initialized."

current_statement: renpy.ast.Node | None = None
"The current statement that is being executed in the game script."

testcases: dict[str, TestCase] = {}
"A dictionary mapping the name of a testcase to the testcase node."

action: Node | None = None
"An action to run before continuing the test execution."

labels: set[str] = set()
"A set of labels that have been reached since the last time execute was called."

context_stack: list["TestSuiteContext"] = []
"Stack of contexts for test execution."

all_results: testreporter.TestSuiteResults
"A TestSuiteResults object that contains the results of all testcases to be executed."


################################################################################
## Public Methods

def is_in_test() -> bool:
    return len(context_stack) > 0


def set_current_statement(node: renpy.ast.Node) -> None:
    """
    Takes the name of a statement that is about to run.
    """
    global current_statement

    if not is_in_test():
        return

    current_statement = node

    if isinstance(node.name, str):
        labels.add(node.name)


def add_testcase(node: TestCase, parent: TestSuite | None = None) -> None:
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
                f"and File {node.filename}:{node.linenumber}.")
        return

    testcases[node.name] = node

    add_child_testcases(node)
    if parent is None:
        link_top_level_testcase_to_parent(node)


def set_next_node(next: Node | None) -> None:
    """
    Sets the next node to execute. This is used to change the flow of execution
    to a different node.
    """

    get_current_context().executor.set_next_node(next)


def initialize(name: str) -> None:
    """
    Initializes the test execution system. This is called when the game starts, and
    sets up the testcases and the context stack.
    """

    global initialized
    global testcases
    global context_stack
    global all_results

    if initialized:
        return

    suite = create_or_get_top_level_suite(name)
    update_suite_skip_flag(suite)
    suite.chain(None)

    all_results = testreporter.TestSuiteResults(suite.name)
    all_results.populate_children(suite)
    push_context_stack(suite)

    initialized = True


def execute() -> None:
    """
    Called periodically by the core interact loop when a new frame is drawn.
    This allows test code to generate events, if desired.
    """

    global context_stack
    global action
    global labels

    if not is_in_test():
        return

    if renpy.display.interface.suppress_underlay and (not _test.force):
        return

    if _test.maximum_framerate:
        renpy.exports.maximum_framerate(10.0)
    else:
        renpy.exports.maximum_framerate(None)

    # Make sure there are no test events in the event queue.
    for e in pygame.event.copy_event_queue():
        if getattr(e, "test", False):
            return

    if action:
        old_action = action
        action = None
        renpy.display.behavior.run(old_action)

    try:
        get_current_context().execute()
    except renpy.game.QuitException as e:
        status = quit_handler()
        raise renpy.game.QuitException(status=status)

    labels.clear()


def exception_handler(exc: Exception) -> bool:
    """
    Handles exceptions that occur during the execution of testcases.
    This is called by Ren'Py when an exception is raised.
    """
    if not is_in_test():
        return False

    get_current_context().handle_exception(exc)
    return True


def quit_handler() -> int:
    """
    Handles the quit command and QuitException thrown by the test.
    Returns a status code that indicates whether the test passed or failed.
    """

    global context_stack

    if not is_in_test():
        return 0

    while context_stack:
        pop_context_stack()

    if all_results and all_results.status == testreporter.TestCaseStatus.FAILED:
        return 1
    return 0


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
        raise TypeError(f"Parent node \"{parent_name}\" is not a TestSuite.")
    parent_node.add(node)


def add_child_testcases(parent: TestCase) -> None:
    if not isinstance(parent, TestSuite):
        return

    for child in parent.testcases:
        add_testcase(child, parent)


def create_or_get_top_level_suite(name) -> TestSuite:
    if name == global_testsuite_name:
        setup_global_test_suite()

    root = get_testcase_by_name(name)

    if isinstance(root, TestSuite):
        return root

    ## If the root is not a TestSuite, we create a new one and run the testcase in isolation.
    return TestSuite(
        name=isolated_testsuite_name,
        loc=(root.filename, root.linenumber),
        testcases=[root]
        )


def setup_global_test_suite() -> None:
    """
    Set up the global test suite, which contains all top-level testcases,
    and contains hooks for before and after each test.
    """
    if global_testsuite_name not in testcases:
        add_testcase(TestSuite(name=global_testsuite_name, loc=("", 0), testcases=[]))

    root = get_testcase_by_name(global_testsuite_name)

    if not isinstance(root, TestSuite):
        raise ValueError(f"Root node for {global_testsuite_name!r} must be a TestSuite, got {type(root)}")

    for node_name, node in testcases.items():
        if (node_name == global_testsuite_name) or ("." in node_name):
            continue
        root.testcases.append(node)


def get_testcase_by_name(name: str) -> TestCase:
    if name not in testcases:
        raise KeyError(f"Testcase {name} not found.")

    return testcases[name]


def update_suite_skip_flag(node: TestSuite) -> None:
    """
    Updates the skip flag for a TestSuite and its children based on the ignore_skip_flag setting.
    """
    for child in node.testcases:
        if isinstance(child, TestSuite):
            update_suite_skip_flag(child)
        else:
            child.skip = not _test.ignore_skip_flag and child.skip

    ## Skip if all the children are skipped, or if the node itself is marked as skipped.
    node.skip = not _test.ignore_skip_flag and (node.skip or all(child.skip for child in node.testcases))


################################################################################
## Context management

def get_current_context() -> "TestSuiteContext":
    """
    Returns the current context, or raises an exception if there is no context.
    """

    global context_stack

    if len(context_stack) == 0:
        raise Exception("No context on context stack.")

    return context_stack[-1]


def push_context_stack(node: TestSuite) -> None:
    """
    Pushes a new context onto the context stack, initializing it with the given TestSuite.
    """
    global context_stack

    if len(context_stack) == 0:
        testreporter.reporter.test_run_start()

    if node.skip:
        report_testcase_skipped(node)
        if len(context_stack) == 0:
            testreporter.reporter.test_run_end(all_results)
        return

    tc = TestSuiteContext(node)
    context_stack.append(tc)

    tc.results.begin()
    testreporter.reporter.test_suite_start(node)


def pop_context_stack() -> "TestSuiteContext":
    """
    Pops the last context from the stack and returns it.
    """

    global context_stack

    if not context_stack:
        raise Exception("No context on context stack.")

    rv = context_stack.pop()
    rv.executor.results.end(None)
    rv.results.end(None)

    testreporter.reporter.test_suite_end(rv.results)

    if len(context_stack) == 0:
        testreporter.reporter.test_run_end(rv.results)
    else:
        ctx = get_current_context()
        ctx.executor.reinitialize(ctx.results, None)

    renpy.test.testmouse.reset()

    return rv


################################################################################
## Reporting methods

def report_testcase_skipped(node: TestCase) -> None:
    """
    Marks all children (if any) of the given testcase as skipped.
    """
    if isinstance(node, TestSuite):
        for child in node.testcases:
            report_testcase_skipped(child)

    results = all_results.get_result_by_name(node.name)
    testreporter.reporter.test_case_skipped(node)
    results.end(testreporter.TestCaseStatus.SKIPPED)


def get_frame_stack() -> list[FrameSummary]:
    """
    Returns a list of FrameSummary objects representing the current context stack.
    This indicates where the exception occurred in the test execution.
    """
    frame_stack: list[FrameSummary] = []

    nodes = [ctx.testsuite for ctx in context_stack]
    labels = [None] + [f"testsuite {ctx.testsuite.name}" for ctx in context_stack[:-1]]

    block = context_stack[-1].testsuite.current_block

    if isinstance(block, TestCase):
        nodes += [block, context_stack[-1].executor.node]
        labels += [
            f"testsuite {context_stack[-1].testsuite.name}",
            f"testcase {block.name}"
            ]
    elif isinstance(block, renpy.test.testast.Block):
        nodes += [block, context_stack[-1].executor.node]
        labels += [
            f"testsuite {context_stack[-1].testsuite.name}",
            f"hook {block.name}"
            ]

    for n, label in zip(nodes, labels):
        if n is None:
            frame_stack.append(FrameSummary(label, "<during last test>", 0)) # type: ignore
        else:
            frame_stack.append(FrameSummary(label, n.filename, n.linenumber)) # type: ignore

    return frame_stack


class TestSuiteContext:
    """
    A context manager for testcases. This is used to set the current node and state
    when entering a testcase, and to reset them when exiting.
    """

    testsuite: TestSuite
    "The testcase being executed."

    results: testreporter.TestSuiteResults
    "The results of the testcase being executed."

    executor: "NodeExecutor"
    "The executor for the current node."


    def __init__(self, node: TestSuite):
        self.testsuite = node
        results = all_results.get_result_by_name(node.name)
        if not isinstance(results, testreporter.TestSuiteResults):
            raise ValueError(f"TestSuiteResults not found for {node.name}")
        self.results = results
        self.executor = NodeExecutor(results, None)


    def execute(self) -> None:
        try:
            self.prepare_next_execution()
            if self.executor.done:
                return

            self.executor.execute()
            if self.executor.done and isinstance(self.testsuite.current_block, TestCase):
                self.executor.results.end(testreporter.TestCaseStatus.PASSED)
                testreporter.reporter.test_case_end(self.executor.results)

        except renpy.game.QuitException:
            raise

        except Exception as exc:
            self.handle_exception(exc)

            if isinstance(self.executor.node, renpy.test.testast.Until):
                ## Clean up the Until node if it was running.
                self.executor.node.left.after_until()



    def prepare_next_execution(self):
        """
        If the executor has finished executing the current node,
        this method will reinitialize it with the next node to execute,
        or alter the context stack as needed.
        """
        if not self.executor.done:
            return

        next_node = self.testsuite.get_next_block()
        if isinstance(next_node, TestSuite):
            push_context_stack(next_node)
            return

        if next_node is None:
            pop_context_stack()
            return

        if isinstance(next_node, TestCase):
            if next_node.skip:
                report_testcase_skipped(next_node)
                return

            testcase_results = all_results.get_result_by_name(next_node.name)
            testcase_results.begin()
            self.executor.reinitialize(testcase_results, next_node)
            return

        self.executor.reinitialize(self.results, next_node)

    def handle_exception(self, exc: Exception) -> None:
        frame_stack = get_frame_stack()
        testreporter.reporter.log_exception(exc, frame_stack)

        self.executor.results.end(testreporter.TestCaseStatus.FAILED)
        self.executor.reinitialize(self.executor.results, None)

        ## If the exception happened outside of a testcase (eg. in the "before" hook),
        ## mark the testsuite as failed.
        if not self.testsuite.is_in_testcase:
            self.results.end(testreporter.TestCaseStatus.FAILED)
            pop_context_stack()


class NodeExecutor:
    """
    This class is responsible for executing a single node in the test execution.
    It manages the state of the node, handles starting and executing it, and
    transitions to the next node when the current one is done.
    """

    node: Node | None = None
    "Current node being executed."

    state: State | None = None
    "The state of the current node being executed."

    node_has_started: bool = False
    "Whether the current node has run the start() method."

    next_node: Node | None = None
    "The next node to execute after the current one."

    old_state: State | None = None
    "The previous state of the current node."

    old_loc: NodeLocation | None = None
    "The previous location in the game script of the current node."

    last_state_change: float = 0.0
    "The last time the state changed."

    results: testreporter.TestCaseResults
    "The results of the current testcase being executed, if any."

    def __init__(self, results: testreporter.TestCaseResults, node: Node | None = None):
        self.reinitialize(results, node)

    def reinitialize(self, results: testreporter.TestCaseResults, node: Node | None) -> None:
        self.node = node
        self.state = None
        self.node_has_started = False
        self.next_node = None
        self.old_state = None
        self.old_loc = None
        self.last_state_change = renpy.display.core.get_time()
        self.results = results

    def set_next_node(self, next: Node | None) -> None:
        self.next_node = next

    def execute(self) -> None:
        """
        Performs one execution cycle of a node.
        """
        if self.node is None:
            raise RuntimeError("No node to execute.")

        now = renpy.display.core.get_time()

        self.try_to_start_node(now)

        if self.node_has_started:
            self.state = self.node.execute(self.state, now - self.start)
            self.try_to_move_to_next_node()

        self.check_for_timeout(now)

    def try_to_start_node(self, now) -> None:
        if self.node_has_started:
            return

        if self.node.ready():
            self.state = self.node.start()
            self.start = now
            self.node_has_started = True
        else:
            self.state = None
            self.node_has_started = False

    def try_to_move_to_next_node(self) -> None:
        if self.state is not None:
            return

        self.node.done = True

        if isinstance(self.node, renpy.test.testast.Assert):
            self.handle_assertion_node(self.node)

        self.node = self.next_node
        self.node_has_started = False

    def check_for_timeout(self, now) -> None:
        self.update_last_state_change(now)

        if (now - self.last_state_change) > _test.timeout:
            raise RenpyTestTimeoutError(f"Testcase timed out after {_test.timeout} seconds.")

    def update_last_state_change(self, now):
        loc = renpy.exports.get_filename_line()

        if (self.old_state != self.state) or (self.old_loc != loc):
            self.last_state_change = now

        self.old_state = self.state
        self.old_loc = loc

    def handle_assertion_node(self, assertion: renpy.test.testast.Assert) -> None:
        self.results.num_asserts += 1
        testreporter.reporter.log_assert(assertion)

        if assertion.failed:
            self.results.num_asserts_failed += 1
            raise RenpyTestAssertionError(f"Assertion failed: {assertion}")
        else:
            self.results.num_asserts_passed += 1

    @property
    def done(self) -> bool:
        return self.node is None


def test_command() -> bool:
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ## NOTE: This command gets called when the game starts for the first time,
    ## OR when the game goes back to the main menu after finishing the game.
    if initialized:
        return True

    ap = renpy.arguments.ArgumentParser(description="Runs a testcase.")
    ap.add_argument("testcase", help="The name of a testcase to run.", nargs="?",
                    default=global_testsuite_name)
    ap.add_argument("--no-skip", action="store_true", dest="ignore_skip_flag", default=False,
                    help="Do not skip testcases marked as skip.")
    ap.add_argument("--print-details", action="store_true", dest="print_details", default=False,
                    help="Print detailed information for entire run.")
    ap.add_argument("--print-skipped", action="store_true", dest="print_skipped", default=False,
                    help="Print information about skipped testcases. Requires --print-detailed.")

    args = ap.parse_args()
    _test.ignore_skip_flag = args.ignore_skip_flag
    _test.print_skipped = args.print_skipped
    _test.print_details = args.print_details

    testreporter.reporter.register(testreporter.ConsoleReporter())
    initialize(args.testcase)

    return True


renpy.arguments.register_command("test", test_command, uses_display=True)
