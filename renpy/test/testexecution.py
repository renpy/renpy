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

initialized: bool = False

# A map from the name of a testcase to the testcase.
testcases: dict[str, TestCase] = {}

# An action to run before executing another command.
action: Node | None = None

# The set of labels that have been reached since the last time execute
# has been called.
labels: set[str] = set()

# A stack of text contexts, which tracks the execution of testcases.
context_stack: list["TestSuiteContext"] = []

all_results: testreporter.TestSuiteResults

def take_name(name: str) -> None:
    """
    Takes the name of a statement that is about to run.
    """

    if not is_in_test():
        return

    if isinstance(name, str):
        labels.add(name)


def add_testcase(name: str, node: TestCase, parent: TestSuite | None = None) -> None:
    """
    Adds a testcase to the `testcases` dictionary. The name is a tuple of strings,
    and the node is the root node of the testcase.
    """

    ## NOTE: This is run every time the script is reloaded.

    if name in testcases:
        if testcases[name] != node:
            existing = testcases[name]
            raise KeyError(
                f"The testcase \"{name}\" is defined twice, "
                f"at File {existing.filename}:{existing.linenumber} "
                f"and File {node.filename}:{node.linenumber}.")
        else:
            return

    testcases[name] = node

    if (parent is None) and ("." in name):
        ## Add top-level dotted name tests to the appropriate testsuite
        parent_name = name.rsplit(".", 1)[0]
        parent_node = lookup(parent_name)
        if not isinstance(parent_node, TestSuite):
            raise TypeError(f"Parent node \"{parent_name}\" is not a TestSuite.")
        parent_node.children.append(node)

    if isinstance(node, TestSuite):
        for child in node.children:
            add_testcase(child.name, child, node)


def lookup(name: str, from_node: Node | None = None) -> TestCase:
    """
    Tries to look up the name with `target`. If found, returns it, otherwise
    raises an exception.
    """

    if name in testcases:
        return testcases[name]

    if from_node is None:
        raise KeyError("Testcase {} not found.".format(name))
    raise KeyError("Testcase {} not found at {}:{}.".format(name, from_node.filename, from_node.linenumber))


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

    testreporter.reporter.register(testreporter.ConsoleReporter())
    renpy.config.exception_handler = exception_handler

    if name != "all":
        root = lookup(name)
    else:
        ## Set up the "all" testsuite
        if "all" not in testcases:
            add_testcase("all", TestSuite(name="all", loc=("", 0), children=[]))
        root = lookup("all")

        if not isinstance(root, TestSuite):
            raise ValueError("Root node for 'all' must be a TestSuite, got {}".format(type(root)))

        for node_name, node in testcases.items():
            if node_name == "all" or "." in node_name:
                continue
            root.children.append(node)

    ## If the root is not a TestSuite, create one with root as the child.
    if isinstance(root, TestSuite):
        suite = root
    else:
        suite = TestSuite(name="<Top>", loc=(root.filename, root.linenumber), children=[root])


    ## Mark skipped tests correctly
    def _update_skip_flag(node: TestSuite) -> None:
        for child in node.children:
            if isinstance(child, TestSuite):
                _update_skip_flag(child)
            else:
                child.skip = child.skip and not _test.ignore_skip_flag

        node.skip = not _test.ignore_skip_flag and all(child.skip for child in node.children)

    _update_skip_flag(suite)

    ## Chain the nodes in the testcases
    for case in testcases.values():
        case.chain(None)

    all_results = testreporter.TestSuiteResults(suite.name)
    all_results.populate_children(suite)
    push_context_stack(suite)

    initialized = True


def push_context_stack(node: TestSuite) -> None:
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
        ctx.ran_testcase = True

    renpy.test.testmouse.reset()

    return rv


def get_current_context() -> "TestSuiteContext":
    """
    Returns the current context, or raises an exception if there is no context.
    """

    global context_stack

    if len(context_stack) == 0:
        raise Exception("No context on context stack.")

    return context_stack[-1]


def set_next_node(next: Node | None) -> None:
    """
    Sets the next node to execute. This is used to change the flow of execution
    to a different node.
    """

    get_current_context().executor.set_next_node(next)


def is_in_test() -> bool:
    return len(context_stack) > 0


def report_testcase_skipped(node: TestCase) -> None:
    """
    Marks all children (if any) of the given testcase as skipped.
    """
    if isinstance(node, TestSuite):
        for child in node.children:
            report_testcase_skipped(child)

    results = all_results.get_result_by_name(node.name)
    testreporter.reporter.test_case_skipped(node)
    results.end(testreporter.TestCaseStatus.SKIPPED)


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


def exception_handler(exc: renpy.error.TracebackException) -> bool:
    """
    Handles exceptions that occur during the execution of testcases.
    This is called by Ren'Py when an exception is raised.
    """
    if not is_in_test():
        return False

    get_current_context().handle_exception(None)
    return True


def quit_handler() -> int:
    """
    Handles the quit command and QuitException thrown by the test.
    Returns a status code that indicates whether the test passed or failed.
    """

    global context_stack

    while context_stack:
        pop_context_stack()

    if all_results.status == testreporter.TestCaseStatus.FAILED:
        return 1
    return 0

class TestSuiteContext:
    """
    A context manager for testcases. This is used to set the current node and state
    when entering a testcase, and to reset them when exiting.
    """

    testsuite: TestSuite
    """The testcase being executed."""

    results: testreporter.TestSuiteResults
    """The results of the testcase being executed."""

    testcase_index: int = 0
    """The index of the current testcase being executed."""

    ran_before: bool = False
    """Whether the before() method of the testcase has been run."""

    ran_before_each: bool = False
    """Whether the before_each() method of the testcase has been run."""

    ran_testcase: bool = False
    """Whether the current testcase has been run."""

    ran_after_each: bool = False
    """Whether the after_each() method of the testcase has been run."""

    ran_after: bool = False
    """Whether the after() method of the testcase has been run."""

    executor: "NodeExecutor"


    def __init__(self, node: TestSuite):
        self.testsuite = node
        results = all_results.get_result_by_name(node.name)
        if not isinstance(results, testreporter.TestSuiteResults):
            raise ValueError("TestSuiteResults not found for {}".format(node.name))
        self.results = results

        self.testcase_index = 0
        self.ran_before = self.testsuite.before is None
        self.ran_after = self.testsuite.after is None
        self.executor = NodeExecutor(results, None)

        self.prepare_for_next_testcase()


    def prepare_for_next_testcase(self) -> None:
        self.ran_before_each = self.testsuite.before_each is None
        self.ran_testcase = len(self.testsuite.children) == 0
        self.ran_after_each = self.testsuite.after_each is None


    def execute(self) -> None:
        try:
            ## Before
            if not self.ran_before and self.testsuite.before:
                if self.executor.done:
                    self.executor.reinitialize(self.results, self.testsuite.before)

                self.executor.execute()
                self.ran_before = self.executor.done

            ## Before Each
            elif not self.ran_before_each and self.testsuite.before_each:
                if self.executor.done:
                    self.executor.reinitialize(self.results, self.testsuite.before_each)

                self.executor.execute()
                self.ran_before_each = self.executor.done

            ## Test Case
            elif not self.ran_testcase and self.testsuite.children:
                if self.executor.done:
                    new_case = self.testsuite.children[self.testcase_index]

                    if new_case.skip:
                        report_testcase_skipped(new_case)

                        self.testcase_index += 1
                        if self.testcase_index >= len(self.testsuite.children):
                            self.ran_testcase = True
                        return

                    if isinstance(new_case, TestSuite):
                        push_context_stack(new_case)
                        return
                    else:
                        test_results = all_results.get_result_by_name(new_case.name)
                        self.executor.reinitialize(test_results, new_case)
                        test_results.begin()

                self.executor.execute()
                self.ran_testcase = self.executor.done
                if self.ran_testcase:
                    self.executor.results.end(testreporter.TestCaseStatus.PASSED)

            ## After Each
            elif not self.ran_after_each and self.testsuite.after_each:
                if self.executor.done:
                    self.executor.reinitialize(self.results, self.testsuite.after_each)

                self.executor.execute()
                self.ran_after_each = self.executor.done

            elif self.testcase_index < len(self.testsuite.children) - 1:
                self.testcase_index += 1
                self.prepare_for_next_testcase()

            ## After
            elif not self.ran_after and self.testsuite.after:
                if self.executor.done:
                    self.executor.reinitialize(self.results, self.testsuite.after)

                self.executor.execute()
                self.ran_after = self.executor.done

            ## Done with the testsuite
            else:
                pop_context_stack()

        except renpy.game.QuitException:
            raise

        except Exception as exc:
            self.handle_exception(exc)


    def handle_exception(self, exc: Exception | None) -> None:
        ## Find where in the test execution the exception happened.
        if len(context_stack) == 0:
            raise RuntimeError("No context stack available for exception reporting.")

        frame_stack: list[FrameSummary] = []

        nodes = [ctx.testsuite for ctx in context_stack]
        labels = [None] + [f"testsuite {ctx.testsuite.name}" for ctx in context_stack[:-1]]

        if context_stack[-1].executor.testcase:
            nodes += [context_stack[-1].executor.testcase, context_stack[-1].executor.node]
            labels += [
                f"testsuite {context_stack[-1].testsuite.name}",
                f"testcase {context_stack[-1].executor.testcase.name}"
                ]

        for n, label in zip(nodes, labels):
            frame_stack.append(FrameSummary(label, n.filename, n.linenumber)) # type: ignore

        ## Pass to the reporter
        testreporter.reporter.log_exception(exc, frame_stack)

        self.executor.results.end(testreporter.TestCaseStatus.FAILED)

        if self.ran_before and self.ran_before_each and not self.ran_testcase:
            ## If the exception happened in a testcase, move to the next one.
            self.executor.reinitialize(self.results, None)
            self.ran_testcase = True

        else:
            ## The exception happened outside of a testcase (eg. in the "before" hook),
            ## so declare the testsuite failed.
            self.results.end(testreporter.TestCaseStatus.FAILED)
            pop_context_stack()

class NodeExecutor:
    node: Node | None = None
    """Current node being executed."""

    state: State | None = None
    """The state of the current node being executed."""

    node_has_started: bool = False
    """Whether the current node has run the start() method."""

    next_node: Node | None = None
    """The next node to execute after the current one."""

    old_state: State | None = None
    """The previous state of the current node."""

    old_loc: NodeLocation | None = None
    """The previous location in the game script of the current node."""

    last_state_change: float = 0.0
    """The last time the state changed."""

    testcase: TestCase | None = None
    """The current testcase being executed, if any."""

    results: testreporter.TestCaseResults
    """The results of the current testcase being executed, if any."""

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

        if isinstance(node, TestCase):
            self.testcase = node
        else:
            self.testcase = None

    def set_next_node(self, next: Node | None) -> None:
        self.next_node = next

    def execute(self) -> None:
        """
        Performs one execution cycle of a node.
        """
        now = renpy.display.core.get_time()

        if not self.node_has_started:
            if self.node.ready():
                self.state = self.node.start()
                self.start = now
                self.node_has_started = True
            else:
                self.state = None
                self.node_has_started = False


        if self.node_has_started:
            self.state = self.node.execute(self.state, now - self.start)

            ## If the current state is None, move to the next node
            if self.state is None:
                if isinstance(self.node, renpy.test.testast.Assert):
                    self.results.num_asserts += 1
                    testreporter.reporter.log_assert(self.node)

                    if self.node.failed:
                        self.results.num_asserts_failed += 1
                        raise RenpyTestAssertionError("Assertion failed: {}".format(self.node))
                    else:
                        self.results.num_asserts_passed += 1

                self.node = self.next_node
                self.node_has_started = False

        loc = renpy.exports.get_filename_line()

        if (self.old_state != self.state) or (self.old_loc != loc):
            self.last_state_change = now

        self.old_state = self.state
        self.old_loc = loc

        if (now - self.last_state_change) > _test.timeout:
            raise RenpyTestTimeoutError("Testcase timed out after {} seconds.".format(_test.timeout))

    @property
    def done(self) -> bool:
        return self.node is None


def test_command() -> bool:
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ap = renpy.arguments.ArgumentParser(description="Runs a testcase.")
    ap.add_argument("testcase", help="The name of a testcase to run.", nargs="?", default="all")
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

    ## NOTE: This command gets called when the game starts for the first time, OR when the game
    ## goes back to the main menu after finishing the game. Special care is taken to avoid
    ## messing up the state of the test/call stack
    initialize(args.testcase)

    return True


renpy.arguments.register_command("test", test_command, uses_display=True)
